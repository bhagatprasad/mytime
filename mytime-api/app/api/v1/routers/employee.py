from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.schemas.employee_schemas import (
    EmployeeResponse,
    EmployeeDeleteResponse
)
from app.core.database import get_db
from app.services.employee_service import EmployeeService

router = APIRouter()


@router.get("/fetchEmployee/{employee_id}", response_model=EmployeeResponse)
async def fetch_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get employee by ID"""
    try:
        employee = EmployeeService.fetch_employee(db, employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee: {str(e)}"
        )

@router.get("/fetchAllEmployees", response_model=List[EmployeeResponse])
async def fetch_all_employees(db: Session = Depends(get_db)):
    """Get all employees"""
    try:
        employees = EmployeeService.fetch_all_employees(db)
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employees: {str(e)}"
        )

@router.post("/InsertOrUpdateEmployee")
async def insert_or_update_employee(employee: dict, db: Session = Depends(get_db)):
    """Insert or update employee"""
    try:
        response = EmployeeService.insert_or_update_employee(db, employee)
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
            detail=f"Error saving employee: {str(e)}"
        )


@router.delete("/DeleteEmployee/{employee_id}", response_model=EmployeeDeleteResponse)
async def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete employee"""
    try:
        response = EmployeeService.delete_employee(db, employee_id)
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
            detail=f"Error deleting employee: {str(e)}"
        )