from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CountryBase(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    Code: Optional[str] = Field(None, max_length=100)
    IsActive: Optional[bool] = True

class CountryCreate(CountryBase):
    CreatedBy: Optional[int] = None

class CountryUpdate(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    Code: Optional[str] = Field(None, max_length=100)
    IsActive: Optional[bool] = None
    ModifiedBy: Optional[int] = None

class CountryResponse(CountryBase):
    Id: int
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CountryListResponse(BaseModel):
    """Schema for listing multiple Countrys - matching C# return structure"""
    total: int
    items: List[CountryResponse]
    page: int
    size: int
    pages: int

class CountryExistsResponse(BaseModel):
    """Response for Country existence check"""
    exists: bool

class CountryDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Country deleted successfully"