from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TimesheetStatusChangeModel(BaseModel):
    timesheet_id: int
    change_type: Optional[str] = None
    status: Optional[str] = None
    comment: Optional[str] = None
    modified_on: Optional[datetime] = None
    modified_by: Optional[int] = None

    class Config:
        orm_mode = True
