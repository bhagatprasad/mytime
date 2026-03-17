from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Text
from app.core.database import Base


class LeaveType(Base):
    __tablename__ = "LeaveType"

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