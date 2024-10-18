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
