from ast import Try
from io import BytesIO
from hashlib import md5
from datetime import date, timedelta
from typing import Optional, Dict, List, Union, Any
from webapp.backend.handlers.bodys.InitFilters import Body as BodyRQFromInitFilters

import httpx
from httpx import AsyncClient, Response

from webapp.backend.netschoolapi import errors, schemas

__all__ = ['NetSchoolAPI']

from webapp.backend.netschoolapi.async_client_wrapper import AsyncClientWrapper, Requester


async def _die_on_bad_status(response: Response):
    if not response.is_redirect:
        response.raise_for_status()


class NetSchoolAPI:
    def __init__(self, url: str, default_requests_timeout: int = None):
        url = url.rstrip('/')
        self._wrapped_client = AsyncClientWrapper(
            async_client=AsyncClient(
                base_url=f'{url}/webapi',
                headers={'user-agent': 'NetSchoolAPI/5.0.3', 'referer': url},
                event_hooks={'response': [_die_on_bad_status]},
            ),
            default_requests_timeout=default_requests_timeout,
        )

        self._student_id = -1
        self._year_id = -1
        self._school_id = -1

        self._assignment_types: Dict[int, str] = {}
        self._login_data = ()
        self._access_token = None

    async def __aenter__(self) -> 'NetSchoolAPI':
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):
        await self.logout()

    async def login(
            self, user_name: str, password: str,
            school_name_or_id: Union[int, str],
            requests_timeout: int = None):
        requester = self._wrapped_client.make_requester(requests_timeout)
        # Getting the `NSSESSIONID` cookie for `auth/getdata`
        await requester(self._wrapped_client.client.build_request(
            method="GET", url="logindata"
        ))

        # Getting the `NSSESSIONID` cookie for `login`
        response = await requester(self._wrapped_client.client.build_request(
            method="POST", url='auth/getdata'
        ))
        login_meta = response.json()
        salt = login_meta.pop('salt')

        encoded_password = md5(
            password.encode('windows-1251')
        ).hexdigest().encode()
        pw2 = md5(salt.encode() + encoded_password).hexdigest()
        pw = pw2[: len(password)]

        try:
            response = await requester(
                self._wrapped_client.client.build_request(
                    method="POST",
                    url='login',
                    data={
                        'loginType': 1,
                        'scid': (
                            (await self._get_school_id(
                                school_name_or_id, requester,
                            ))
                            if isinstance(school_name_or_id, str) else
                            school_name_or_id
                        ),
                        'un': user_name,
                        'pw': pw,
                        'pw2': pw2,
                        **login_meta,
                    },
                )
            )
        except httpx.HTTPStatusError as http_status_error:
            if http_status_error.response.status_code == httpx.codes.CONFLICT:
                try:
                    response_json = http_status_error.response.json()
                except httpx.ResponseNotRead:
                    pass
                else:
                    if 'message' in response_json:
                        raise errors.AuthError(
                            http_status_error.response.json()['message']
                        )
                raise errors.AuthError()
            else:
                raise http_status_error
        auth_result = response.json()

        if 'at' not in auth_result:
            raise errors.AuthError(auth_result['message'])

        self._access_token = auth_result["at"]
        self._wrapped_client.client.headers['at'] = auth_result['at']

        response = await requester(self._wrapped_client.client.build_request(
            method="GET", url='student/diary/init',
        ))
        diary_info = response.json()
        student = diary_info['students'][diary_info['currentStudentId']]
        self._student_id = student['studentId']

        response = await requester(self._wrapped_client.client.build_request(
            method="GET", url='years/current'
        ))
        year_reference = response.json()
        self._year_id = year_reference['id']

        response = await requester(self._wrapped_client.client.build_request(
            method="GET", url="grade/assignment/types", params={"all": False},
        ))
        assignment_reference = response.json()
        self._assignment_types = {
            assignment['id']: assignment['name']
            for assignment in assignment_reference
        }
        self._login_data = (user_name, password, school_name_or_id)

    async def _request_with_optional_relogin(
            self, requests_timeout: Optional[int], request: httpx.Request,
            follow_redirects=False):
        try:
            response = await self._wrapped_client.request(
                requests_timeout, request, follow_redirects
            )
        except httpx.HTTPStatusError as http_status_error:
            if (
                http_status_error.response.status_code
                == httpx.codes.UNAUTHORIZED
            ):
                if self._login_data:
                    await self.login(*self._login_data)
                    return await self._request_with_optional_relogin(
                        requests_timeout, request, follow_redirects
                    )
                else:
                    raise errors.AuthError(
                        ".login() before making requests that need "
                        "authorization"
                    )
            else:
                raise http_status_error
        else:
            return response

    async def download_attachment(
            self, attachment_id: int, buffer: BytesIO,
            requests_timeout: int = None):
        buffer.write((
            await self._request_with_optional_relogin(
                requests_timeout,
                self._wrapped_client.client.build_request(
                    method="GET", url=f"attachments/{attachment_id}",
                )
            )
        ).content)

    async def diary(
        self,
        start: Optional[date] = None,
        end: Optional[date] = None,
        requests_timeout: int = None,
        json: bool = False
    ) -> schemas.Diary | Any:
        if not start:
            monday = date.today() - timedelta(days=date.today().weekday())
            start = monday
        if not end:
            end = start + timedelta(days=5)

        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url="student/diary",
                params={
                    'studentId': self._student_id,
                    'yearId': self._year_id,
                    'weekStart': start.isoformat(),
                    'weekEnd': end.isoformat(),
                },
            )
        )

        if json: return response.json()

        diary_schema = schemas.DiarySchema()
        diary_schema.context['assignment_types'] = self._assignment_types
        diary = diary_schema.load(response.json())
        return diary  # type: ignore

    async def params_average_mark(self, requests_timeout: int = None, json: bool = False) -> schemas.ParamsAverageMark | list[dict]:
        response = await self._request_with_optional_relogin(
                    requests_timeout,
                    self._wrapped_client.client.build_request(
                        method="GET",
                        url="v2/reports/studentaveragemark",
                        params={},
                    )
                )

        response_json = response.json()

        if json:
            return_data = {
                'selectedData': {
                    0: {
                        'filterId': 'SID',
                        'filterText': response_json['filterSources'][0]['items'][0]['title'],
                        'filterValue': response_json['filterSources'][0]['items'][0]['value'] 

                    },
                    1: {
                        'filterId': 'MarksType',
                        'filterText': response_json['filterSources'][1]['items'][0]['title'],
                        'filterValue': response_json['filterSources'][1]['items'][0]['value']
                    },
                    2: {
                        'filterId': 'PCLID',
                        'filterText': response_json['filterSources'][2]['items'][0]['title'],
                        'filterValue': response_json['filterSources'][2]['items'][0]['value']
                    },
                    3: []
                }
            }
            
            TERMIDs: list[dict[str, str]] = response_json['filterSources'][3]['items']
            TERMIDs.pop(0)

            for TERMID in TERMIDs:
                return_data['selectedData'][3].append({
                    'title': TERMID['title'],
                    'value': TERMID['value']
                })

            return return_data

        return schemas.ParamsAverageMark(response_json)  # type: ignore

    async def initfilters(
            self,
            requests_timeout: int = None,
            json: bool = False,
            class_data: BodyRQFromInitFilters | schemas.ParamsAverageMark = None
            ) -> schemas.ParamsAverageMark | dict | Exception:
        print('q')
        if class_data != None:
            if class_data == BodyRQFromInitFilters:
                response = await self._request_with_optional_relogin(
                    requests_timeout,
                    self._wrapped_client.client.build_request(
                        method="POST",
                        url="v2/reports/studentaveragemarkdyn/initfilters",
                        json={
                                "selectedData":
                                    [
                                        {
                                            "filterId": class_data.SID_filterId,
                                            "filterValue": class_data.SID_filterValue,
                                            "filterText": class_data.SID_filterText
                                        },
                                        {
                                            "filterId": class_data.MarksType_filterId,
                                            "filterValue": class_data.MarksType_filterValue,
                                            "filterText": class_data.MarksType_filterText
                                        },
                                        {
                                            "filterId": class_data.PCLID_filterId,
                                            "filterValue": class_data.PCLID_filterValue,
                                            "filterText": class_data.PCLID_filterText
                                        },
                                        {
                                            "filterId": class_data.TERM_filterId,
                                            "filterValue": class_data.TERM_filterValue,
                                            "filterText": class_data.TERM_filterText
                                        }
                                    ]
                                }
                        )
                )
            elif class_data == schemas.ParamsAverageMark:
                response_start = await self._request_with_optional_relogin(
                    requests_timeout,
                    self._wrapped_client.client.build_request(
                        method="POST",
                        url="v2/reports/studentaveragemarkdyn/initfilters",
                        json={
                                "selectedData":
                                    [
                                        {
                                            "filterId": class_data.SID.filterId,
                                            "filterValue": class_data.SID.filterValue,
                                            "filterText": class_data.SID.filterText
                                        },
                                        {
                                            "filterId": class_data.MarksType.filterId,
                                            "filterValue": class_data.MarksType.filterValue,
                                            "filterText": class_data.MarksType.filterText
                                        },
                                        {
                                            "filterId": class_data.PCLID.filterId,
                                            "filterValue": class_data.PCLID.filterValue,
                                            "filterText": class_data.PCLID.filterText
                                        },
                                        {
                                            "filterId": class_data.TERMIDs[0].filterId,
                                            "filterValue": class_data.TERMIDs[0].filterValue,
                                            "filterText": class_data.TERMIDs[0].filterText
                                        }
                                    ]
                                }
                        )
                )
                response_end = await self._request_with_optional_relogin(
                    requests_timeout,
                    self._wrapped_client.client.build_request(
                        method="POST",
                        url="v2/reports/studentaveragemarkdyn/initfilters",
                        json={
                                "selectedData":
                                    [
                                        {
                                            "filterId": class_data.SID.filterId,
                                            "filterValue": class_data.SID.filterValue,
                                            "filterText": class_data.SID.filterText
                                        },
                                        {
                                            "filterId": class_data.MarksType.filterId,
                                            "filterValue": class_data.MarksType.filterValue,
                                            "filterText": class_data.MarksType.filterText
                                        },
                                        {
                                            "filterId": class_data.PCLID.filterId,
                                            "filterValue": class_data.PCLID.filterValue,
                                            "filterText": class_data.PCLID.filterText
                                        },
                                        {
                                            "filterId": class_data.TERMIDs[-1].filterId,
                                            "filterValue": class_data.TERMIDs[-1].filterValue,
                                            "filterText": class_data.TERMIDs[-1].filterText
                                        }
                                    ]
                                }
                        )
                )
                return {
                    "start": response_start.json()['range']['start'][0.9],
                    "end": response_end.json()['range']['end'][0.9]
                    }
        if json: return response.json()

        response_json = response.json()
        return schemas.InitFilters(response_json['range']['start'][0.9], response_json['range']['end'][0.9])

    async def diary_assigns(self, id: str, requests_timeout: int = None, json: bool = True) -> Any:
        response = await self._request_with_optional_relogin(
                requests_timeout,
                self._wrapped_client.client.build_request(
                    method="POST",
                    url=f"student/diary/assigns/{id}",
                    params={
                        "studentId": self._student_id
                    }
                )
            )
        return response.json()

    async def overdue(
        self,
        start: Optional[date] = None,
        end: Optional[date] = None,
        requests_timeout: int = None,
        json: bool = False
    ) -> List[schemas.Assignment] | Any:
        if not start:
            monday = date.today() - timedelta(days=date.today().weekday())
            start = monday
        if not end:
            end = start + timedelta(days=5)

        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url='student/diary/pastMandatory',
                params={
                    'studentId': self._student_id,
                    'yearId': self._year_id,
                    'weekStart': start.isoformat(),
                    'weekEnd': end.isoformat(),
                },
            )
        )

        if json: return response.json()

        assignments_schema = schemas.AssignmentSchema()
        assignments_schema.context['assignment_types'] = self._assignment_types
        assignments = assignments_schema.load(response.json(), many=True)
        return assignments  # type: ignore

    async def announcements(
            self, take: Optional[int] = -1,
            requests_timeout: int = None,
            json: bool = False) -> List[schemas.Announcement] | Any:
        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url="announcements",
                params={"take": take},
            )
        )

        if json: return response.json()

        announcements = schemas.AnnouncementSchema().load(response.json(), many=True)
        return announcements  # type: ignore

    async def attachments(
            self, assignment_id: int,
            requests_timeout: int = None,
            json: bool = False
            ) -> List[schemas.Attachment] | Any:
        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="POST",
                url='student/diary/get-attachments',
                params={'studentId': self._student_id},
                json={'assignId': [assignment_id]},
            ),
        )

        response = response.json()

        if json: return response

        if not response:
            return []
        attachments_json = response[0]['attachments']
        attachments = schemas.AttachmentSchema().load(attachments_json, many=True)
        return attachments  # type: ignore

    async def school(
            self,
            requests_timeout: int = None,
            json: bool = False
                    ) -> schemas.School:
        response = await self._request_with_optional_relogin(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET",
                url='schools/{0}/card'.format(self._school_id),
            )
        )

        if json: return response.json()

        school = schemas.SchoolSchema().load(response.json())
        return school  # type: ignore

    async def logout(self, requests_timeout: int = None) -> None:
        try:
            await self._wrapped_client.request(
                requests_timeout,
                self._wrapped_client.client.build_request(
                    method="POST",
                    url='auth/logout',
                )
            )
        except httpx.HTTPStatusError as http_status_error:
            if (
                http_status_error.response.status_code
                == httpx.codes.UNAUTHORIZED
            ):
                # Session is dead => we are logged out already
                # OR
                # We are logged out already
                pass
            else:
                raise http_status_error

    async def full_logout(self, requests_timeout: int = None):
        await self.logout(requests_timeout)
        await self._wrapped_client.client.aclose()

    async def schools(
            self, requests_timeout: int = None) -> List[schemas.ShortSchool]:
        resp = await self._wrapped_client.request(
            requests_timeout,
            self._wrapped_client.client.build_request(
                method="GET", url="schools/search",
            )
        )
        schools = schemas.ShortSchoolSchema().load(resp.json(), many=True)
        return schools  # type: ignore

    async def _get_school_id(
            self, school_name: str,
            requester: Requester) -> Dict[str, int]:
        schools = (await requester(
            self._wrapped_client.client.build_request(
                method="GET",
                url="schools/search",
            )
        )).json()

        for school in schools:
            if school["shortName"] == school_name:
                self._school_id = school['id']
                return school["id"]
        raise errors.SchoolNotFoundError(school_name)

    async def download_profile_picture(
            self, user_id: int, buffer: BytesIO,
            requests_timeout: int = None):
        buffer.write((
            await self._request_with_optional_relogin(
                requests_timeout,
                self._wrapped_client.client.build_request(
                    method="GET",
                    url="users/photo",
                    params={"at": self._access_token, "userId": user_id},
                ),
                follow_redirects=True,
            )
        ).content)
