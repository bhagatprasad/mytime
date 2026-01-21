from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Role(Base):
    __tablename__ = "Roles"  # Match your SQL Server table name
    
    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255), nullable=True)
    Code = Column(String(100), nullable=True)
    IsActive = Column(Boolean, default=True)
    CreatedBy = Column(Integer, nullable=True)
    CreatedOn = Column(DateTime, server_default=func.now())
    ModifiedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<Role(Id={self.Id}, Name='{self.Name}', Code='{self.Code}')>"