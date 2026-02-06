from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class Employee(Base):
    __tablename__ = "Employee"
    
    EmployeeId = Column(Integer, primary_key=True, index=True)
    EmployeeCode = Column(String(100), nullable=False, unique=True)  # Changed from String(max)
    FirstName = Column(String(255), nullable=True)  # Changed from String(max)
    LastName = Column(String(255), nullable=True)   # Changed from String(max)
    FatherName = Column(String(255), nullable=True)
    MotherName = Column(String(255), nullable=True)
    Gender = Column(String(50), nullable=True)
    DateOfBirth = Column(DateTime(timezone=True), nullable=True)
    Email = Column(String(255), nullable=True)
    Phone = Column(String(50), nullable=True)
    UserId = Column(Integer, nullable=True)
    RoleId = Column(Integer, nullable=True)
    DepartmentId = Column(Integer, nullable=True)
    DesignationId = Column(Integer, nullable=True)
    StartedOn = Column(DateTime(timezone=True), nullable=True)
    EndedOn = Column(DateTime(timezone=True), nullable=True)
    ResignedOn = Column(DateTime(timezone=True), nullable=True)
    LastWorkingDay = Column(DateTime(timezone=True), nullable=True)
    OfferRelesedOn = Column(DateTime(timezone=True), nullable=True)  # Keep the typo to match DB
    OfferAcceptedOn = Column(DateTime(timezone=True), nullable=True)
    OfferPrice = Column(Numeric(precision=22, scale=11), nullable=True)  # Match DB precision
    CurrentPrice = Column(Numeric(precision=22, scale=11), nullable=True)
    JoiningBonus = Column(Numeric(precision=22, scale=11), nullable=True)
    CreatedBy = Column(Integer, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), nullable=True, default=datetime.utcnow)
    ModifiedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), nullable=True, onupdate=datetime.utcnow)
    IsActive = Column(Boolean, nullable=True, default=True)
    
    def __repr__(self):
        return f"<Employee(EmployeeId={self.EmployeeId}, EmployeeCode='{self.EmployeeCode}')>"