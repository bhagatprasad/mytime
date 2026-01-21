from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class EmployeeEmergencyContact(Base):
    __tablename__ = "EmployeeEmergencyContact"  # Match your SQL Server table name
    
    EmployeeEmergencyContactId = Column(Integer, primary_key=True, index=True)
    EmployeeId = Column(Integer, nullable=True)
    Name = Column(String(max), nullable=True)
    Relation = Column(String(max), nullable=True)
    Phone = Column(String(max), nullable=True)
    Email = Column(String(max), nullable=True)
    Address = Column(String(max), nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    CreatedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    ModifiedBy = Column(Integer, nullable=True)
    IsActive = Column(Boolean, nullable=True)
    
    def __repr__(self):
        return f"<EmployeeEmergencyContact(EmployeeEmergencyContactId={self.EmployeeEmergencyContactId}, EmployeeId={self.EmployeeId}, Name='{self.Name}')>"