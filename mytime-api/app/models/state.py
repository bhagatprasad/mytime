from sqlalchemy import Column, BigInteger, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class State(Base):
    __tablename__ = "State"

    StateId = Column(BigInteger, primary_key=True, index=True)
    CountryId = Column(BigInteger, nullable=False)

    Name = Column(Text, nullable=False)
    Description = Column(Text, nullable=True)
    StateCode = Column(Text, nullable=True)
    CountryCode = Column(Text, nullable=True)

    # Common fields from Common base class
    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<State(StateId={self.StateId}, Name='{self.Name}', "
            f"StateCode='{self.StateCode}', CountryCode='{self.CountryCode}')>"
        )
