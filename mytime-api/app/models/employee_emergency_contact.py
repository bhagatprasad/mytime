from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class EmployeeEmergencyContact(Base):
    __tablename__ = "EmployeeEmergencyContact"  # Match your SQL Server table name
    
    EmployeeEmergencyContactId = Column(Integer, primary_key=True, index=True)
    EmployeeId = Column(Integer,    nullable=True)
    Name = Column(String(255), nullable=True)
    Relation = Column(String(100), nullable=True)
    Phone = Column(String(20), nullable=True)
    Email = Column(String(255), nullable=True)
    Address = Column(String(500), nullable=True)
    CreatedOn = Column(DateTime,    nullable=True)
    CreatedBy = Column(Integer,     nullable=True)
    ModifiedOn = Column(DateTime,   nullable=True)
    ModifiedBy = Column(Integer,    nullable=True)
    IsActive = Column(Boolean,      nullable=True)
    
    def __repr__(self):
        return f"<EmployeeEmergencyContact(EmployeeEmergencyContactId={self.EmployeeEmergencyContactId}, EmployeeId={self.EmployeeId}, Name='{self.Name}')>"