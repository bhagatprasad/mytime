from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class MonthlySalaryBase(BaseModel):
    """Base schema with common fields"""
    Title: Optional[str] = None
    SalaryMonth: Optional[str] = Field(None, max_length=20)
    SalaryYear: Optional[str] = Field(None, max_length=4)
    Location: Optional[str] = None
    StdDays: Optional[int] = None
    WrkDays: Optional[int] = None
    LopDays: Optional[int] = None
    IsActive: Optional[bool] = True

class MonthlySalaryCreate(MonthlySalaryBase):
    """Schema for creating a new monthly salary"""
    CreatedBy: Optional[int] = None

class MonthlySalaryUpdate(BaseModel):
    """Schema for updating an existing monthly salary"""
    Title: Optional[str] = None
    SalaryMonth: Optional[str] = Field(None, max_length=20)
    SalaryYear: Optional[str] = Field(None, max_length=4)
    Location: Optional[str] = None
    StdDays: Optional[int] = None
    WrkDays: Optional[int] = None
    LopDays: Optional[int] = None
    IsActive: Optional[bool] = None
    ModifiedBy: Optional[int] = None

class MonthlySalaryResponse(MonthlySalaryBase):
    """Schema for single monthly salary response"""
    MonthlySalaryId: int
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Keep this if you still need it for other purposes, but don't use it for the list endpoint
class MonthlySalaryListResponse(BaseModel):
    """Schema for listing multiple monthly salaries with pagination"""
    total: int
    items: List[MonthlySalaryResponse]
    page: int
    size: int
    pages: int

class MonthlySalaryExistsResponse(BaseModel):
    """Response for monthly salary existence check"""
    exists: bool

class MonthlySalaryDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Monthly salary record deleted successfully"