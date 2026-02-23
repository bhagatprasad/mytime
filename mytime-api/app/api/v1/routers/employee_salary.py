from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.employee_salary import EmployeeSalary
from app.services.employee_salary_service import EmployeeSalaryService
from app.schemas.employee_salary_schemas import EmployeeSalaryInDB

router = APIRouter()

@router.get("/fetchEmployeeSalary/{id}", response_model=EmployeeSalaryInDB)
async def fetch_employee_salary(id: int, db: Session = Depends(get_db)):
    """Get employee salary by ID - matches C# fetchEmployeeSalary endpoint"""
    try:
        employee_salary = EmployeeSalaryService.fetch_employee_salary(db, id)
        if not employee_salary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salary not found"
            )
        return employee_salary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/fetchEmployeeSalariesByEmployee/{employeeId}", response_model=List[EmployeeSalaryInDB])
async def fetch_employee_salaries_by_employee(employeeId: int, db: Session = Depends(get_db)):
    """Get employee salaries by employee ID - matches C# fetchEmployeeSalaries endpoint"""
    try:
        employee_salaries = EmployeeSalaryService.fetch_employee_salaries_by_employeeid(db, employeeId)
        if not employee_salaries:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Salaries not found for employee ID: {employeeId}"
            )
        return employee_salaries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/fetchEmployeeSalaries", response_model=List[EmployeeSalaryInDB])
async def fetch_all_employee_salaries(db: Session = Depends(get_db)):
    """Get all employee salaries - matches C# fetchEmployeeSalaries endpoint"""
    try:
        employee_salaries = EmployeeSalaryService.fetch_all_employee_salaries(db)
        if not employee_salaries:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salaries not found"
            )
        return employee_salaries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )