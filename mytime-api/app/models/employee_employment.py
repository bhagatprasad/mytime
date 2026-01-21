from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from app.core.database import Base


class EmployeeEmployment(Base):
    __tablename__ = "EmployeeEmployment"

    EmployeeEmploymentId = Column(BigInteger, primary_key=True, index=True)
    EmployeeId = Column(BigInteger, nullable=True)

    CompanyName = Column(Text, nullable=True)
    Address = Column(Text, nullable=True)
    Designation = Column(Text, nullable=True)

    StartedOn = Column(DateTime(timezone=True), nullable=True)
    EndedOn = Column(DateTime(timezone=True), nullable=True)

    Reason = Column(Text, nullable=True)
    ReportingManager = Column(Text, nullable=True)
    HREmail = Column(Text, nullable=True)
    Reference = Column(Text, nullable=True)

    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    CreatedBy = Column(BigInteger, nullable=True)

    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<EmployeeEmployment("
            f"EmployeeEmploymentId={self.EmployeeEmploymentId}, "
            f"EmployeeId={self.EmployeeId}, "
            f"CompanyName='{self.CompanyName}')>"
        )
