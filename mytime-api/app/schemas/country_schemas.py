from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class CountryBase(BaseModel):
    Name: Optional[str] = Field(None, max_length=255, description="Country name")
    Code: Optional[str] = Field(None, max_length=10, description="Country code (e.g., US, IN)")
    IsActive: Optional[bool] = Field(True, description="Whether the country is active")


class CountryCreate(CountryBase):
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")


class CountryUpdate(BaseModel):
    Name: Optional[str] = Field(None, max_length=255, description="Country name")
    Code: Optional[str] = Field(None, max_length=10, description="Country code")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the country is active")


class CountryResponse(BaseModel):
    Id: int
    Name: Optional[str] = None
    Code: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class CountryListResponse(BaseModel):
    total: int
    items: List[CountryResponse]
    page: int
    size: int
    pages: int


class CountryExistsResponse(BaseModel):
    exists: bool


class CountryDeleteResponse(BaseModel):
    success: bool
    message: str = "Country deleted successfully"