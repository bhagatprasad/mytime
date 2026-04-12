from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Text
from app.core.database import Base

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
