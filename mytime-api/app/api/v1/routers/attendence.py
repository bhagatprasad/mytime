from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.schemas.attendence_schemas import (
    AttendenceCreate,
    AttendenceUpdate,
    AttendenceResponse,
    AttendenceListResponse,
    AttendenceExistsResponse,
    AttendenceDeleteResponse
)
from app.core.database import get_db
from app.services.attendence_service import AttendenceService

router = APIRouter(prefix="/attendence", tags=["Attendence"])

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
        return attendence
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendence: {str(e)}"
        )

# Fetch All Attendence
@router.get("/fetchAll", response_model=List[AttendenceResponse])
def fetch_all_attendence(db: Session = Depends(get_db)):
    try:
        return AttendenceService.fetch_all_attendence(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendence list: {str(e)}"
        )

# Pagination + Search
@router.get("/list", response_model=AttendenceListResponse)
def get_attendence_with_pagination(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    employee_id: Optional[int] = None,
    status_param: Optional[str] = Query(None, alias="status"),
    approval_status: Optional[str] = None,
    sort_by: str = "AttendenceId",
    sort_order: str = "desc",
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
        pages = (total // limit) + (1 if total % limit > 0 else 0)
        return AttendenceListResponse(
            total=total,
            items=items,
            page=(skip // limit) + 1,
            size=limit,
            pages=pages
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendence list: {str(e)}"
        )

# Create Attendence
@router.post("/create", response_model=AttendenceResponse)
def create_attendence(attendence: AttendenceCreate, db: Session = Depends(get_db)):
    try:
        return AttendenceService.create_attendence(db, attendence)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating attendence: {str(e)}"
        )

# Update Attendence
@router.put("/update/{attendence_id}", response_model=AttendenceResponse)
def update_attendence(attendence_id: int, attendence: AttendenceUpdate, db: Session = Depends(get_db)):
    try:
        updated = AttendenceService.update_attendence(db, attendence_id, attendence)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendence not found"
            )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating attendence: {str(e)}"
        )

# Check if Attendence Exists
@router.get("/exists/{attendence_id}", response_model=AttendenceExistsResponse)
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
@router.delete("/delete/{attendence_id}", response_model=AttendenceDeleteResponse)
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
@router.put("/approve/{attendence_id}")
def approve_attendence(attendence_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        result = AttendenceService.approve_attendence(db, attendence_id, user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Attendence not found")
        return {"message": "Attendence approved successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error approving attendence: {str(e)}"
        )

# Reject Attendence
@router.put("/reject/{attendence_id}")
def reject_attendence(attendence_id: int, user_id: int, reason: str, db: Session = Depends(get_db)):
    try:
        result = AttendenceService.reject_attendence(db, attendence_id, user_id, reason)
        if not result:
            raise HTTPException(status_code=404, detail="Attendence not found")
        return {"message": "Attendence rejected successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rejecting attendence: {str(e)}"
        )