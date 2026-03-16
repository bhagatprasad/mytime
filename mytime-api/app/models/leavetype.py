# from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
# from sqlalchemy.sql import func
# from app.core.database import Base

# class LeaveType(Base):
#     __tablename__ = "[olc_db_usr].[LeaveType]"  # Match your SQL Server table name
    
#     Id = Column(Integer, primary_key=True, index=True)
#     Name = Column(String(255), nullable=True)
#     MaxDaysPerYear=Column(Integer,nullable=True)
#     Description=Column(Text,nullable=True)
#     CreatedBy = Column(Integer, nullable=True)
#     CreatedOn = Column(DateTime,   nullable=True)
#     ModifiedBy = Column(Integer, nullable=True)
#     ModifiedOn = Column(DateTime,   nullable=True)
#     IsActive = Column(Boolean, default=True)
    
#     def __repr__(self):
#         return f"<LeaveType(Id={self.Id}, Name='{self.Name}', MaxDaysPerYear='{self.MaxDaysPerYear}',Description='{self.Description}')>"

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from app.core.database import Base

class LeaveType(Base):
    __tablename__ = "LeaveType"
    __table_args__ = {"schema": "olc_db_usr"}

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255), nullable=True)
    MaxDaysPerYear = Column(Integer, nullable=True)
    Description = Column(Text, nullable=True)
    CreatedBy = Column(Integer, nullable=True)
    CreatedOn = Column(DateTime, nullable=True)
    ModifiedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime, nullable=True)
    IsActive = Column(Boolean, default=True)

    def __repr__(self):
        return f"<LeaveType(Id={self.Id}, Name='{self.Name}', MaxDaysPerYear='{self.MaxDaysPerYear}', Description='{self.Description}')>"