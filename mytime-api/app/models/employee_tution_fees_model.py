from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class EmployeeTutionFeesModel(BaseModel):
    id: int
    employee_id: Optional[int] = None
    employee_full_name: Optional[str] = None

    actual_fee: Optional[Decimal] = None
    final_fee: Optional[Decimal] = None
    remaining_fee: Optional[Decimal] = None
    paid_fee: Optional[Decimal] = None

    # Common fields (from Common base class)
    created_by: Optional[int] = None
    created_on: Optional[datetime] = None
    modified_by: Optional[int] = None
    modified_on: Optional[datetime] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True
