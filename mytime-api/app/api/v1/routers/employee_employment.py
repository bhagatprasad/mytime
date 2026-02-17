from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.schemas.employee_employment_schemas import (
    EmployeeEmploymentResponse,
    EmployeeEmploymentDeleteResponse
   )
from app.core.database import get_db
from app.services.employee_employment_service import EmployeeEmploymentService

router = APIRouter()


@router.get("/fetchEmployeeEmployment/{employee_employment_id}", response_model=EmployeeEmploymentResponse)
async def fetch_employee_employment(employee_employment_id: int, db: Session = Depends(get_db)):
    """Get employee employment by ID"""
    try:
        employment = EmployeeEmploymentService.fetch_employee_employment(db, employee_employment_id)
        if not employment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee employment record with ID {employee_employment_id} not found"
            )
        return employment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee employment record: {str(e)}"
        )


@router.get("/fetchEmploymentsByEmployee/{employee_id}", response_model=List[EmployeeEmploymentResponse])
async def fetch_employments_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get all employment records for a specific employee"""
    try:
        employments = EmployeeEmploymentService.fetch_employments_by_employee(db, employee_id)
        return employments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employment records for employee: {str(e)}"
        )


@router.get("/fetchActiveEmploymentsByEmployee/{employee_id}", response_model=List[EmployeeEmploymentResponse])
async def fetch_active_employments_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get active employment records for a specific employee"""
    try:
        employments = EmployeeEmploymentService.fetch_active_employments_by_employee(db, employee_id)
        return employments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active employment records for employee: {str(e)}"
        )


@router.get("/fetchLatestEmploymentByEmployee/{employee_id}", response_model=Optional[EmployeeEmploymentResponse])
async def fetch_latest_employment_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get latest employment record for an employee"""
    try:
        employment = EmployeeEmploymentService.fetch_latest_employment_by_employee(db, employee_id)
        return employment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching latest employment for employee: {str(e)}"
        )

@router.post("/InsertOrUpdateEmployeeEmployment")
async def insert_or_update_employee_employment(employment: dict, db: Session = Depends(get_db)):
    """Insert or update employee employment record"""
    try:
        response = EmployeeEmploymentService.insert_or_update_employee_employment(db, employment)
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
            detail=f"Error saving employee employment record: {str(e)}"
        )


@router.delete("/DeleteEmployeeEmployment/{employee_employment_id}", response_model=EmployeeEmploymentDeleteResponse)
async def delete_employee_employment(employee_employment_id: int, db: Session = Depends(get_db)):
    """Delete employee employment record"""
    try:
        response = EmployeeEmploymentService.delete_employee_employment(db, employee_employment_id)
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
            detail=f"Error deleting employee employment record: {str(e)}"
        )