from sqlalchemy import Column, BigInteger, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class MessageType(Base):
    __tablename__ = "MessageType"

    Id = Column(BigInteger, primary_key=True, index=True)
    Name = Column(Text, nullable=False)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime,   nullable=True)

    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime,   nullable=True)

    IsActive = Column(Boolean, default=True)

    # Relationship to MailBox (one-to-many)
    mailboxes = relationship("MailBox", back_populates="message_type")

    def __repr__(self):
        return f"<MessageType(Id={self.Id}, Name='{self.Name}')>"
