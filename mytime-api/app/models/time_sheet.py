from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from app.core.database import Base


class Timesheet(Base):
    __tablename__ = "Timesheet"

    Id = Column(BigInteger, primary_key=True, index=True)

    FromDate = Column(DateTime(timezone=True), nullable=True)
    ToDate = Column(DateTime(timezone=True), nullable=True)
    Description = Column(Text, nullable=True)

    EmployeeId = Column(BigInteger, nullable=True)
    UserId = Column(BigInteger, nullable=True)
    Status = Column(Text, nullable=True)

    AssignedOn = Column(DateTime(timezone=True), nullable=True)
    AssignedTo = Column(BigInteger, nullable=True)

    ApprovedOn = Column(DateTime(timezone=True), nullable=True)
    ApprovedBy = Column(BigInteger, nullable=True)
    ApprovedComments = Column(Text, nullable=True)

    CancelledOn = Column(DateTime(timezone=True), nullable=True)
    CancelledBy = Column(BigInteger, nullable=True)
    CancelledComments = Column(Text, nullable=True)

    RejectedOn = Column(DateTime(timezone=True), nullable=True)
    RejectedBy = Column(BigInteger, nullable=True)
    RejectedComments = Column(Text, nullable=True)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())

    IsActive = Column(Boolean, nullable=True)

    # One-to-many relationship to TimesheetTask
    timesheet_tasks = relationship("TimesheetTask", back_populates="timesheet")

    def __repr__(self):
        return f"<Timesheet(Id={self.Id}, Status='{self.Status}', EmployeeId={self.EmployeeId})>"
