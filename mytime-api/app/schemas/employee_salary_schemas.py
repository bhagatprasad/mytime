from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional

class EmployeeSalaryBase(BaseModel):
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

class EmployeeSalaryCreate(EmployeeSalaryBase):
    pass

class EmployeeSalaryUpdate(EmployeeSalaryBase):
    pass

class EmployeeSalaryInDB(EmployeeSalaryBase):
    EmployeeSalaryId: int
    CreatedOn: Optional[datetime] = None
    CreatedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None

    class Config:
        from_attributes = True 

class EmployeeSalaryInDB(BaseModel):
    """Employee salary schema for nested response"""
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
    CreatedOn: Optional[datetime] = None
    CreatedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class MonthlySalaryWithEmployees(BaseModel):
    """Monthly salary with its nested employee salaries"""
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
    employee_salaries: List[EmployeeSalaryInDB] = [] 
    total_employees: int = 0                                   # ← convenience count

    model_config = ConfigDict(from_attributes=True)


class MonthlySalaryWithEmployeesListResponse(BaseModel):
    """Paginated list of monthly salaries each with their employee salaries"""
    total: int = Field(..., ge=0)
    items: List[MonthlySalaryWithEmployees]

    model_config = ConfigDict(from_attributes=True)

class EmployeeSalaryBulkCreate(BaseModel):
    """Schema for bulk inserting employee salaries"""
    salaries: List[EmployeeSalaryCreate]

    model_config = ConfigDict(from_attributes=True)

class EmployeeSalaryBulkResponse(BaseModel):
    """Response schema for bulk insert"""
    total_created: int
    salaries: List[EmployeeSalaryInDB]

    model_config = ConfigDict(from_attributes=True)