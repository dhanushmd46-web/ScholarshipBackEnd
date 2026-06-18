from sqlalchemy import Column, Integer, String, CheckConstraint
from database import Base
 
class UserTable(Base):
    __tablename__ = "User_table"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(10), CheckConstraint("role IN ('user','admin')"), default="user", nullable=False)