from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.department_schemas import (
     DepartmentResponse, 
     DepartmentDeleteResponse
)
from app.core.database import get_db
from app.services.department_service import DepartmentService

router = APIRouter()


@router.get("/fetchDepartment/{department_id}", response_model=DepartmentResponse)
async def fetch_department(department_id: int, db: Session = Depends(get_db)):
    """Get department by ID"""
    try:
        department = DepartmentService.fetch_department(db, department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {department_id} not found"
            )
        return department
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching department: {str(e)}"
        )


@router.get("/fetchAllDepartments", response_model=List[DepartmentResponse])
async def fetch_all_departments(db: Session = Depends(get_db)):
    """Get all departments"""
    try:
        departments = DepartmentService.fetch_all_departments(db)
        return departments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching departments: {str(e)}"
        )

@router.post("/InsertOrUpdateDepartment")
async def insert_or_update_department(department: dict, db: Session = Depends(get_db)):
    """Insert or update department"""
    try:
        response = DepartmentService.insert_or_update_department(db, department)
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
            detail=f"Error saving department: {str(e)}"
        )


@router.delete("/DeleteDepartment/{department_id}", response_model=DepartmentDeleteResponse)
async def delete_department(department_id: int, db: Session = Depends(get_db)):
    """Delete department"""
    try:
        response = DepartmentService.delete_department(db, department_id)
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
            detail=f"Error deleting department: {str(e)}"
        )