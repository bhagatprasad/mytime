from sqlalchemy import Column, BigInteger, Text, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class MonthlySalary(Base):
    __tablename__ = "MonthlySalary"

    MonthlySalaryId = Column(BigInteger, primary_key=True, index=True)

    Title = Column(Text, nullable=True)
    SalaryMonth = Column(Text, nullable=True)
    SalaryYear = Column(Text, nullable=True)
    Location = Column(Text, nullable=True)

    StdDays = Column(Integer, nullable=True)
    WrkDays = Column(Integer, nullable=True)
    LopDays = Column(Integer, nullable=True)

    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    CreatedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)
    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<MonthlySalary(MonthlySalaryId={self.MonthlySalaryId}, "
            f"Title='{self.Title}', SalaryMonth='{self.SalaryMonth}', SalaryYear='{self.SalaryYear}')>"
        )
