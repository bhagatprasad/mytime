from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class EmployeeDocument(Base):
    __tablename__ = "EmployeeDocument"  # Match your SQL Server table name
    
    Id = Column(Integer, primary_key=True, index=True)
    EmployeeId = Column(Integer, nullable=False)  # Assuming not nullable based on C# model
    DocumentTypeId = Column(Integer, nullable=False)
    DocumentName = Column(String(max), nullable=True)
    DocumentPath = Column(String(max), nullable=True)
    DocumentExtension = Column(String(max), nullable=True)
    CreatedBy = Column(Integer, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    ModifiedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    IsActive = Column(Boolean, nullable=True)
    
    def __repr__(self):
        return f"<EmployeeDocument(Id={self.Id}, EmployeeId={self.EmployeeId}, DocumentName='{self.DocumentName}')>"