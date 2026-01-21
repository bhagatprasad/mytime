from pydantic import BaseModel
from typing import Optional


class ReportingManagerVM(BaseModel):
    repoting_manager_id: int
    employee_id: int
    manager_id: int

    employee_code: str
    employee_email: str
    employee_name: str

    manager_code: str
    manager_email: str
    manager_name: str

    class Config:
        orm_mode = True
