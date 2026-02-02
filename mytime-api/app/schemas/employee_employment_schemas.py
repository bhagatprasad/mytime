from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Dict, Optional, List
from datetime import datetime


class EmployeeEmploymentBase(BaseModel):
    """Base schema for EmployeeEmployment data"""
    EmployeeId: int = Field(..., description="Foreign key to Employee table")
    CompanyName: str = Field(..., max_length=500, description="Previous company name")
    Address: Optional[str] = Field(None, max_length=1000, description="Company address")
    Designation: str = Field(..., max_length=255, description="Previous designation")
    StartedOn: datetime = Field(..., description="Employment start date")
    EndedOn: Optional[datetime] = Field(None, description="Employment end date")
    Reason: Optional[str] = Field(None, max_length=1000, description="Reason for leaving")
    ReportingManager: Optional[str] = Field(None, max_length=255, description="Reporting manager name")
    HREmail: Optional[EmailStr] = Field(None, description="HR email at previous company")
    Reference: Optional[str] = Field(None, max_length=1000, description="Reference details")


class EmployeeEmploymentCreate(EmployeeEmploymentBase):
    """Schema for creating a new EmployeeEmployment"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")
    IsActive: Optional[bool] = Field(True, description="Whether the employment record is active")


class EmployeeEmploymentUpdate(BaseModel):
    """Schema for updating an existing EmployeeEmployment"""
    CompanyName: Optional[str] = Field(None, max_length=500, description="Previous company name")
    Address: Optional[str] = Field(None, max_length=1000, description="Company address")
    Designation: Optional[str] = Field(None, max_length=255, description="Previous designation")
    StartedOn: Optional[datetime] = Field(None, description="Employment start date")
    EndedOn: Optional[datetime] = Field(None, description="Employment end date")
    Reason: Optional[str] = Field(None, max_length=1000, description="Reason for leaving")
    ReportingManager: Optional[str] = Field(None, max_length=255, description="Reporting manager name")
    HREmail: Optional[EmailStr] = Field(None, description="HR email at previous company")
    Reference: Optional[str] = Field(None, max_length=1000, description="Reference details")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the employment record is active")


class EmployeeEmploymentResponse(BaseModel):
    """Schema for EmployeeEmployment response (read operations)"""
    EmployeeEmploymentId: int
    EmployeeId: int
    CompanyName: str
    Address: Optional[str] = None
    Designation: str
    StartedOn: datetime
    EndedOn: Optional[datetime] = None
    Reason: Optional[str] = None
    ReportingManager: Optional[str] = None
    HREmail: Optional[str] = None
    Reference: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class EmployeeEmploymentListResponse(BaseModel):
    """Schema for listing multiple EmployeeEmployment records with pagination"""
    total: int
    items: List[EmployeeEmploymentResponse]
    page: int
    size: int
    pages: int


class EmployeeEmploymentExistsResponse(BaseModel):
    """Response for EmployeeEmployment existence check"""
    exists: bool
    employee_employment_id: Optional[int] = None


class EmployeeEmploymentDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Employee employment record deleted successfully"
    employee_employment_id: Optional[int] = None


class EmployeeEmploymentWithDetailsResponse(EmployeeEmploymentResponse):
    """Extended response with related data"""
    employee_name: Optional[str] = None
    duration_months: Optional[int] = Field(None, description="Employment duration in months")

class EmployeeEmploymentCreateResponse(BaseModel):
    """Response after creating a new employee employment record"""
    success: bool
    message: str = "Employee employment record created successfully"
    employee_employment_id: int


class EmployeeEmploymentUpdateResponse(BaseModel):
    """Response after updating an employee employment record"""
    success: bool
    message: str = "Employee employment record updated successfully"
    employee_employment_id: int
    modified_fields: List[str] = Field(default_factory=list)


class EmployeeEmploymentBulkCreate(BaseModel):
    """Schema for creating multiple employment records at once"""
    employments: List[EmployeeEmploymentCreate]
    employee_id: Optional[int] = None


class EmployeeEmploymentFilterParams(BaseModel):
    """Schema for filtering employee employment records"""
    employee_id: Optional[int] = None
    company_name: Optional[str] = None
    designation: Optional[str] = None
    start_year_from: Optional[int] = Field(None, ge=1900, le=2100, description="Start year from")
    start_year_to: Optional[int] = Field(None, ge=1900, le=2100, description="Start year to")
    end_year_from: Optional[int] = Field(None, ge=1900, le=2100, description="End year from")
    end_year_to: Optional[int] = Field(None, ge=1900, le=2100, description="End year to")
    is_active: Optional[bool] = None
    search_term: Optional[str] = None


class EmployeeEmploymentStatistics(BaseModel):
    """Schema for employment statistics"""
    total_records: int
    by_company: Dict[str, int]
    by_designation: Dict[str, int]
    by_year: Dict[int, int]
    average_duration_months: float