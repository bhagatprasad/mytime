from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class EmployeeSalaryStructureModel(BaseModel):
    employee_salary_structure_id: int
    employee_id: Optional[int] = None
    employee_name: Optional[int] = None  # C# had long? EmployeeName, keeping it same

    PAN: Optional[str] = None
    Adhar: Optional[str] = None
    BankAccount: Optional[str] = None
    BankName: Optional[str] = None
    IFSC: Optional[str] = None

    BASIC: Optional[Decimal] = None
    HRA: Optional[Decimal] = None
    CONVEYANCE: Optional[Decimal] = None
    MEDICALALLOWANCE: Optional[Decimal] = None
    SPECIALALLOWANCE: Optional[Decimal] = None
    SPECIALBONUS: Optional[Decimal] = None
    STATUTORYBONUS: Optional[Decimal] = None
    OTHERS: Optional[Decimal] = None

    UAN: Optional[str] = None
    PFNO: Optional[str] = None

    PF: Optional[Decimal] = None
    ESIC: Optional[Decimal] = None
    PROFESSIONALTAX: Optional[Decimal] = None
    GroupHealthInsurance: Optional[Decimal] = None

    GROSSEARNINGS: Optional[Decimal] = None
    GROSSDEDUCTIONS: Optional[Decimal] = None

    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    class Config:
        orm_mode = True
