from sqlalchemy import Column, BigInteger, Boolean, DateTime, Text, String
from sqlalchemy.sql import func
from app.core.database import Base


class EmployeeEmployment(Base):
    __tablename__ = "EmployeeEmployment"

    EmployeeEmploymentId = Column(BigInteger, primary_key=True, index=True)
    EmployeeId = Column(BigInteger, nullable=True)

    CompanyName = Column(String, nullable=True)  # Changed from Text to String
    Address = Column(String, nullable=True)      # Changed from Text to String
    Designation = Column(String, nullable=True)  # Changed from Text to String

    StartedOn = Column(DateTime,   nullable=True)
    EndedOn = Column(DateTime,   nullable=True)

    Reason = Column(String, nullable=True)           # Changed from Text to String
    ReportingManager = Column(String, nullable=True) # Changed from Text to String
    HREmail = Column(String, nullable=True)          # Changed from Text to String
    Referance = Column(String, nullable=True)        # NOTE: Spelled as "Referance" to match SQL table

    CreatedOn = Column(DateTime,   nullable=True)
    CreatedBy = Column(BigInteger, nullable=True)

    ModifiedOn = Column(DateTime,   nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, nullable=True, default=True)

    def __repr__(self):
        return (
            f"<EmployeeEmployment("
            f"EmployeeEmploymentId={self.EmployeeEmploymentId}, "
            f"EmployeeId={self.EmployeeId}, "
            f"CompanyName='{self.CompanyName}')>"
        )