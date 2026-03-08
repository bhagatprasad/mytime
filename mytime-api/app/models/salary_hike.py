from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class SalaryHikeModel(BaseModel):
    employee_id: int
    original_salary: Optional[Decimal] = None
    latest_salary: Optional[Decimal] = None
    modified_by: Optional[int] = None
    modified_on: Optional[datetime] = None

    class Config:
        orm_mode = True
