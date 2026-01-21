from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class NotificationType(Base):
    __tablename__ = "NotificationType"

    NotificationTypeId = Column(BigInteger, primary_key=True, index=True)
    Name = Column(Text, nullable=False)
    Description = Column(Text, nullable=True)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())

    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())

    IsActive = Column(Boolean, default=True)

    def __repr__(self):
        return f"<NotificationType(Id={self.NotificationTypeId}, Name='{self.Name}')>"
