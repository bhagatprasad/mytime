from pydantic import BaseModel, Field, ConfigDict, condecimal
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class EmployeeBase(BaseModel):
    """Base schema for Employee data"""
    EmployeeCode: Optional[str] = Field(None, max_length=50, description="Unique employee code")
    FirstName: str = Field(..., max_length=255, description="Employee's first name")
    LastName: str = Field(..., max_length=255, description="Employee's last name")
    FatherName: Optional[str] = Field(None, max_length=255, description="Father's name")
    MotherName: Optional[str] = Field(None, max_length=255, description="Mother's name")
    Gender: Optional[str] = Field(None, max_length=10, description="Gender (Male/Female/Other)")
    DateOfBirth: Optional[datetime] = Field(None, description="Date of birth")
    Email: Optional[str] = Field(None, description="Email address")
    Phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    UserId: Optional[int] = Field(None, description="Associated user ID")
    RoleId: Optional[int] = Field(None, description="Role ID")
    DepartmentId: Optional[int] = Field(None, description="Department ID")
    DesignationId: Optional[int] = Field(None, description="Designation ID")
    StartedOn: Optional[datetime] = Field(None, description="Employment start date")
    EndedOn: Optional[datetime] = Field(None, description="Employment end date")
    ResignedOn: Optional[datetime] = Field(None, description="Resignation date")
    LastWorkingDay: Optional[datetime] = Field(None, description="Last working day")
    OfferReleasedOn: Optional[datetime] = Field(None, description="Date when offer was released")
    OfferAcceptedOn: Optional[datetime] = Field(None, description="Date when offer was accepted")
    
    # Corrected: Use condecimal instead of max_digits/decimal_places in Field()
    OfferPrice: Optional[condecimal] = Field(
        None, description="Offer price/salary"
    )
    CurrentPrice: Optional[condecimal] = Field(
        None, description="Current salary"
    )
    JoiningBonus: Optional[condecimal] = Field(
        None, description="Joining bonus amount"
    )


class EmployeeCreate(EmployeeBase):
    """Schema for creating a new Employee"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")
    IsActive: Optional[bool] = Field(True, description="Whether the employee is active")


class EmployeeUpdate(BaseModel):
    """Schema for updating an existing Employee"""
    EmployeeCode: Optional[str] = Field(None, max_length=50, description="Unique employee code")
    FirstName: Optional[str] = Field(None, max_length=255, description="Employee's first name")
    LastName: Optional[str] = Field(None, max_length=255, description="Employee's last name")
    FatherName: Optional[str] = Field(None, max_length=255, description="Father's name")
    MotherName: Optional[str] = Field(None, max_length=255, description="Mother's name")
    Gender: Optional[str] = Field(None, max_length=10, description="Gender (Male/Female/Other)")
    DateOfBirth: Optional[datetime] = Field(None, description="Date of birth")
    Email: Optional[str] = Field(None, description="Email address")
    Phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    UserId: Optional[int] = Field(None, description="Associated user ID")
    RoleId: Optional[int] = Field(None, description="Role ID")
    DepartmentId: Optional[int] = Field(None, description="Department ID")
    DesignationId: Optional[int] = Field(None, description="Designation ID")
    StartedOn: Optional[datetime] = Field(None, description="Employment start date")
    EndedOn: Optional[datetime] = Field(None, description="Employment end date")
    ResignedOn: Optional[datetime] = Field(None, description="Resignation date")
    LastWorkingDay: Optional[datetime] = Field(None, description="Last working day")
    OfferReleasedOn: Optional[datetime] = Field(None, description="Date when offer was released")
    OfferAcceptedOn: Optional[datetime] = Field(None, description="Date when offer was accepted")
    
    # Corrected: Use condecimal for Decimal fields
    OfferPrice: Optional[condecimal] = Field(
        None, description="Offer price/salary"
    )
    CurrentPrice: Optional[condecimal] = Field(
        None, description="Current salary"
    )
    JoiningBonus: Optional[condecimal] = Field(
        None, description="Joining bonus amount"
    )
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the employee is active")


class EmployeeResponse(BaseModel):
    """Schema for Employee response (read operations)"""
    EmployeeId: int
    EmployeeCode: Optional[str] = None
    FirstName: str
    LastName: str
    FatherName: Optional[str] = None
    MotherName: Optional[str] = None
    Gender: Optional[str] = None
    DateOfBirth: Optional[datetime] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    UserId: Optional[int] = None
    RoleId: Optional[int] = None
    DepartmentId: Optional[int] = None
    DesignationId: Optional[int] = None
    StartedOn: Optional[datetime] = None
    EndedOn: Optional[datetime] = None
    ResignedOn: Optional[datetime] = None
    LastWorkingDay: Optional[datetime] = None
    OfferReleasedOn: Optional[datetime] = None
    OfferAcceptedOn: Optional[datetime] = None
    OfferPrice: Optional[Decimal] = None
    CurrentPrice: Optional[Decimal] = None
    JoiningBonus: Optional[Decimal] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)


class EmployeeListResponse(BaseModel):
    """Schema for listing multiple Employees with pagination"""
    total: int
    items: List[EmployeeResponse]
    page: int
    size: int
    pages: int


class EmployeeExistsResponse(BaseModel):
    """Response for Employee existence check"""
    exists: bool
    employee_id: Optional[int] = None
    employee_code: Optional[str] = None


class EmployeeDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Employee deleted successfully"
    employee_id: Optional[int] = None


class EmployeeSummaryResponse(BaseModel):
    """Lightweight schema for employee summary/list views"""
    EmployeeId: int
    EmployeeCode: Optional[str] = None
    FirstName: str
    LastName: str
    Email: Optional[str] = None
    Phone: Optional[str] = None
    DepartmentId: Optional[int] = None
    DesignationId: Optional[int] = None
    IsActive: Optional[bool] = None
    FullName: str

    model_config = ConfigDict(from_attributes=True)


class EmployeeCreateResponse(BaseModel):
    """Response after creating a new employee"""
    success: bool
    message: str = "Employee created successfully"
    employee_id: int
    employee_code: Optional[str] = None


class EmployeeUpdateResponse(BaseModel):
    """Response after updating an employee"""
    success: bool
    message: str = "Employee updated successfully"
    employee_id: int
    modified_fields: List[str] = Field(default_factory=list)


class EmployeeFilterParams(BaseModel):
    """Schema for filtering employees"""
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
    start_date_from: Optional[datetime] = None
    start_date_to: Optional[datetime] = None
    search_term: Optional[str] = None
    gender: Optional[str] = None


class EmployeeSearchResponse(BaseModel):
    """Response for employee search"""
    total: int
    employees: List[EmployeeSummaryResponse]


# Alternative approach if you prefer to keep Decimal type annotations:
class EmployeeBaseAlternative(BaseModel):
    """Alternative with field_validator for Decimal fields"""
    # ... other fields ...
    
    OfferPrice: Optional[Decimal] = Field(None, description="Offer price/salary")
    CurrentPrice: Optional[Decimal] = Field(None, description="Current salary")
    JoiningBonus: Optional[Decimal] = Field(None, description="Joining bonus amount")
    