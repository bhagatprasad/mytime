from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class EmployeeAddress(Base):
    __tablename__ = "EmployeeAddress"  # Match your SQL Server table name
    
    EmployeeAddressId = Column(Integer, primary_key=True, index=True)
    EmployeeId = Column(Integer, nullable=True)
    HNo = Column(String(max), nullable=True)
    AddressLineOne = Column(String(max), nullable=True)
    AddressLineTwo = Column(String(max), nullable=True)
    Landmark = Column(String(max), nullable=True)
    CityId = Column(Integer, nullable=True)
    StateId = Column(Integer, nullable=True)
    CountryId = Column(Integer, nullable=True)
    Zipcode = Column(String(max), nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    CreatedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    ModifiedBy = Column(Integer, nullable=True)
    IsActive = Column(Boolean, nullable=True)
    
    def __repr__(self):
        return f"<EmployeeAddress(EmployeeAddressId={self.EmployeeAddressId}, EmployeeId={self.EmployeeId}, HNo='{self.HNo}')>"