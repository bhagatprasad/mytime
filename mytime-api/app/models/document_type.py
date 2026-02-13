from sqlalchemy import Boolean, Column, DateTime, Text, BigInteger, func
from app.core.database import Base


class DocumentType(Base):
    __tablename__ = "DocumentType"

    Id = Column(BigInteger, primary_key=True, index=True)
    Name = Column(Text, nullable=True)
    CreatedOn = Column(DateTime,nullable=True)
    CreatedBy = Column(BigInteger, nullable=True)

    ModifiedOn = Column(DateTime,nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<DocumentType("
            f"Id={self.Id}, "
            f"Name='{self.Name}')>"
        )
