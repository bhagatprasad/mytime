from sqlalchemy import Column, Integer, Boolean, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from app.core.database import Base


class HolidayCallender(Base):
    __tablename__ = "HolidayCallender"

    Id = Column(BigInteger, primary_key=True, index=True)

    FestivalName = Column(Text, nullable=True)
    HolidayDate = Column(DateTime(timezone=True), nullable=True)
    Year = Column(Integer, nullable=True)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())

    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())

    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<HolidayCallender("
            f"Id={self.Id}, "
            f"FestivalName='{self.FestivalName}', "
            f"Year={self.Year})>"
        )
