from pydantic import BaseModel
from datetime import date


class LeaveApply(BaseModel):

    userId:int
    leaveTypeId:int
    fromDate:date
    toDate:date
    reason:str
    description:str

class LeaveApprove(BaseModel):

    adminComment:str

class LeaveReject(BaseModel):

    adminComment:str

class LeaveCancel(BaseModel):

    cancelReason:str    