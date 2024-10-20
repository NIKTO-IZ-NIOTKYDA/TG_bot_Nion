import datetime
from dataclasses import field, dataclass
from gc import callbacks
from typing import Any, Dict, List

from httpx import Response
from marshmallow import EXCLUDE, Schema, pre_load
from marshmallow_dataclass import class_schema

__all__ = ['Attachment', 'Announcement', 'Assignment', 'Diary', 'School']


class NetSchoolAPISchema(Schema):
    class Meta:
        dateformat = '%Y-%m-%dT00:00:00'
        unknown = EXCLUDE


@dataclass
class Attachment(NetSchoolAPISchema):
    id: int
    name: str = field(metadata=dict(data_key='originalFileName'))
    description: str = field(metadata=dict(
        allow_none=True, missing='', required=False
    ))


@dataclass
class Author(NetSchoolAPISchema):
    id: int
    full_name: str = field(metadata=dict(data_key="fio"))
    nickname: str = field(metadata=dict(data_key="nickName"))


@dataclass
class Announcement(NetSchoolAPISchema):
    name: str
    author: Author
    content: str = field(metadata=dict(data_key='description'))
    post_date: datetime.datetime = field(metadata=dict(data_key='postDate'))
    attachments: List[Attachment] = field(default_factory=list)


@dataclass
class Assignment(NetSchoolAPISchema):
    id: int
    comment: str
    type: str
    content: str = field(metadata=dict(data_key='assignmentName'))
    mark: int = field(metadata=dict(allow_none=True, data_key='mark'))
    is_duty: bool = field(metadata=dict(data_key='dutyMark'))
    deadline: datetime.date = field(metadata=dict(data_key='dueDate'))

    @pre_load
    def unwrap_marks(self, assignment: Dict[str, Any], **_) -> Dict[str, str]:
        mark = assignment.pop('mark', None)
        if mark:
            assignment.update(mark)
        else:
            assignment.update({'mark': None, 'dutyMark': False})
        mark_comment = assignment.pop("markComment", None)
        assignment["comment"] = mark_comment["name"] if mark_comment else ""
        assignment["type"] = self.context["assignment_types"][assignment.pop("typeId")]
        return assignment


@dataclass
class Lesson(NetSchoolAPISchema):
    day: datetime.date
    start: datetime.time = field(metadata=dict(data_key='startTime'))
    end: datetime.time = field(metadata=dict(data_key='endTime'))
    room: str = field(metadata=dict(
        missing='', allow_none=True, required=False
    ))
    number: int
    subject: str = field(metadata=dict(data_key='subjectName'))
    assignments: List[Assignment] = field(default_factory=list)


@dataclass
class Day(NetSchoolAPISchema):
    lessons: List[Lesson]
    day: datetime.date = field(metadata=dict(data_key='date'))


@dataclass
class Diary(NetSchoolAPISchema):
    start: datetime.date = field(metadata=dict(data_key='weekStart'))
    end: datetime.date = field(metadata=dict(data_key='weekEnd'))
    schedule: List[Day] = field(metadata=dict(data_key='weekDays'))


class ParamsAverageMark_SID(NetSchoolAPISchema):
    filterId: str = "SID"
    filterText: str = None
    filterValue: str = None

    def __init__(self, filterText: str, filterValue: str):
        self.filterText = filterText
        self.filterValue = filterValue


class ParamsAverageMark_MarksType(NetSchoolAPISchema):
    filterId: str = "MarksType"
    filterText: str = None
    filterValue: str = None

    def __init__(self,  filterText: str, filterValue: str):
        self.filterText = filterText
        self.filterValue = filterValue


class ParamsAverageMark_PCLID(NetSchoolAPISchema):
    filterId: str = "PCLID"
    filterText: str = None
    filterValue: str = None

    def __init__(self,  filterText: str, filterValue: str):
        self.filterText = filterText
        self.filterValue = filterValue


class ParamsAverageMark_TERMID(NetSchoolAPISchema):
    filterId: str = "TERMID"
    filterText: str = None
    filterValue: str = None

    def __init__(self,  filterText: str, filterValue: str):
        self.filterText = filterText
        self.filterValue = filterValue


class ParamsAverageMark(NetSchoolAPISchema):
    SID: ParamsAverageMark_SID = None
    MarkType: ParamsAverageMark_MarksType = None
    PCLID: ParamsAverageMark_PCLID = None
    TERMIDs: list[ParamsAverageMark_TERMID] = []


    def __init__(self, response: Response):
        TERMIDs: list[dict[str, str]] = response['filterSources'][3]['items']
        TERMIDs.pop(0)

        self.SID = ParamsAverageMark_SID(
            filterText=response['filterSources'][0]['items'][0]['title'],
            filterValue=response['filterSources'][0]['items'][0]['value'])
        
        self.MarkType = ParamsAverageMark_MarksType(
            filterText=response['filterSources'][1]['items'][0]['title'],
            filterValue=response['filterSources'][1]['items'][0]['value'])
        
        self.PCLID = ParamsAverageMark_PCLID(
            filterText=response['filterSources'][2]['items'][0]['title'],
            filterValue=response['filterSources'][2]['items'][0]['value'])

        for TERMID in TERMIDs:
            self.TERMIDs.append(
                ParamsAverageMark_TERMID(
                    filterText=TERMID["title"],
                    filterValue=TERMID["value"]
                )
            )


class InitFilters():
    start: datetime.date
    end: datetime.date

    def __init__(self, start: datetime.date, end: datetime.date):
        self.start = start
        self.end = end


@dataclass
class ShortSchool(NetSchoolAPISchema):
    name: str
    id: int
    address: str = field(metadata=dict(data_key="addressString"))


@dataclass
class School(NetSchoolAPISchema):
    name: str = field(metadata=dict(data_key='fullSchoolName'))
    about: str

    address: str
    email: str
    site: str = field(metadata=dict(data_key='web'))
    phone: str = field(metadata=dict(data_key='phones'))

    director: str
    AHC: str = field(metadata=dict(data_key='principalAHC'))
    IT: str = field(metadata=dict(data_key='principalIT'))
    UVR: str = field(metadata=dict(data_key='principalUVR'))

    @pre_load
    def unwrap_nested_dicts(
            self, school: Dict[str, Any], **_) -> Dict[str, str]:
        school.update(school.pop('commonInfo'))
        school.update(school.pop('contactInfo'))
        school.update(school.pop('managementInfo'))
        school['address'] = school['juridicalAddress'] or school['postAddress']
        return school


AttachmentSchema = class_schema(Attachment)
DiarySchema = class_schema(Diary)
AssignmentSchema = class_schema(Assignment)
ShortSchoolSchema = class_schema(ShortSchool)
SchoolSchema = class_schema(School)
AnnouncementSchema = class_schema(Announcement)
