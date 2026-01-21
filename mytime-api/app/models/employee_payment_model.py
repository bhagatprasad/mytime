from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmployeePaymentModel(BaseModel):
    id: int
    employee_id: Optional[int] = None
    employee_full_name: Optional[str] = None

    payment_method_id: Optional[int] = None
    payment_method_name: Optional[str] = None

    payment_type_id: Optional[int] = None
    payment_type_name: Optional[str] = None

    amount: Optional[float] = None
    payment_message: Optional[str] = None

    created_by: Optional[int] = None
    created_on: Optional[datetime] = None

    modified_by: Optional[int] = None
    modified_on: Optional[datetime] = None

    is_active: bool = True

    class Config:
        orm_mode = True
