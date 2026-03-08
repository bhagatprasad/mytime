from sqlalchemy import Boolean, Column, DateTime, Text, BigInteger, func
from app.core.database import Base


class Country(Base):
    __tablename__ = "Country"

    Id = Column(BigInteger, primary_key=True, index=True)

    Name = Column(Text, nullable=True)
    Code = Column(Text, nullable=True)
    CreatedOn = Column(DateTime,   nullable=True)
    CreatedBy = Column(BigInteger, nullable=True)

    ModifiedOn = Column(DateTime,   nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<Country("
            f"Id={self.Id}, "
            f"Name='{self.Name}', "
            f"Code='{self.Code}')>"
        )
