from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Text
from app.core.database import Base


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


    