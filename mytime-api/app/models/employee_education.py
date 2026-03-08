from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base

class EmployeeEducation(Base):
    __tablename__ = "EmployeeEducation"  # Match your SQL Server table name
    
    EmployeeEducationId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    EmployeeId = Column(Integer, nullable=False)  # Should likely be NOT NULL
    Degree = Column(String(255), nullable=True)  # Specify length instead of 'max'
    FeildOfStudy = Column(String(255), nullable=True)  # Fixed typo: 'Field' not 'Feild'
    Institution = Column(String(500), nullable=True)
    YearOfCompletion = Column(DateTime, nullable=True)
    PercentageMarks = Column(String(50), nullable=True)  # Limit length
    Year = Column(String(10), nullable=True)
    CreatedOn = Column(DateTime, nullable=True, default=None)
    CreatedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime, nullable=True, default=None, onupdate=None)
    ModifiedBy = Column(Integer, nullable=True)
    IsActive = Column(Boolean, nullable=True, default=True)
    
    def __repr__(self):
        return f"<EmployeeEducation(EmployeeEducationId={self.EmployeeEducationId}, EmployeeId={self.EmployeeId}, Degree='{self.Degree}')>"