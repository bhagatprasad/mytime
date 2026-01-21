from sqlalchemy import Boolean, Column, DateTime, Text, BigInteger, func
from app.core.database import Base


class Designation(Base):
    __tablename__ = "Designation"

    DesignationId = Column(BigInteger, primary_key=True, index=True)

    Name = Column(Text, nullable=True)
    Code = Column(Text, nullable=True)

    # Common fields (from Common base class)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    CreatedBy = Column(BigInteger, nullable=True)

    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<Designation("
            f"DesignationId={self.Id}, "
            f"Name='{self.Name}', "
            f"Code='{self.Code}')>"
        )
