from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class EmployeeEducation(Base):
    __tablename__ = "EmployeeEducation"  # Match your SQL Server table name
    
    EmployeeEducationId = Column(Integer, primary_key=True, index=True)
    EmployeeId = Column(Integer, nullable=True)
    Degree = Column(String(max), nullable=True)
    FeildOfStudy = Column(String(max), nullable=True)  # Corrected typo from "FeildOfStudy"
    Institution = Column(String(max), nullable=True)
    YearOfCompletion = Column(DateTime(timezone=True), nullable=True)
    PercentageMarks = Column(String(max), nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    CreatedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    ModifiedBy = Column(Integer, nullable=True)
    IsActive = Column(Boolean, nullable=True)
    Year = Column(String(10), nullable=True)
    
    def __repr__(self):
        return f"<EmployeeEducation(EmployeeEducationId={self.EmployeeEducationId}, EmployeeId={self.EmployeeId}, Degree='{self.Degree}')>"