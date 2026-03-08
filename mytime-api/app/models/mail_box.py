from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class MailBox(Base):
    __tablename__ = "MailBox"

    MailBoxId = Column(BigInteger, primary_key=True, index=True)

    MessageTypeId = Column(BigInteger, ForeignKey("MessageType.Id"), nullable=True)

    Title = Column(Text, nullable=True)
    Subject = Column(Text, nullable=True)
    Description = Column(Text, nullable=True)
    Message = Column(Text, nullable=True)
    HTMLMessage = Column(Text, nullable=True)

    IsForAll = Column(Boolean, default=False)

    FromUser = Column(Text, nullable=True)
    ToUser = Column(Text, nullable=True)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime,   nullable=True)

    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime,   nullable=True)

    IsActive = Column(Boolean, nullable=True)

    # Relationship to MessageType
    message_type = relationship("MessageType", backref="mailboxes")

    def __repr__(self):
        return (
            f"<MailBox(MailBoxId={self.MailBoxId}, "
            f"Title='{self.Title}', Subject='{self.Subject}')>"
        )
