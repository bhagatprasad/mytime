# models/leave_balance_model.py

from sqlalchemy import Column, BigInteger, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class LeaveBalance(Base):
    __tablename__ = "LeaveBalance"

    Id = Column(BigInteger, primary_key=True, index=True)
    UserId = Column(BigInteger, ForeignKey("User.Id"), nullable=False)
    LeaveTypeId = Column(Integer, ForeignKey("LeaveType.Id"), nullable=False)
    Year = Column(Integer, nullable=False)

    TotalLeaves = Column(Integer, nullable=False)
    UsedLeaves = Column(Integer, default=0)
    RemainingLeaves = Column(Integer, nullable=False)

    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    CreatedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, default=True)