from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Project(Base):
    __tablename__ = "Project"  # Match your SQL Server table name
    
    ProjectId = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255), nullable=True)
    CreatedBy = Column(Integer, nullable=True)
    CreatedOn = Column(DateTime,   nullable=True)
    ModifiedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime,   nullable=True)
    IsActive = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Project(ProjectId={self.ProjectId}, Name='{self.Name}')>"