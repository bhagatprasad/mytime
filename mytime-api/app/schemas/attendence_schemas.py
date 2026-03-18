from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time, datetime

class AttendanceBase(BaseModel):
    EmployeeId: int
    AttendanceDate: date
    CheckInTime: Optional[time] = None
    CheckOutTime: Optional[time] = None
    Status: str
    WorkHours: Optional[float] = None
    Description: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    CreatedBy: Optional[int] = None

class AttendanceUpdate(BaseModel):
    EmployeeId: Optional[int] = None
    AttendanceDate: Optional[date] = None
    CheckInTime: Optional[time] = None
    CheckOutTime: Optional[time] = None
    Status: Optional[str] = None
    WorkHours: Optional[float] = None
    Description: Optional[str] = None

    ModifiedBy: Optional[int] = None

    # Approval Fields
    ApprovalStatus: Optional[str] = None
    ApprovedBy: Optional[int] = None
    ApprovedOn: Optional[datetime] = None
    RejectedBy: Optional[int] = None
    RejectedOn: Optional[datetime] = None
    RejectionReason: Optional[str] = None

class AttendanceResponse(AttendanceBase):
    AttendanceId: int

    CreatedOn: Optional[datetime]
    CreatedBy: Optional[int]
    ModifiedOn: Optional[datetime]
    ModifiedBy: Optional[int]

    ApprovalStatus: Optional[str]
    ApprovedBy: Optional[int]
    ApprovedOn: Optional[datetime]
    RejectedBy: Optional[int]
    RejectedOn: Optional[datetime]
    RejectionReason: Optional[str]

    class Config:
        orm_mode = True


from datetime import date, time, datetime
from typing import Optional,List

class AttendanceBase(BaseModel):
    """Base schema for Attendance data"""
    EmployeeId     : int
    AttendanceDate : date
    CheckInTime    : Optional[time] = None
    CheckOutTime   : Optional[time] = None
    Status         : str
    WorkHours      : Optional[float] = None
    Description    : Optional[str] = None

class AttendanceCreate(AttendanceBase):
    """Schema for creating a new Attendance"""
    CreatedBy      : Optional[int] = None

class AttendanceUpdate(BaseModel):
    """Schema for updating an existing Attendance"""
    EmployeeId     : Optional[int] = None
    AttendanceDate : Optional[date] = None
    CheckInTime    : Optional[time] = None
    CheckOutTime   : Optional[time] = None
    Status         : Optional[str] = None
    WorkHours      : Optional[float] = None
    Description    : Optional[str] = None
    ModifiedBy     : Optional[int] = None

class AttendanceResponse(AttendanceBase):
    """Schema for Attendance response (read operations)"""
    AttendanceId  : int
    CreatedOn     : datetime
    CreatedBy     : Optional[int]
    ModifiedOn    : Optional[datetime]
    ModifiedBy    : Optional[int]

class AttendanceListResponse(BaseModel):
    """Schema for listing multiple Attendances with pagination"""
    """Schema for listing multiple Attendance records with pagination"""
    total: int
    items: List[AttendanceResponse]
    page: int
    size: int
    pages: int

class AttendanceExistsResponse(BaseModel):
    """Response for Attendance existence check"""
    exists: bool
   
class AttendanceDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Attendance deleted successfully"
    deletedId: int
