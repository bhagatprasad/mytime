from sqlalchemy import Column, BigInteger, Numeric, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class TutionFee(Base):
    __tablename__ = "TutionFee"

    Id = Column(BigInteger, primary_key=True, index=True)
    EmployeeId = Column(BigInteger, nullable=True)

    ActualFee = Column(Numeric(18, 2), nullable=True)
    FinalFee = Column(Numeric(18, 2), nullable=True)
    RemaingFee = Column(Numeric(18, 2), nullable=True)
    PaidFee = Column(Numeric(18, 2), nullable=True)

    # Common fields from Common base class
    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())
    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())
    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<TutionFee(Id={self.Id}, EmployeeId={self.EmployeeId}, "
            f"ActualFee={self.ActualFee}, FinalFee={self.FinalFee})>"
        )
