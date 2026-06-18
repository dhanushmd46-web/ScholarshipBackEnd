from pydantic import BaseModel
 
class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "user"
 
class UserLogin(BaseModel):
    username: str
    password: str
 
    class Config:
        from_attributes = True