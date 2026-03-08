from pydantic import BaseModel
from typing import Optional

from app.models.employee import Employee
from app.models.employee_salary import EmployeeSalary


# assume these already exist



class EmployeeSalaryViewModel(BaseModel):
    employee_salary: Optional["EmployeeSalary"] = None
    employee: Optional["Employee"] = None

    class Config:
        orm_mode = True
