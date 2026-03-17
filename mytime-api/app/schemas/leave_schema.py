from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional,List

class LeaveApply(BaseModel):
    userId: int
    leaveTypeId: int
    fromDate: date
    toDate: date
    reason: str = Field(..., max_length=300)
    description: Optional[str] = Field(None, max_length=500)

    @validator('toDate')
    def validate_dates(cls, v, values):
        if 'fromDate' in values and v < values['fromDate']:
            raise ValueError('toDate must be after fromDate')
        return v

class LeaveApprove(BaseModel):
    adminComment: str = Field(..., max_length=500)
    approvedBy: Optional[int] = None

class LeaveReject(BaseModel):
    adminComment: str = Field(..., max_length=500)
    rejectedBy: Optional[int] = None

class LeaveCancel(BaseModel):
    cancelReason: str = Field(..., max_length=500)

class LeaveResponse(BaseModel):
    Id: int
    UserId: int
    LeaveTypeId: int
    FromDate: date
    ToDate: date
    TotalDays: int
    Reason: str
    Description: Optional[str]
    Status: str
    AdminComment: Optional[str]
    CancelReason: Optional[str]
    CreatedBy: Optional[int]
    CreatedOn: datetime
    ModifiedBy: Optional[int]
    ModifiedOn: Optional[datetime]
    IsActive: bool

    class Config:
        from_attributes = True

class LeaveListResponse(BaseModel):
    total: int
    items: List[LeaveResponse]
    page: int
    size: int
    pages: int