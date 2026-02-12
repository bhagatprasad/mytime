from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.schemas.employee_employment_schemas import (
    EmployeeEmploymentCreate, EmployeeEmploymentUpdate, EmployeeEmploymentResponse,
    EmployeeEmploymentListResponse, EmployeeEmploymentExistsResponse,
    EmployeeEmploymentDeleteResponse, EmployeeEmploymentCreateResponse,
    EmployeeEmploymentUpdateResponse, EmployeeEmploymentBulkCreate,
    EmployeeEmploymentFilterParams, EmployeeEmploymentWithDetailsResponse,
    EmployeeEmploymentStatistics
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


@router.get("/getEmployeeEmployments", response_model=EmployeeEmploymentListResponse)
async def get_employee_employments(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    company_name: Optional[str] = Query(None, description="Filter by company name"),
    designation: Optional[str] = Query(None, description="Filter by designation"),
    start_year_from: Optional[int] = Query(None, ge=1900, le=2100, description="Start year from"),
    start_year_to: Optional[int] = Query(None, ge=1900, le=2100, description="Start year to"),
    end_year_from: Optional[int] = Query(None, ge=1900, le=2100, description="End year from"),
    end_year_to: Optional[int] = Query(None, ge=1900, le=2100, description="End year to"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("EmployeeEmploymentId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated employee employment records with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeEmploymentService.get_employee_employments_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            employee_id=employee_id,
            company_name=company_name,
            designation=designation,
            start_year_from=start_year_from,
            start_year_to=start_year_to,
            end_year_from=end_year_from,
            end_year_to=end_year_to,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pages = (total + size - 1) // size  # Ceiling division
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "size": size,
            "pages": pages
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee employment records: {str(e)}"
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


@router.get("/getEmployeeEmploymentSummary/{employee_id}", response_model=dict)
async def get_employee_employment_summary(employee_id: int, db: Session = Depends(get_db)):
    """Get employment summary for an employee"""
    try:
        summary = EmployeeEmploymentService.get_employee_employment_summary(db, employee_id)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employment summary: {str(e)}"
        )