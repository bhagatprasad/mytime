from sqlalchemy import Column, Integer, Boolean, DateTime, Text, BigInteger, Numeric
from sqlalchemy.sql import func
from app.core.database import Base


class EmployeePayment(Base):
    __tablename__ = "EmployeePayment"

    Id = Column(BigInteger, primary_key=True, index=True)

    EmployeeId = Column(BigInteger, nullable=True)
    TutionFeeId = Column(BigInteger, nullable=True)
    PaymentMethodId = Column(BigInteger, nullable=True)
    PaymentTypeId = Column(BigInteger, nullable=True)

    Amount = Column(Numeric(18, 2), nullable=True)
    PaymentMessage = Column(Text, nullable=True)

    # Common fields (from Common base class)
    CreatedOn = Column(DateTime,   nullable=True)
    CreatedBy = Column(BigInteger, nullable=True)

    ModifiedOn = Column(DateTime,   nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<EmployeePayment("
            f"Id={self.Id}, "
            f"EmployeeId={self.EmployeeId}, "
            f"Amount={self.Amount})>"
        )
