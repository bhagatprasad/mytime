from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Text
from app.core.database import Base


# ---------------------------------------------------------
# Leave Types
# ---------------------------------------------------------

class LeaveType(Base):

    __tablename__ = "LeaveTypes"

    Id = Column(Integer, primary_key=True, index=True)

    Name = Column(String(100), nullable=False)

    MaxDaysPerYear = Column(Integer)

    Description = Column(String(300))

    CreatedBy = Column(BigInteger)

    CreatedOn = Column(DateTime, default=datetime.utcnow)

    ModifiedBy = Column(BigInteger)

    ModifiedOn = Column(DateTime)

    IsActive = Column(Boolean, default=True)


# ---------------------------------------------------------
# Leave Requests
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Leave Attachments
# ---------------------------------------------------------

class LeaveAttachment(Base):

    __tablename__ = "LeaveAttachments"

    Id = Column(BigInteger, primary_key=True, index=True)

    LeaveRequestId = Column(BigInteger, nullable=False)

    FileName = Column(String(200))

    FilePath = Column(String(500))

    FileType = Column(String(50))

    CreatedBy = Column(BigInteger)

    CreatedOn = Column(DateTime, default=datetime.utcnow)

    ModifiedBy = Column(BigInteger)

    ModifiedOn = Column(DateTime)

    IsActive = Column(Boolean, default=True)


# ---------------------------------------------------------
# Leave History
# ---------------------------------------------------------

class LeaveHistory(Base):

    __tablename__ = "LeaveHistory"

    Id = Column(BigInteger, primary_key=True, index=True)

    LeaveRequestId = Column(BigInteger)

    OldStatus = Column(String(20))

    NewStatus = Column(String(20))

    Comment = Column(String(500))

    ChangedBy = Column(BigInteger)

    ChangedOn = Column(DateTime, default=datetime.utcnow)

    CreatedBy = Column(BigInteger)

    CreatedOn = Column(DateTime, default=datetime.utcnow)

    ModifiedBy = Column(BigInteger)

    ModifiedOn = Column(DateTime)

    IsActive = Column(Boolean, default=True)


    