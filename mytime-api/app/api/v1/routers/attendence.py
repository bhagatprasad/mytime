from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, date

from app.schemas.attendence_schemas import (
    AttendenceResponse,
    AttendenceListResponse,
    AttendenceExistsResponse,
    AttendenceDeleteResponse,
    AttendenceOperationResponse
)
from app.core.database import get_db
from app.services.attendence_service import AttendenceService

router = APIRouter()


# Fetch Single Attendence
@router.get("/fetch/{attendence_id}", response_model=AttendenceResponse)
def fetch_attendence(attendence_id: int, db: Session = Depends(get_db)):
    try:
        attendence = AttendenceService.fetch_attendence(db, attendence_id)
        if not attendence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendence with ID {attendence_id} not found"
            )
        # Convert SQLAlchemy model to Pydantic schema
        return AttendenceResponse.model_validate(attendence)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendence: {str(e)}"
        )


# Fetch Attendence by Employee
@router.get("/fetchattendencebyemployee/{employee_id}", response_model=List[AttendenceResponse])
def fetch_attendence_by_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        attendence_list = AttendenceService.fetch_attendence_by_employee(db, employee_id)
        # Convert SQLAlchemy models to Pydantic schemas
        return [AttendenceResponse.model_validate(item) for item in attendence_list]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendence: {str(e)}"
        )


# Fetch All Attendence
@router.get("/fetchAll", response_model=List[AttendenceResponse])
def fetch_all_attendence(db: Session = Depends(get_db)):
    try:
        attendence_list = AttendenceService.fetch_all_attendence(db)
        # Convert SQLAlchemy models to Pydantic schemas
        return [AttendenceResponse.model_validate(item) for item in attendence_list]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendence list: {str(e)}"
        )


# Pagination + Search
@router.get("/list", response_model=AttendenceListResponse)
def get_attendence_with_pagination(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    search: Optional[str] = Query(None, description="Search term"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    status_param: Optional[str] = Query(None, alias="status", description="Filter by status"),
    approval_status: Optional[str] = Query(None, description="Filter by approval status"),
    sort_by: str = Query("AttendenceId", description="Sort by field"),
    sort_order: str = Query("desc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db)
):
    try:
        items, total = AttendenceService.get_attendence_with_pagination(
            db,
            skip=skip,
            limit=limit,
            search=search,
            employee_id=employee_id,
            status=status_param,
            approval_status=approval_status,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Convert SQLAlchemy models to Pydantic schemas
        response_items = [AttendenceResponse.model_validate(item) for item in items]
        
        pages = (total // limit) + (1 if total % limit > 0 else 0)
        current_page = (skip // limit) + 1
        
        return AttendenceListResponse(
            total=total,
            items=response_items,
            page=current_page,
            size=limit,
            pages=pages
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendence list: {str(e)}"
        )


# Insert or Update Attendence
@router.post("/insert_or_update_attendence", response_model=AttendenceOperationResponse)
def insert_or_update_attendence(
    attendence: dict,
    db: Session = Depends(get_db)
):
    try:
        result = AttendenceService.insert_or_update_attendence(db, attendence)

        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("message")
            )

        # Convert the SQLAlchemy model to Pydantic schema if data exists
        if result.get("data"):
            result["data"] = AttendenceResponse.model_validate(result["data"])

        return AttendenceOperationResponse(**result)

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving attendence: {str(e)}"
        )


# Check if Attendence Exists
@router.get("/check_attendence_exists/{attendence_id}", response_model=AttendenceExistsResponse)
def check_attendence_exists(attendence_id: int, db: Session = Depends(get_db)):
    try:
        exists = AttendenceService.exists(db, attendence_id)
        return AttendenceExistsResponse(exists=exists)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking attendence existence: {str(e)}"
        )


# Delete Attendence
@router.delete("/delete_attendence/{attendence_id}", response_model=AttendenceDeleteResponse)
def delete_attendence(attendence_id: int, db: Session = Depends(get_db)):
    try:
        success, message = AttendenceService.delete_attendence(db, attendence_id)
        if not success:
            raise HTTPException(status_code=404, detail=message)
        return AttendenceDeleteResponse(success=success, message=message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting attendence: {str(e)}"
        )


# Approve Attendence
@router.put("/approve_attendence/{attendence_id}", response_model=AttendenceResponse)
def approve_attendence(
    attendence_id: int, 
    user_id: int, 
    db: Session = Depends(get_db)
):
    try:
        result = AttendenceService.approve_attendence(db, attendence_id, user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Attendence not found")
        # Convert to response schema
        return AttendenceResponse.model_validate(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error approving attendence: {str(e)}"
        )


# Reject Attendence
@router.put("/reject_attendence/{attendence_id}", response_model=AttendenceResponse)
def reject_attendence(
    attendence_id: int, 
    user_id: int, 
    reason: str, 
    db: Session = Depends(get_db)
):
    try:
        result = AttendenceService.reject_attendence(db, attendence_id, user_id, reason)
        if not result:
            raise HTTPException(status_code=404, detail="Attendence not found")
        # Convert to response schema
        return AttendenceResponse.model_validate(result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rejecting attendence: {str(e)}"
        )


# Get Attendence by Date Range
@router.get("/get_attendence_by_date_range", response_model=List[AttendenceResponse])
def get_attendence_by_date_range(
    employee_id: int,
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db)
):
    try:
        result = AttendenceService.get_attendence_by_date_range(db, employee_id, from_date, to_date)
        # Convert SQLAlchemy models to Pydantic schemas
        return [AttendenceResponse.model_validate(item) for item in result]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting attendence by date range: {str(e)}"
        )