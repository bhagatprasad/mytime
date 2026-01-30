from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class DepartmentBase(BaseModel):
    """Base schema for Department data"""
    Name: Optional[str] = Field(None, max_length=255, description="Department name")
    Description: Optional[str] = Field(None, description="Department description")
    Code: Optional[str] = Field(None, max_length=50, description="Department code")
    IsActive: Optional[bool] = Field(True, description="Whether the department is active")


class DepartmentCreate(DepartmentBase):
    """Schema for creating a new Department"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")


class DepartmentUpdate(BaseModel):
    """Schema for updating an existing Department"""
    Name: Optional[str] = Field(None, max_length=255, description="Department name")
    Description: Optional[str] = Field(None, description="Department description")
    Code: Optional[str] = Field(None, max_length=50, description="Department code")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the department is active")


class DepartmentResponse(BaseModel):
    """Schema for Department response (read operations)"""
    DepartmentId: int
    Name: Optional[str] = None
    Description: Optional[str] = None
    Code: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class DepartmentListResponse(BaseModel):
    """Schema for listing multiple Departments with pagination"""
    total: int
    items: List[DepartmentResponse]
    page: int
    size: int
    pages: int


class DepartmentExistsResponse(BaseModel):
    """Response for Department existence check"""
    exists: bool


class DepartmentDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Department deleted successfully"