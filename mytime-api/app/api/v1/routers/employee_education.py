from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.schemas.employee_education_schemas import (
     EmployeeEducationResponse,
        EmployeeEducationDeleteResponse
        )
from app.core.database import get_db
from app.services.employee_education_service import EmployeeEducationService

router = APIRouter()


@router.get("/fetchEmployeeEducation/{employee_education_id}", response_model=EmployeeEducationResponse)
async def fetch_employee_education(employee_education_id: int, db: Session = Depends(get_db)):
    """Get employee education by ID"""
    try:
        education = EmployeeEducationService.fetch_employee_education(db, employee_education_id)
        if not education:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee education record with ID {employee_education_id} not found"
            )
        return education
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee education record: {str(e)}"
        )


@router.get("/fetchEducationsByEmployee/{employee_id}", response_model=List[EmployeeEducationResponse])
async def fetch_educations_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get all education records for a specific employee"""
    try:
        educations = EmployeeEducationService.fetch_educations_by_employee(db, employee_id)
        return educations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching education records for employee: {str(e)}"
        )


@router.post("/InsertOrUpdateEmployeeEducation")
async def insert_or_update_employee_education(education: dict, db: Session = Depends(get_db)):
    """Insert or update employee education record"""
    try:
        response = EmployeeEducationService.insert_or_update_employee_education(db, education)
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
            detail=f"Error saving employee education record: {str(e)}"
        )


@router.delete("/DeleteEmployeeEducation/{employee_education_id}", response_model=EmployeeEducationDeleteResponse)
async def delete_employee_education(employee_education_id: int, db: Session = Depends(get_db)):
    """Delete employee education record"""
    try:
        response = EmployeeEducationService.delete_employee_education(db, employee_education_id)
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
            detail=f"Error deleting employee education record: {str(e)}"
        )