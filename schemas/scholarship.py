from pydantic import BaseModel, Field
 
class UserScholarshipCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str
    amount: float = Field(gt=5000, lt=50000)
    deadline: str
    eligibility: str  
 
class UserScholarshipResponse(BaseModel):
    id: int
    name: str
    description: str
    amount: float
    deadline: str
    eligibility: str  

    class Config:
        from_attributes = True
 