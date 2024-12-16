from pydantic import BaseModel

class Body(BaseModel):
    UserID: int
    Login: str
    Password: str
    Key: str
