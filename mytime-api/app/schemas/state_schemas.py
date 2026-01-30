from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class StateBase(BaseModel):
    """Base schema for State data"""
    CountryId: int = Field(..., description="Foreign key to Country table")
    Name: str = Field(..., max_length=255, description="State name")
    Description: Optional[str] = Field(None, description="State description")
    SateCode: Optional[str] = Field(None, max_length=100, description="State code")
    CountryCode: Optional[str] = Field(None, max_length=100, description="Country code")


class StateCreate(StateBase):
    """Schema for creating a new State"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")
    IsActive: Optional[bool] = Field(True, description="Whether the state is active")


class StateUpdate(BaseModel):
    """Schema for updating an existing State"""
    CountryId: Optional[int] = Field(None, description="Foreign key to Country table")
    Name: Optional[str] = Field(None, max_length=255, description="State name")
    Description: Optional[str] = Field(None, description="State description")
    SateCode: Optional[str] = Field(None, max_length=100, description="State code")
    CountryCode: Optional[str] = Field(None, max_length=100, description="Country code")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the state is active")


class StateResponse(BaseModel):
    """Schema for State response (read operations)"""
    StateId: int
    CountryId: int
    Name: str
    Description: Optional[str] = None
    SateCode: Optional[str] = None
    CountryCode: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class StateListResponse(BaseModel):
    """Schema for listing multiple States with pagination"""
    total: int
    items: List[StateResponse]
    page: int
    size: int
    pages: int


class StateExistsResponse(BaseModel):
    """Response for State existence check"""
    exists: bool


class StateDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "State deleted successfully"