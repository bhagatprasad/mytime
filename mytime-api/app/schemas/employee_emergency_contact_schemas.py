from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class EmployeeEmergencyContactBase(BaseModel):
    """Base schema for EmployeeEmergencyContact data"""
    EmployeeId: int = Field(..., description="Foreign key to Employee table")
    Name: str = Field(..., max_length=255, description="Emergency contact name")
    Relation: str = Field(..., max_length=100, description="Relationship to employee")
    Phone: str = Field(..., max_length=20, description="Emergency phone number")
    Email: Optional[str] = Field(None, description="Emergency email address")
    Address: Optional[str] = Field(None, max_length=500, description="Emergency contact address")


class EmployeeEmergencyContactCreate(EmployeeEmergencyContactBase):
    """Schema for creating a new EmployeeEmergencyContact"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")
    IsActive: Optional[bool] = Field(True, description="Whether the emergency contact is active")


class EmployeeEmergencyContactUpdate(BaseModel):
    """Schema for updating an existing EmployeeEmergencyContact"""
    Name: Optional[str] = Field(None, max_length=255, description="Emergency contact name")
    Relation: Optional[str] = Field(None, max_length=100, description="Relationship to employee")
    Phone: Optional[str] = Field(None, max_length=20, description="Emergency phone number")
    Email: Optional[str] = Field(None, description="Emergency email address")
    Address: Optional[str] = Field(None, max_length=500, description="Emergency contact address")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the emergency contact is active")


class EmployeeEmergencyContactResponse(BaseModel):
    """Schema for EmployeeEmergencyContact response (read operations)"""
    EmployeeEmergencyContactId: int
    EmployeeId: int
    Name: str
    Relation: str
    Phone: str
    Email: Optional[str] = None
    Address: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class EmployeeEmergencyContactListResponse(BaseModel):
    """Schema for listing multiple EmployeeEmergencyContacts with pagination"""
    total: int
    items: List[EmployeeEmergencyContactResponse]
    page: int
    size: int
    pages: int


class EmployeeEmergencyContactExistsResponse(BaseModel):
    """Response for EmployeeEmergencyContact existence check"""
    exists: bool
    employee_emergency_contact_id: Optional[int] = None


class EmployeeEmergencyContactDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Employee emergency contact deleted successfully"
    employee_emergency_contact_id: Optional[int] = None


class EmployeeEmergencyContactWithDetailsResponse(EmployeeEmergencyContactResponse):
    """Extended response with related data"""
    employee_name: Optional[str] = None


class EmployeeEmergencyContactCreateResponse(BaseModel):
    """Response after creating a new employee emergency contact"""
    success: bool
    message: str = "Employee emergency contact created successfully"
    employee_emergency_contact_id: int


class EmployeeEmergencyContactUpdateResponse(BaseModel):
    """Response after updating an employee emergency contact"""
    success: bool
    message: str = "Employee emergency contact updated successfully"
    employee_emergency_contact_id: int
    modified_fields: List[str] = Field(default_factory=list)


class EmployeeEmergencyContactBulkCreate(BaseModel):
    """Schema for creating multiple emergency contacts at once"""
    contacts: List[EmployeeEmergencyContactCreate]
    employee_id: Optional[int] = None


class EmployeeEmergencyContactFilterParams(BaseModel):
    """Schema for filtering employee emergency contacts"""
    employee_id: Optional[int] = None
    relation: Optional[str] = None
    is_active: Optional[bool] = None
    search_term: Optional[str] = None