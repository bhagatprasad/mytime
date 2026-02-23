from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class MonthlySalaryBase(BaseModel):
    """Base schema with common fields"""
    Title: Optional[str] = Field(None, max_length=200)
    SalaryMonth: Optional[str] = Field(None, max_length=20)
    SalaryYear: Optional[str] = Field(None, max_length=4)
    Location: Optional[str] = Field(None, max_length=200)
    StdDays: Optional[int] = Field(None, ge=0, le=31)
    WrkDays: Optional[int] = Field(None, ge=0, le=31)
    LopDays: Optional[int] = Field(None, ge=0, le=31)
    IsActive: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class MonthlySalaryCreate(MonthlySalaryBase):
    """Schema for creating a new monthly salary"""
    CreatedBy: Optional[int] = Field(None, ge=1)
    Title: str = Field(..., max_length=200, min_length=1)
    SalaryMonth: str = Field(..., max_length=20, min_length=1)
    SalaryYear: str = Field(..., max_length=4, min_length=4)


class MonthlySalaryUpdate(BaseModel):
    """Schema for updating an existing monthly salary"""
    Title: Optional[str] = Field(None, max_length=200, min_length=1)
    SalaryMonth: Optional[str] = Field(None, max_length=20, min_length=1)
    SalaryYear: Optional[str] = Field(None, max_length=4, min_length=4)
    Location: Optional[str] = Field(None, max_length=200)
    StdDays: Optional[int] = Field(None, ge=0, le=31)
    WrkDays: Optional[int] = Field(None, ge=0, le=31)
    LopDays: Optional[int] = Field(None, ge=0, le=31)
    IsActive: Optional[bool] = None
    ModifiedBy: Optional[int] = Field(None, ge=1)

    model_config = ConfigDict(from_attributes=True)


class MonthlySalaryResponse(MonthlySalaryBase):
    """Schema for single monthly salary response"""
    MonthlySalaryId: int
    Title: Optional[str] = None
    SalaryMonth: Optional[str] = None
    SalaryYear: Optional[str] = None
    Location: Optional[str] = None
    StdDays: Optional[int] = None
    WrkDays: Optional[int] = None
    LopDays: Optional[int] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class MonthlySalaryListResponse(BaseModel):
    """Schema for listing multiple monthly salaries with pagination"""
    total: int = Field(..., ge=0)
    items: List[MonthlySalaryResponse]
    page: int = Field(..., ge=1)
    size: int = Field(..., ge=1, le=100)
    pages: int = Field(..., ge=0)

    model_config = ConfigDict(from_attributes=True)


class MonthlySalaryExistsResponse(BaseModel):
    """Response for monthly salary existence check"""
    exists: bool

    model_config = ConfigDict(from_attributes=True)


class MonthlySalaryDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Monthly salary record deleted successfully"
    monthly_salary_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class MonthlySalaryPublishResponse(BaseModel):
    """Response for publish operation"""
    success: bool
    message: str
    monthly_salary_id: Optional[int] = None
    employees_processed: Optional[int] = Field(None, ge=0)

    model_config = ConfigDict(from_attributes=True)


# ──────────────────────────────────────────────────────────────────────
# NEW — Employee salary nested inside monthly salary responses
# ──────────────────────────────────────────────────────────────────────
class EmployeeSalaryNestedResponse(BaseModel):
    """Employee salary schema for nesting inside monthly salary responses"""
    EmployeeSalaryId: int
    EmployeeId: Optional[int] = None
    MonthlySalaryId: Optional[int] = None
    Title: Optional[str] = None
    SalaryMonth: Optional[str] = None
    SalaryYear: Optional[str] = None
    LOCATION: Optional[str] = None
    STDDAYS: Optional[int] = None
    WRKDAYS: Optional[int] = None
    LOPDAYS: Optional[int] = None
    Earning_Monthly_Basic: Optional[float] = None
    Earning_YTD_Basic: Optional[float] = None
    Earning_Montly_HRA: Optional[float] = None
    Earning_YTD_HRA: Optional[float] = None
    Earning_Montly_CONVEYANCE: Optional[float] = None
    Earning_YTD_CONVEYANCE: Optional[float] = None
    Earning_Montly_MEDICALALLOWANCE: Optional[float] = None
    Earning_YTD_MEDICALALLOWANCE: Optional[float] = None
    Earning_Montly_SPECIALALLOWANCE: Optional[float] = None
    Earning_YTD_SPECIALALLOWANCE: Optional[float] = None
    Earning_Montly_SPECIALBONUS: Optional[float] = None
    Earning_YTD_SPECIALBONUS: Optional[float] = None
    Earning_Montly_STATUTORYBONUS: Optional[float] = None
    Earning_YTD_STATUTORYBONUS: Optional[float] = None
    Earning_Montly_GROSSEARNINGS: Optional[float] = None
    Earning_YTD_GROSSEARNINGS: Optional[float] = None
    Earning_Montly_OTHERS: Optional[float] = None
    Earning_YTD_OTHERS: Optional[float] = None
    Deduction_Montly_PROFESSIONALTAX: Optional[float] = None
    Deduction_YTD_PROFESSIONALTAX: Optional[float] = None
    Deduction_Montly_ProvidentFund: Optional[float] = None
    Deduction_YTD_ProvidentFund: Optional[float] = None
    Deduction_Montly_GroupHealthInsurance: Optional[float] = None
    Deduction_YTD_GroupHealthInsurance: Optional[float] = None
    Deduction_Montly_OTHERS: Optional[float] = None
    Deduction_YTD_OTHERS: Optional[float] = None
    Deduction_Montly_GROSSSDeduction: Optional[float] = None
    Deduction_YTD_GROSSSDeduction: Optional[float] = None
    NETPAY: Optional[float] = None
    NETTRANSFER: Optional[float] = None
    INWords: Optional[str] = None
    IsActive: Optional[bool] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ──────────────────────────────────────────────────────────────────────
# NEW — Single monthly salary with its nested employee salaries
# ──────────────────────────────────────────────────────────────────────
class MonthlySalaryWithEmployees(BaseModel):
    """Single monthly salary response with nested employee salaries"""
    MonthlySalaryId: int
    Title: Optional[str] = None
    SalaryMonth: Optional[str] = None
    SalaryYear: Optional[str] = None
    Location: Optional[str] = None
    StdDays: Optional[int] = None
    WrkDays: Optional[int] = None
    LopDays: Optional[int] = None
    IsActive: Optional[bool] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    employee_salaries: List[EmployeeSalaryNestedResponse] = []   # ← nested list
    total_employees: int = 0                                      # ← convenience count

    model_config = ConfigDict(from_attributes=True)


# ──────────────────────────────────────────────────────────────────────
# NEW — Paginated list of monthly salaries each with employee salaries
# ──────────────────────────────────────────────────────────────────────
class MonthlySalaryWithEmployeesListResponse(BaseModel):
    """Paginated list response of monthly salaries with nested employee salaries"""
    total: int = Field(..., ge=0)
    items: List[MonthlySalaryWithEmployees]

    model_config = ConfigDict(from_attributes=True)