from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from decimal import Decimal

from app.models.employee_salary_structure import EmployeeSalaryStructure
from app.schemas.employee_salary_structure_schemas import (
    EmployeeSalaryStructureResponse,
    EmployeeSalaryStructureDeleteResponse
)
from app.core.database import get_db
from app.services.employee_salary_structure_service import EmployeeSalaryStructureService

router = APIRouter()


@router.get("/fetchEmployeeSalaryStructure/{employee_salary_structure_id}", response_model=EmployeeSalaryStructureResponse)
async def fetch_employee_salary_structure(employee_salary_structure_id: int, db: Session = Depends(get_db)):
    """Get employee salary structure by ID"""
    try:
        salary = EmployeeSalaryStructureService.fetch_employee_salary_structure(db, employee_salary_structure_id)
        if not salary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee salary structure with ID {employee_salary_structure_id} not found"
            )
        return salary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee salary structure: {str(e)}"
        )


@router.get("/fetchSalaryStructureByEmployee/{employee_id}", response_model=Optional[EmployeeSalaryStructureResponse])
async def fetch_salary_structure_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get salary structure for a specific employee"""
    try:
        salary = EmployeeSalaryStructureService.fetch_salary_structure_by_employee(db, employee_id)
        return salary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching salary structure for employee: {str(e)}"
        )

@router.get("/fetchAllEmployeeSalaryStructures", response_model=List[EmployeeSalaryStructureResponse])
async def fetch_all_employee_salary_structures(db: Session = Depends(get_db)):
    """Get all employee salary structures"""
    try:
        salaries = EmployeeSalaryStructureService.fetch_all_employee_salary_structures(db)
        return salaries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching all employee salary structures: {str(e)}"
        )

@router.post("/InsertOrUpdateEmployeeSalaryStructure")
async def insert_or_update_employee_salary_structure(salary: dict, db: Session = Depends(get_db)):
    """Insert or update employee salary structure"""
    try:
        response = EmployeeSalaryStructureService.insert_or_update_employee_salary_structure(db, salary)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving employee salary structure: {str(e)}"
        )


@router.delete("/DeleteEmployeeSalaryStructure/{employee_salary_structure_id}", response_model=EmployeeSalaryStructureDeleteResponse)
async def delete_employee_salary_structure(employee_salary_structure_id: int, db: Session = Depends(get_db)):
    """Delete employee salary structure"""
    try:
        response = EmployeeSalaryStructureService.delete_employee_salary_structure(db, employee_salary_structure_id)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting employee salary structure: {str(e)}"
        )