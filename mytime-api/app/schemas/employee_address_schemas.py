from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class EmployeeAddressBase(BaseModel):
    """Base schema for EmployeeAddress data"""
    EmployeeId: int = Field(..., description="Foreign key to Employee table")
    HNo: Optional[str] = Field(None, max_length=100, description="House number")
    AddressLineOne: str = Field(..., max_length=500, description="Address line 1")
    AddressLineTwo: Optional[str] = Field(None, max_length=500, description="Address line 2")
    Landmark: Optional[str] = Field(None, max_length=255, description="Landmark")
    CityId: Optional[int] = Field(None, description="Foreign key to City table")
    StateId: Optional[int] = Field(None, description="Foreign key to State table")
    CountryId: Optional[int] = Field(None, description="Foreign key to Country table")
    Zipcode: Optional[str] = Field(None, max_length=20, description="Postal/ZIP code")


class EmployeeAddressCreate(EmployeeAddressBase):
    """Schema for creating a new EmployeeAddress"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")
    IsActive: Optional[bool] = Field(True, description="Whether the address is active")


class EmployeeAddressUpdate(BaseModel):
    """Schema for updating an existing EmployeeAddress"""
    HNo: Optional[str] = Field(None, max_length=100, description="House number")
    AddressLineOne: Optional[str] = Field(None, max_length=500, description="Address line 1")
    AddressLineTwo: Optional[str] = Field(None, max_length=500, description="Address line 2")
    Landmark: Optional[str] = Field(None, max_length=255, description="Landmark")
    CityId: Optional[int] = Field(None, description="Foreign key to City table")
    StateId: Optional[int] = Field(None, description="Foreign key to State table")
    CountryId: Optional[int] = Field(None, description="Foreign key to Country table")
    Zipcode: Optional[str] = Field(None, max_length=20, description="Postal/ZIP code")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the address is active")


class EmployeeAddressResponse(BaseModel):
    """Schema for EmployeeAddress response (read operations)"""
    EmployeeAddressId: int
    EmployeeId: int
    HNo: Optional[str] = None
    AddressLineOne: str
    AddressLineTwo: Optional[str] = None
    Landmark: Optional[str] = None
    CityId: Optional[int] = None
    StateId: Optional[int] = None
    CountryId: Optional[int] = None
    Zipcode: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class EmployeeAddressListResponse(BaseModel):
    """Schema for listing multiple EmployeeAddresses with pagination"""
    total: int
    items: List[EmployeeAddressResponse]
    page: int
    size: int
    pages: int


class EmployeeAddressExistsResponse(BaseModel):
    """Response for EmployeeAddress existence check"""
    exists: bool
    employee_address_id: Optional[int] = None


class EmployeeAddressDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Employee address deleted successfully"
    employee_address_id: Optional[int] = None


class EmployeeAddressWithDetailsResponse(EmployeeAddressResponse):
    """Extended response with related data"""
    city_name: Optional[str] = None
    state_name: Optional[str] = None
    country_name: Optional[str] = None
    employee_name: Optional[str] = None


class EmployeeAddressCreateResponse(BaseModel):
    """Response after creating a new employee address"""
    success: bool
    message: str = "Employee address created successfully"
    employee_address_id: int


class EmployeeAddressUpdateResponse(BaseModel):
    """Response after updating an employee address"""
    success: bool
    message: str = "Employee address updated successfully"
    employee_address_id: int
    modified_fields: List[str] = Field(default_factory=list)


class EmployeeAddressBulkCreate(BaseModel):
    """Schema for creating multiple addresses at once"""
    addresses: List[EmployeeAddressCreate]
    employee_id: Optional[int] = None


class EmployeeAddressFilterParams(BaseModel):
    """Schema for filtering employee addresses"""
    employee_id: Optional[int] = None
    city_id: Optional[int] = None
    state_id: Optional[int] = None
    country_id: Optional[int] = None
    is_active: Optional[bool] = None
    search_term: Optional[str] = None