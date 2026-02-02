from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Optional, List
from datetime import datetime
from decimal import Decimal


class EmployeeSalaryStructureBase(BaseModel):
    """Base schema for EmployeeSalaryStructure data"""
    EmployeeId: int = Field(..., description="Foreign key to Employee table")
    PAN: Optional[str] = Field(None, max_length=20, description="PAN number")
    Adhar: Optional[str] = Field(None, max_length=12, description="Aadhaar number")
    BankAccount: Optional[str] = Field(None, max_length=50, description="Bank account number")
    BankName: Optional[str] = Field(None, max_length=100, description="Bank name")
    IFSC: Optional[str] = Field(None, max_length=11, description="IFSC code")
    
    # Earnings
    BASIC: Decimal = Field(..., ge=0, max_digits=18, decimal_places=2, description="Basic salary")
    HRA: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="House Rent Allowance")
    CONVEYANCE: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="Conveyance allowance")
    MEDICALALLOWANCE: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="Medical allowance")
    SPECIALALLOWANCE: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="Special allowance")
    SPECIALBONUS: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="Special bonus")
    STATUTORYBONUS: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="Statutory bonus")
    OTHERS: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="Other earnings")
    
    # Provident Fund
    UAN: Optional[str] = Field(None, max_length=20, description="UAN number")
    PFNO: Optional[str] = Field(None, max_length=20, description="PF number")
    
    # Deductions
    PF: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="Provident Fund deduction")
    ESIC: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="ESIC deduction")
    PROFESSIONALTAX: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="Professional Tax")
    GroupHealthInsurance: Decimal = Field(0, ge=0, max_digits=18, decimal_places=2, description="Health insurance")


class EmployeeSalaryStructureCreate(EmployeeSalaryStructureBase):
    """Schema for creating a new EmployeeSalaryStructure"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")
    IsActive: Optional[bool] = Field(True, description="Whether the salary structure is active")


class EmployeeSalaryStructureUpdate(BaseModel):
    """Schema for updating an existing EmployeeSalaryStructure"""
    PAN: Optional[str] = Field(None, max_length=20, description="PAN number")
    Adhar: Optional[str] = Field(None, max_length=12, description="Aadhaar number")
    BankAccount: Optional[str] = Field(None, max_length=50, description="Bank account number")
    BankName: Optional[str] = Field(None, max_length=100, description="Bank name")
    IFSC: Optional[str] = Field(None, max_length=11, description="IFSC code")
    
    # Earnings
    BASIC: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Basic salary")
    HRA: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="House Rent Allowance")
    CONVEYANCE: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Conveyance allowance")
    MEDICALALLOWANCE: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Medical allowance")
    SPECIALALLOWANCE: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Special allowance")
    SPECIALBONUS: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Special bonus")
    STATUTORYBONUS: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Statutory bonus")
    OTHERS: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Other earnings")
    
    # Provident Fund
    UAN: Optional[str] = Field(None, max_length=20, description="UAN number")
    PFNO: Optional[str] = Field(None, max_length=20, description="PF number")
    
    # Deductions
    PF: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Provident Fund deduction")
    ESIC: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="ESIC deduction")
    PROFESSIONALTAX: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Professional Tax")
    GroupHealthInsurance: Optional[Decimal] = Field(None, ge=0, max_digits=18, decimal_places=2, description="Health insurance")
    
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the salary structure is active")


class EmployeeSalaryStructureResponse(BaseModel):
    """Schema for EmployeeSalaryStructure response (read operations)"""
    EmployeeSalaryStructureId: int
    EmployeeId: int
    
    # Personal details
    PAN: Optional[str] = None
    Adhar: Optional[str] = None
    BankAccount: Optional[str] = None
    BankName: Optional[str] = None
    IFSC: Optional[str] = None
    
    # Earnings
    BASIC: Decimal
    HRA: Decimal
    CONVEYANCE: Decimal
    MEDICALALLOWANCE: Decimal
    SPECIALALLOWANCE: Decimal
    SPECIALBONUS: Decimal
    STATUTORYBONUS: Decimal
    OTHERS: Decimal
    
    # Provident Fund
    UAN: Optional[str] = None
    PFNO: Optional[str] = None
    
    # Deductions
    PF: Decimal
    ESIC: Decimal
    PROFESSIONALTAX: Decimal
    GroupHealthInsurance: Decimal
    
    # Calculated fields
    GROSSEARNINGS: Optional[Decimal] = None
    GROSSDEDUCTIONS: Optional[Decimal] = None
    NETTAKEHOME: Optional[Decimal] = Field(None, description="Calculated net take-home salary")
    
    # Metadata
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class EmployeeSalaryStructureListResponse(BaseModel):
    """Schema for listing multiple EmployeeSalaryStructures with pagination"""
    total: int
    items: List[EmployeeSalaryStructureResponse]
    page: int
    size: int
    pages: int


class EmployeeSalaryStructureExistsResponse(BaseModel):
    """Response for EmployeeSalaryStructure existence check"""
    exists: bool
    employee_salary_structure_id: Optional[int] = None


class EmployeeSalaryStructureDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Employee salary structure deleted successfully"
    employee_salary_structure_id: Optional[int] = None


class EmployeeSalaryStructureWithDetailsResponse(EmployeeSalaryStructureResponse):
    """Extended response with related data"""
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None


class EmployeeSalaryStructureCreateResponse(BaseModel):
    """Response after creating a new employee salary structure"""
    success: bool
    message: str = "Employee salary structure created successfully"
    employee_salary_structure_id: int
    net_takehome: Decimal


class EmployeeSalaryStructureUpdateResponse(BaseModel):
    """Response after updating an employee salary structure"""
    success: bool
    message: str = "Employee salary structure updated successfully"
    employee_salary_structure_id: int
    modified_fields: List[str] = Field(default_factory=list)
    net_takehome: Optional[Decimal] = None


class SalaryBreakdownResponse(BaseModel):
    """Salary breakdown for reporting"""
    earnings: Dict[str, Decimal]
    deductions: Dict[str, Decimal]
    totals: Dict[str, Decimal]
    percentages: Dict[str, float]


class EmployeeSalaryStructureFilterParams(BaseModel):
    """Schema for filtering employee salary structures"""
    employee_id: Optional[int] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    min_basic: Optional[Decimal] = Field(None, ge=0, description="Minimum basic salary")
    max_basic: Optional[Decimal] = Field(None, ge=0, description="Maximum basic salary")
    is_active: Optional[bool] = None
    has_pan: Optional[bool] = None
    has_bank_account: Optional[bool] = None


class SalaryStatisticsResponse(BaseModel):
    """Salary statistics response"""
    total_employees: int
    average_basic: Decimal
    average_gross_earnings: Decimal
    average_net_takehome: Decimal
    highest_salary: Decimal
    lowest_salary: Decimal
    salary_distribution: Dict[str, int]  # Salary ranges and count