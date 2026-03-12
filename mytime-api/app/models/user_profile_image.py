from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from app.core.database import Base

class UserProfileImage(Base):
    __tablename__ = "UserProfileImage"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserId = Column(Integer, nullable=True)
    FileId = Column(String(500), nullable=True)
    FileName = Column(String(500), nullable=True)
    BucketId = Column(String(500), nullable=True)
    ContentLength = Column(BigInteger, nullable=True)
    ContentType = Column(String(200), nullable=True)
    FileInfo = Column(Text, nullable=True)
    UploadTimestamp = Column(DateTime(timezone=True), nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    CreatedBy = Column(Integer, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    ModifiedBy = Column(Integer, nullable=True)
    IsActive = Column(Boolean, default=True)

    def __repr__(self):
        return f"<UserProfileImage(Id={self.Id}, UserId={self.UserId}, FileName='{self.FileName}')>"