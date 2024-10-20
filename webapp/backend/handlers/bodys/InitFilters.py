from pydantic import BaseModel

class Body(BaseModel):
    SID_filterId: str = "SID"
    SID_filterText: str
    SID_filterValue: str

    MarksType_filterId: str = "MarksType"
    MarksType_filterText: str
    MarksType_filterValue: str

    PCLID_filterId: str = "PCLID"
    PCLID_filterText: str
    PCLID_filterValue: str

    TERM_filterId: str = "TERMID"
    TERM_filterText: str
    TERM_filterValue: str

    # def __init__(self,
    #             SID_filterId: str,
    #             SID_filterText: str,
    #             SID_filterValue: str,
    #             MarksType_filterId: str,
    #             MarksType_filterText: str,
    #             MarksType_filterValue: str,
    #             PCLID_filterId: str,
    #             PCLID_filterText: str,
    #             PCLID_filterValue: str,
    #             TERM_filterId: str,
    #             TERM_filterText: str,
    #             TERM_filterValue: str
    #             ):
    #     self.SID_filterId = SID_filterId
    #     self.SID_filterText = SID_filterText
    #     self.SID_filterValue = SID_filterValue

    #     self.MarksType_filterId = MarksType_filterId
    #     self.MarksType_filterText = MarksType_filterText
    #     self.MarksType_filterValue = MarksType_filterValue

    #     self.PCLID_filterId = PCLID_filterId
    #     self.PCLID_filterText = PCLID_filterText
    #     self.PCLID_filterValue = PCLID_filterValue

    #     self.TERM_filterId = TERM_filterId
    #     self.TERM_filterText = TERM_filterText
    #     self.TERM_filterValue = TERM_filterValue
