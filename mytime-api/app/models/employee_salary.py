from sqlalchemy import (
    Column, Integer, Boolean, DateTime, Text,
    BigInteger, Numeric
)
from sqlalchemy.sql import func
from app.core.database import Base


class EmployeeSalary(Base):
    __tablename__ = "EmployeeSalary"

    EmployeeSalaryId = Column(BigInteger, primary_key=True, index=True)
    EmployeeId = Column(BigInteger, nullable=True)
    MonthlySalaryId = Column(BigInteger, nullable=True)

    Title = Column(Text, nullable=True)
    SalaryMonth = Column(Text, nullable=True)
    SalaryYear = Column(Text, nullable=True)

    LOCATION = Column(Text, nullable=True)

    STDDAYS = Column(Integer, nullable=True)
    WRKDAYS = Column(Integer, nullable=True)
    LOPDAYS = Column(Integer, nullable=True)

    # ===== Earnings (Monthly / YTD) =====
    Earning_Monthly_Basic = Column(Numeric(18, 2), nullable=True)
    Earning_YTD_Basic = Column(Numeric(18, 2), nullable=True)

    Earning_Montly_HRA = Column(Numeric(18, 2), nullable=True)
    Earning_YTD_HRA = Column(Numeric(18, 2), nullable=True)

    Earning_Montly_CONVEYANCE = Column(Numeric(18, 2), nullable=True)
    Earning_YTD_CONVEYANCE = Column(Numeric(18, 2), nullable=True)

    Earning_Montly_MEDICALALLOWANCE = Column(Numeric(18, 2), nullable=True)
    Earning_YTD_MEDICALALLOWANCE = Column(Numeric(18, 2), nullable=True)

    Earning_Montly_SPECIALALLOWANCE = Column(Numeric(18, 2), nullable=True)
    Earning_YTD_SPECIALALLOWANCE = Column(Numeric(18, 2), nullable=True)

    Earning_Montly_SPECIALBONUS = Column(Numeric(18, 2), nullable=True)
    Earning_YTD_SPECIALBONUS = Column(Numeric(18, 2), nullable=True)

    Earning_Montly_STATUTORYBONUS = Column(Numeric(18, 2), nullable=True)
    Earning_YTD_STATUTORYBONUS = Column(Numeric(18, 2), nullable=True)

    Earning_Montly_GROSSEARNINGS = Column(Numeric(18, 2), nullable=True)
    Earning_YTD_GROSSEARNINGS = Column(Numeric(18, 2), nullable=True)

    Earning_Montly_OTHERS = Column(Numeric(18, 2), nullable=True)
    Earning_YTD_OTHERS = Column(Numeric(18, 2), nullable=True)

    # ===== Deductions (Monthly / YTD) =====
    Deduction_Montly_PROFESSIONALTAX = Column(Numeric(18, 2), nullable=True)
    Deduction_YTD_PROFESSIONALTAX = Column(Numeric(18, 2), nullable=True)

    Deduction_Montly_ProvidentFund = Column(Numeric(18, 2), nullable=True)
    Deduction_YTD_ProvidentFund = Column(Numeric(18, 2), nullable=True)

    Deduction_Montly_GroupHealthInsurance = Column(Numeric(18, 2), nullable=True)
    Deduction_YTD_GroupHealthInsurance = Column(Numeric(18, 2), nullable=True)

    Deduction_Montly_OTHERS = Column(Numeric(18, 2), nullable=True)
    Deduction_YTD_OTHERS = Column(Numeric(18, 2), nullable=True)

    Deduction_Montly_GROSSSDeduction = Column(Numeric(18, 2), nullable=True)
    Deduction_YTD_GROSSSDeduction = Column(Numeric(18, 2), nullable=True)

    # ===== Net Pay =====
    NETPAY = Column(Numeric(18, 2), nullable=True)
    NETTRANSFER = Column(Numeric(18, 2), nullable=True)

    INWords = Column(Text, nullable=True)

    # ===== Audit =====
    CreatedOn = Column(DateTime,   nullable=True)
    CreatedBy = Column(BigInteger, nullable=True)

    ModifiedOn = Column(DateTime,   nullable=True)
    ModifiedBy = Column(BigInteger, nullable=True)

    IsActive = Column(Boolean, nullable=True)

    def __repr__(self):
        return (
            f"<EmployeeSalary("
            f"EmployeeSalaryId={self.EmployeeSalaryId}, "
            f"EmployeeId={self.EmployeeId}, "
            f"SalaryMonth={self.SalaryMonth}, "
            f"SalaryYear={self.SalaryYear})>"
        )
