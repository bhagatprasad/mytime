from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class TimesheetTaskBase(BaseModel):
    TaskItemId: Optional[int] = None
    TaskCodeId: Optional[int] = None
    MondayHours: Optional[int] = None
    TuesdayHours: Optional[int] = None
    WednesdayHours: Optional[int] = None
    ThursdayHours: Optional[int] = None
    FridayHours: Optional[int] = None
    SaturdayHours: Optional[int] = None
    SundayHours: Optional[int] = None
    TotalHrs: Optional[float] = None
    IsActive: Optional[bool] = True

class TimesheetTaskCreate(TimesheetTaskBase):
    CreatedBy: Optional[int] = None

class TimesheetTaskUpdate(BaseModel):
    TaskItemId: Optional[int] = None
    TaskCodeId: Optional[int] = None
    MondayHours: Optional[int] = None
    TuesdayHours: Optional[int] = None
    WednesdayHours: Optional[int] = None
    ThursdayHours: Optional[int] = None
    FridayHours: Optional[int] = None
    SaturdayHours: Optional[int] = None
    SundayHours: Optional[int] = None
    TotalHrs: Optional[float] = None
    ModifiedBy: Optional[int] = None
    IsActive: Optional[bool] = None

class TimesheetTaskResponse(BaseModel):
    Id: int
    TimesheetId: Optional[int] = None
    TaskItemId: Optional[int] = None
    TaskCodeId: Optional[int] = None
    MondayHours: Optional[int] = None
    TuesdayHours: Optional[int] = None
    WednesdayHours: Optional[int] = None
    ThursdayHours: Optional[int] = None
    FridayHours: Optional[int] = None
    SaturdayHours: Optional[int] = None
    SundayHours: Optional[int] = None
    TotalHrs: Optional[float] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class TimesheetBase(BaseModel):
    FromDate: Optional[datetime] = None
    ToDate: Optional[datetime] = None
    Description: Optional[str] = None
    EmployeeId: Optional[int] = None
    UserId: Optional[int] = None
    Status: Optional[str] = None
    AssignedOn: Optional[datetime] = None
    AssignedTo: Optional[int] = None
    ApprovedOn: Optional[datetime] = None
    ApprovedBy: Optional[int] = None
    ApprovedComments: Optional[str] = None
    CancelledOn: Optional[datetime] = None
    CancelledBy: Optional[int] = None
    CancelledComments: Optional[str] = None
    RejectedOn: Optional[datetime] = None
    RejectedBy: Optional[int] = None
    RejectedComments: Optional[str] = None
    TotalHrs: Optional[float] = None
    IsActive: Optional[bool] = True

class TimesheetCreate(TimesheetBase):
    CreatedBy: Optional[int] = None
    tasks: Optional[List[TimesheetTaskCreate]] = []

class TimesheetUpdate(BaseModel):
    FromDate: Optional[datetime] = None
    ToDate: Optional[datetime] = None
    Description: Optional[str] = None
    EmployeeId: Optional[int] = None
    UserId: Optional[int] = None
    Status: Optional[str] = None
    AssignedOn: Optional[datetime] = None
    AssignedTo: Optional[int] = None
    ApprovedOn: Optional[datetime] = None
    ApprovedBy: Optional[int] = None
    ApprovedComments: Optional[str] = None
    CancelledOn: Optional[datetime] = None
    CancelledBy: Optional[int] = None
    CancelledComments: Optional[str] = None
    RejectedOn: Optional[datetime] = None
    RejectedBy: Optional[int] = None
    RejectedComments: Optional[str] = None
    TotalHrs: Optional[float] = None
    ModifiedBy: Optional[int] = None
    IsActive: Optional[bool] = None

class TimesheetResponse(BaseModel):
    Id: int
    FromDate: Optional[datetime] = None
    ToDate: Optional[datetime] = None
    Description: Optional[str] = None
    EmployeeId: Optional[int] = None
    UserId: Optional[int] = None
    Status: Optional[str] = None
    AssignedOn: Optional[datetime] = None
    AssignedTo: Optional[int] = None
    ApprovedOn: Optional[datetime] = None
    ApprovedBy: Optional[int] = None
    ApprovedComments: Optional[str] = None
    CancelledOn: Optional[datetime] = None
    CancelledBy: Optional[int] = None
    CancelledComments: Optional[str] = None
    RejectedOn: Optional[datetime] = None
    RejectedBy: Optional[int] = None
    RejectedComments: Optional[str] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None
    TotalHrs: Optional[float] = None
    tasks: List[TimesheetTaskResponse] = []

    model_config = ConfigDict(from_attributes=True)

class TimesheetListResponse(BaseModel):
    total: int
    items: List[TimesheetResponse]
    page: int
    size: int
    pages: int

class TimesheetDeleteResponse(BaseModel):
    success: bool
    message: str = "Timesheet deleted successfully"