from sqlalchemy import Column, Integer, String, Text, Float
from database import Base
 
class ScholarshipTable(Base):
    __tablename__ = "table_scholarship"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    deadline = Column(String(20), nullable=False)
    eligibility = Column(Text, nullable=False)  
 