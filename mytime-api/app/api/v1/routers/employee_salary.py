from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.employee_salary import EmployeeSalary
from app.services.employee_salary_service import EmployeeSalaryService
from app.schemas.employee_salary_schemas import EmployeeSalaryInDB,EmployeeSalaryBulkCreate

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
    
@router.post("/createEmployeeSalariesBulk", response_model=List[EmployeeSalaryInDB])
async def create_employee_salaries_bulk(
    salaries: List[EmployeeSalaryBulkCreate],
    db: Session = Depends(get_db)
):
    """Bulk insert employee salaries - matches C# createEmployeeSalariesBulk endpoint"""
    try:
        if not salaries:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Salaries list cannot be empty"
            )
        created_salaries = EmployeeSalaryService.create_employee_salaries_bulk(
            db, [salary.model_dump() for salary in salaries]
        )
        return created_salaries
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.post("/insertEmployeeSalary", response_model=EmployeeSalaryInDB)
async def create_employee_salary(salary: dict, db: Session = Depends(get_db)):
    """Create a single employee salary - matches C# createEmployeeSalary endpoint"""
    try:
        created_salary = EmployeeSalaryService.create_employee_salary(db, salary)
        return created_salary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.put("/updateEmployeeSalary/{id}", response_model=EmployeeSalaryInDB)
async def update_employee_salary(id: int, salary: dict, db: Session = Depends(get_db)):
    """Update a single employee salary - matches C# updateEmployeeSalary endpoint"""
    try:
        updated_salary = EmployeeSalaryService.update_employee_salary(db, id, salary)
        if not updated_salary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salary not found"
            )
        return updated_salary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )