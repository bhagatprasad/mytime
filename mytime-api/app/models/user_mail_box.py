from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class UserMailBox(Base):
    __tablename__ = "UserMailBox"

    UserMailBoxId = Column(BigInteger, primary_key=True, index=True)
    UserId = Column(BigInteger, nullable=True)
    MailBoxId = Column(BigInteger, ForeignKey("MailBox.MailBoxId"), nullable=True)

    IsRead = Column(Boolean, default=False)
    ReadOn = Column(BigInteger, nullable=True)  # assuming timestamp stored as long

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime,   nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime,   nullable=True)
    IsActive = Column(Boolean, nullable=True)

    # Relationship to MailBox
    mail_box = relationship("MailBox")

    def __repr__(self):
        return f"<UserMailBox(UserMailBoxId={self.UserMailBoxId}, UserId={self.UserId}, MailBoxId={self.MailBoxId})>"
