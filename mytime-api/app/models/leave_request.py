from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Text
from app.core.database import Base

class LeaveRequest(Base):

    __tablename__ = "LeaveRequests"

    Id = Column(BigInteger, primary_key=True, index=True)

    UserId = Column(BigInteger, nullable=False)

    LeaveTypeId = Column(Integer, nullable=False)

    FromDate = Column(Date, nullable=False)

    ToDate = Column(Date, nullable=False)

    TotalDays = Column(Integer)

    Reason = Column(String(300))

    Description = Column(Text)

    Status = Column(String(20), default="Pending")

    AdminComment = Column(Text)

    CancelReason = Column(Text)

    CreatedBy = Column(BigInteger)

    CreatedOn = Column(DateTime, default=datetime.utcnow)

    ModifiedBy = Column(BigInteger)

    ModifiedOn = Column(DateTime)

    IsActive = Column(Boolean, default=True)




