from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date, time

# Base Schema
class AttendenceBase(BaseModel):
    """Base schema for Employee Attendence data"""
    EmployeeId: Optional[int] = Field(None, description="Employee ID")
    AttendenceDate: Optional[date] = Field(None, description="Attendence date")
    CheckInTime: Optional[time] = Field(None, description="Check-in time")
    CheckOutTime: Optional[time] = Field(None, description="Check-out time")
    Status: Optional[str] = Field(None, max_length=20, description="Attendence status")
    WorkHours: Optional[float] = Field(None, description="Total work hours")
    Description: Optional[str] = Field(None, description="Remarks / description")
    ApprovalStatus: str = Field("Pending", max_length=20, description="Approval status")

    model_config = {"from_attributes": True}

# Create Schema
class AttendenceCreate(AttendenceBase):
    """Schema for creating a new Attendence"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")

# Update Schema
class AttendenceUpdate(BaseModel):
    """Schema for updating an existing Attendence"""
    EmployeeId: Optional[int] = Field(None, description="Employee ID")
    AttendenceDate: Optional[date] = Field(None, description="Attendence date")
    CheckInTime: Optional[time] = Field(None, description="Check-in time")
    CheckOutTime: Optional[time] = Field(None, description="Check-out time")
    Status: Optional[str] = Field(None, max_length=20, description="Attendence status")
    WorkHours: Optional[float] = Field(None, description="Total work hours")
    Description: Optional[str] = Field(None, description="Remarks / description")
    ModifiedBy: Optional[int] = Field(None, description="User ID who modified the record")
    
    # Approval Fields
    ApprovalStatus: Optional[str] = Field(None, max_length=20, description="Approval status")
    ApprovedBy: Optional[int] = Field(None, description="Approved by user ID")
    ApprovedOn: Optional[datetime] = Field(None, description="Approved date")
    RejectedBy: Optional[int] = Field(None, description="Rejected by user ID")
    RejectedOn: Optional[datetime] = Field(None, description="Rejected date")
    RejectionReason: Optional[str] = Field(None, description="Reason for rejection")

    model_config = {"from_attributes": True}

# Response Schema
class AttendenceResponse(AttendenceBase):
    AttendenceId: int
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    ApprovalStatus: Optional[str] = None
    ApprovedBy: Optional[int] = None
    ApprovedOn: Optional[datetime] = None
    RejectedBy: Optional[int] = None
    RejectedOn: Optional[datetime] = None
    RejectionReason: Optional[str] = None

    model_config = {"from_attributes": True}

# List Response Schema (Pagination)
class AttendenceListResponse(BaseModel):
    total: int
    items: List[AttendenceResponse]
    page: int
    size: int
    pages: int

    model_config = {"from_attributes": True}

# Exists Response
class AttendenceExistsResponse(BaseModel):
    exists: bool
    model_config = {"from_attributes": True}

# Delete Response
class AttendenceDeleteResponse(BaseModel):
    success: bool
    message: str = "Attendence deleted successfully"
    model_config = {"from_attributes": True}