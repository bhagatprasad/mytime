from sqlalchemy import (
    Column, Boolean, DateTime, Text,
    BigInteger, Numeric
)
from sqlalchemy.sql import func
from app.core.database import Base


class EmployeeSalaryStructure(Base):
    __tablename__ = "EmployeeSalaryStructure"

    EmployeeSalaryStructureId = Column(BigInteger, primary_key=True, index=True)
    EmployeeId = Column(BigInteger, nullable=True)

    PAN = Column(Text, nullable=True)
    Adhar = Column(Text, nullable=True)
    BankAccount = Column(Text, nullable=True)
    BankName = Column(Text, nullable=True)
    IFSC = Column(Text, nullable=True)

    BASIC = Column(Numeric(18, 2), nullable=True)
    HRA = Column(Numeric(18, 2), nullable=True)
    CONVEYANCE = Column(Numeric(18, 2), nullable=True)
    MEDICALALLOWANCE = Column(Numeric(18, 2), nullable=True)
    SPECIALALLOWANCE = Column(Numeric(18, 2), nullable=True)
    SPECIALBONUS = Column(Numeric(18, 2), nullable=True)
    STATUTORYBONUS = Column(Numeric(18, 2), nullable=True)
    OTHERS = Column(Numeric(18, 2), nullable=True)

    UAN = Column(Text, nullable=True)
    PFNO = Column(Text, nullable=True)

    PF = Column(Numeric(18, 2), nullable=True)
    ESIC = Column(Numeric(18, 2), nullable=True)
    PROFESSIONALTAX = Column(Numeric(18, 2), nullable=True)
    GroupHealthInsurance = Column(Numeric(18, 2), nullable=True)

    GROSSEARNINGS = Column(Numeric(18, 2), nullable=True)
    GROSSDEDUCTIONS = Column(Numeric(18, 2), nullable=True)

    CreatedBy = Column(BigInteger, nullable=True)
    CreatedOn = Column(DateTime(timezone=True), server_default=func.now())

    ModifiedBy = Column(BigInteger, nullable=True)
    ModifiedOn = Column(DateTime(timezone=True), onupdate=func.now())

    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<EmployeeSalaryStructure("
            f"EmployeeSalaryStructureId={self.EmployeeSalaryStructureId}, "
            f"EmployeeId={self.EmployeeId}, "
            f"PAN='{self.PAN}')>"
        )
