from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class CityBase(BaseModel):
    """Base schema for City data"""
    Name: Optional[str] = Field(None, max_length=255, description="City name")
    Code: Optional[str] = Field(None, max_length=50, description="City code")
    CountryId: Optional[int] = Field(None, description="Foreign key to Country table")
    StateId: Optional[int] = Field(None, description="Foreign key to State table")
    IsActive: Optional[bool] = Field(True, description="Whether the city is active")


class CityCreate(CityBase):
    """Schema for creating a new City"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")


class CityUpdate(BaseModel):
    """Schema for updating an existing City"""
    Name: Optional[str] = Field(None, max_length=255, description="City name")
    Code: Optional[str] = Field(None, max_length=50, description="City code")
    CountryId: Optional[int] = Field(None, description="Foreign key to Country table")
    StateId: Optional[int] = Field(None, description="Foreign key to State table")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the city is active")


class CityResponse(BaseModel):
    """Schema for City response (read operations)"""
    Id: int
    Name: Optional[str] = None
    Code: Optional[str] = None
    CountryId: Optional[int] = None
    StateId: Optional[int] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class CityListResponse(BaseModel):
    """Schema for listing multiple Cities with pagination"""
    total: int
    items: List[CityResponse]
    page: int
    size: int
    pages: int


class CityExistsResponse(BaseModel):
    """Response for City existence check"""
    exists: bool


class CityDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "City deleted successfully"


class CityWithRelationsResponse(CityResponse):
    """Extended response with related country and state info"""
    CountryName: Optional[str] = None
    CountryCode: Optional[str] = None
    StateName: Optional[str] = None
    StateCode: Optional[str] = None