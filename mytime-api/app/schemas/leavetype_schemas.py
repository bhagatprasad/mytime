from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class LeaveTypeBase(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    # MaxDaysPerYear: Optional[int] = Field(None, max_length=100)
    MaxDaysPerYear: Optional[int] = None
    Description: Optional[str] = Field(None, description="LeaveType description")
    IsActive: Optional[bool] = True

class LeaveTypeCreate(LeaveTypeBase):
    CreatedBy: Optional[int] = None

class LeaveTypeUpdate(BaseModel):
    Name: Optional[str] = Field(None, max_length=255)
    #MaxDaysPerYear: Optional[int] = Field(None, max_length=100)
    MaxDaysPerYear: Optional[int] = None
    Description: Optional[str] = Field(None, description="LeaveType description")
    ModifiedBy: Optional[int] = None
    IsActive: Optional[bool] = None
  

class LeaveTypeResponse(LeaveTypeBase):
    Id: int
    Name: Optional[str] = None
    MaxDaysPerYear: Optional[int] = None
    Description: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class LeaveTypeListResponse(BaseModel):
    """Schema for listing multiple leavetypes - matching C# return structure"""
    total: int
    items: List[LeaveTypeResponse]
    page: int
    size: int
    pages: int

class LeaveTypeExistsResponse(BaseModel):
    """Response for leavetype existence check"""
    exists: bool

class LeaveTypeDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "leavetype deleted successfully"