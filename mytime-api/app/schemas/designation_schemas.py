from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class DesignationBase(BaseModel):
    """Base schema for Designation data"""
    Name: Optional[str] = Field(None, max_length=255, description="Designation name")
    Code: Optional[str] = Field(None, max_length=50, description="Designation code")
    IsActive: Optional[bool] = Field(True, description="Whether the designation is active")


class DesignationCreate(DesignationBase):
    """Schema for creating a new Designation"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")


class DesignationUpdate(BaseModel):
    """Schema for updating an existing Designation"""
    Name: Optional[str] = Field(None, max_length=255, description="Designation name")
    Code: Optional[str] = Field(None, max_length=50, description="Designation code")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the designation is active")


class DesignationResponse(BaseModel):
    """Schema for Designation response (read operations)"""
    DesignationId: int
    Name: Optional[str] = None
    Code: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class DesignationListResponse(BaseModel):
    """Schema for listing multiple Designations with pagination"""
    total: int
    items: List[DesignationResponse]
    page: int
    size: int
    pages: int


class DesignationExistsResponse(BaseModel):
    """Response for Designation existence check"""
    exists: bool


class DesignationDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Designation deleted successfully"