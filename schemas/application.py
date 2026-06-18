from pydantic import BaseModel
from datetime import datetime


class UserApplicationBase(BaseModel):
    scholarship_id:int
    user_id:int
    statement:str

class UserApplicationCreate(UserApplicationBase):
    pass

class UserApplicationResponse(UserApplicationBase):
    id:int
    applied_at:datetime
    status:str


    class Config:
        from_attributes=True

