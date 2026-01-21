from pydantic import BaseModel
from typing import List, Optional


# ---- Import your existing models ----
from app.models.employee import EmployeeModel
from app.models.employee_address import EmployeeAddressModel
from app.models.employee_education import EmployeeEducationModel
from app.models.employee_emergency_contact import EmployeeEmergencyContactModel
from app.models.employee_employment import EmployeeEmploymentModel


class AddEditEmployeeModel(BaseModel):
    employee: Optional["EmployeeModel"] = None

    employeeAddresses: List["EmployeeAddressModel"] = []
    employeeEducations: List["EmployeeEducationModel"] = []
    employeeEmergencyContacts: List["EmployeeEmergencyContactModel"] = []
    employeeEmployments: List["EmployeeEmploymentModel"] = []

    PAN: Optional[str] = None
    Adhar: Optional[str] = None
    BankAccount: Optional[str] = None
    BankName: Optional[str] = None
    IFSC: Optional[str] = None
    UAN: Optional[str] = None
    PFNO: Optional[str] = None

    class Config:
        orm_mode = True
