from sqlalchemy import Column, BigInteger, Boolean, DateTime, String
from sqlalchemy.sql import func
from app.core.database import Base


class EmployeeAddress(Base):
    __tablename__ = "EmployeeAddress"
    
    EmployeeAddressId = Column(BigInteger, primary_key=True, index=True)
    EmployeeId = Column(BigInteger, nullable=True)
    HNo = Column(String, nullable=True)  # Use String for varchar(max)
    AddressLineOne = Column(String, nullable=True)
    AddressLineTwo = Column(String, nullable=True)
    Landmark = Column(String, nullable=True)
    CityId = Column(BigInteger, nullable=True)  # Changed to BigInteger
    StateId = Column(BigInteger, nullable=True)  # Changed to BigInteger
    CountryId = Column(BigInteger, nullable=True)  # Changed to BigInteger
    Zipcode = Column(String, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    CreatedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)
    IsActive = Column(Boolean, nullable=True, default=True)
    
    def __repr__(self):
        return f"<EmployeeAddress(EmployeeAddressId={self.EmployeeAddressId}, EmployeeId={self.EmployeeId}, HNo='{self.HNo}')>"