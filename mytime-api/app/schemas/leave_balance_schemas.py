
from pydantic import BaseModel

class LeaveBalanceResponse(BaseModel):
    Id: int
    UserId: int
    LeaveTypeId: int
    Year: int
    TotalLeaves: int
    UsedLeaves: int
    RemainingLeaves: int

    class Config:
        orm_mode = True