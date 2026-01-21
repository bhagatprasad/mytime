from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "User"  # Match your SQL Server table name
    
    Id = Column(Integer, primary_key=True, index=True)
    EmployeeId = Column(Integer, nullable=True)
    FirstName = Column(String(max), nullable=True)
    LastName = Column(String(max), nullable=True)
    Email = Column(String(max), nullable=True)
    Phone = Column(String(max), nullable=True)
    DepartmentId = Column(Integer, nullable=True)
    RoleId = Column(Integer, nullable=True)
    PasswordHash = Column(String(max), nullable=True)
    PasswordSalt = Column(String(max), nullable=True)
    PasswordlastChangedOn = Column(DateTime, server_default=func.now())
    PasswordLastChangedBY = Column(Integer, nullable=True)
    UserWorngPasswordCount = Column(Integer, nullable=True)
    UserLastWrongPasswordOn = Column(DateTime, server_default=func.now())
    IsBlocked = Column(Boolean, default=True)
    IsActive = Column(Boolean, default=True)
    CreatedBy = Column(Integer, nullable=True)
    CreatedOn = Column(DateTime, server_default=func.now())
    ModifiedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<User(Id={self.Id}, FirstName='{self.FirstName}', LastName='{self.LastName}', Email='{self.Email}')>"