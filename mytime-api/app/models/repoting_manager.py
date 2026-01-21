from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class RepotingManager(Base):
    __tablename__ = "RepotingManager"  # Match your SQL Server table name
    
    RepotingManagerId = Column(Integer, primary_key=True, index=True)
    EmployeeId = Column(Integer, nullable=True)
    ManagerId = Column(Integer, nullable=True)
    IsActive = Column(Boolean, default=True)
    CreatedBy = Column(Integer, nullable=True)
    CreatedOn = Column(DateTime, server_default=func.now())
    ModifiedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<RepotingManager(RepotingManagerId={self.RepotingManagerId}, EmployeeId='{self.EmployeeId}', ManagerId='{self.ManagerId}')>"