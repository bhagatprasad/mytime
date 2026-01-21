from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Employee(Base):
    __tablename__ = "Employee"  # Match your SQL Server table name
    
    EmployeeId = Column(Integer, primary_key=True, index=True)
    EmployeeCode = Column(String(max), nullable=True)
    FirstName = Column(String(max), nullable=True)
    LastName = Column(String(max), nullable=True)
    FatherName = Column(String(max), nullable=True)
    MotherName = Column(String(max), nullable=True)
    Gender = Column(String(max), nullable=True)
    DateOfBirth = Column(DateTime(timezone=True), nullable=True)
    Email = Column(String(max), nullable=True)
    Phone = Column(String(max), nullable=True)
    UserId = Column(Integer, nullable=True)
    RoleId = Column(Integer, nullable=True)
    DepartmentId = Column(Integer, nullable=True)
    DesignationId = Column(Integer, nullable=True)
    StartedOn = Column(DateTime(timezone=True), nullable=True)
    EndedOn = Column(DateTime(timezone=True), nullable=True)
    ResignedOn = Column(DateTime(timezone=True), nullable=True)
    LastWorkingDay = Column(DateTime(timezone=True), nullable=True)
    OfferReleasedOn = Column(DateTime(timezone=True), nullable=True)  # Corrected typo from "OfferRelesedOn"
    OfferAcceptedOn = Column(DateTime(timezone=True), nullable=True)
    OfferPrice = Column(Numeric(precision=18, scale=2), nullable=True)  # Assuming decimal for currency
    CurrentPrice = Column(Numeric(precision=18, scale=2), nullable=True)
    JoiningBonus = Column(Numeric(precision=18, scale=2), nullable=True)
    CreatedBy = Column(Integer, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    ModifiedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    IsActive = Column(Boolean, nullable=True)
    
    def __repr__(self):
        return f"<Employee(EmployeeId={self.EmployeeId}, EmployeeCode='{self.EmployeeCode}', FirstName='{self.FirstName}', LastName='{self.LastName}')>"