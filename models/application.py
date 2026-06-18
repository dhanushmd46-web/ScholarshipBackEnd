from sqlalchemy import Integer, Text, DateTime, String, Column, ForeignKey
from database import Base

class ApplicationTable(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    scholarship_id = Column(Integer, ForeignKey("table_scholarship.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("User_table.id"), nullable=False)
    statement = Column(Text, nullable=False)
    applied_at = Column(DateTime, nullable=False)
    status = Column(String(20), default='Under Review')
