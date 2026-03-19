from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.attendence_schemas import (
    AttendenceCreate, AttendenceUpdate, AttendenceResponse,
    AttendenceListResponse, AttendenceExistsResponse,
    AttendenceDeleteResponse
)
from app.core.database import get_db
from app.services.attendence_service import AttendenceService

router = APIRouter()


# ✅ Fetch Single Attendence
@router.get("/fetchAttendence/{attendence_id}", response_model=AttendenceResponse)
async def fetch_attendence(attendence_id: int, db: Session = Depends(get_db)):
    try:
        attendence = AttendenceService.fetch_attendence(db, attendence_id)

        if not attendence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendence with ID {attendence_id} not found"
            )

        return attendence

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendence: {str(e)}"
        )


# ✅ Fetch All
@router.get("/fetchAllAttendence", response_model=List[AttendenceResponse])
async def fetch_all_attendence(db: Session = Depends(get_db)):
    try:
        return AttendenceService.fetch_all_attendence(db)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendence list: {str(e)}"
        )


# ✅ Pagination + Search
@router.get("/getAttendenceList", response_model=AttendenceListResponse)
async def get_attendence_list(
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


# ✅ Insert or Update
@router.post("/InsertOrUpdateAttendence")
async def insert_or_update_attendence(data: dict, db: Session = Depends(get_db)):
    try:
        response = AttendenceService.insert_or_update_attendence(db, data)

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
            detail=f"Error saving attendence: {str(e)}"
        )


# ✅ Delete
@router.delete("/DeleteAttendence/{attendence_id}", response_model=AttendenceDeleteResponse)
async def delete_attendence(attendence_id: int, db: Session = Depends(get_db)):
    try:
        response = AttendenceService.delete_attendence(db, attendence_id)

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
            detail=f"Error deleting attendence: {str(e)}"
        )


# ✅ Create (Strict Schema)
@router.post("/createAttendence", response_model=AttendenceResponse)
async def create_attendence(attendence: AttendenceCreate, db: Session = Depends(get_db)):
    try:
        return AttendenceService.create_attendence(db, attendence)

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating attendence: {str(e)}"
        )


# ✅ Update
@router.put("/updateAttendence/{attendence_id}", response_model=AttendenceResponse)
async def update_attendence(
    attendence_id: int,
    attendence: AttendenceUpdate,
    db: Session = Depends(get_db)
):
    try:
        updated = AttendenceService.update_attendence(db, attendence_id, attendence)

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendence not found"
            )

        return updated

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating attendence: {str(e)}"
        )


# ✅ Approve
@router.put("/approveAttendence/{attendence_id}")
async def approve_attendence(
    attendence_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = AttendenceService.approve_attendence(db, attendence_id, user_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendence not found"
            )

        return {"message": "Attendence approved successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error approving attendence: {str(e)}"
        )


# ✅ Reject
@router.put("/rejectAttendence/{attendence_id}")
async def reject_attendence(
    attendence_id: int,
    user_id: int,
    reason: str,
    db: Session = Depends(get_db)
):
    try:
        result = AttendenceService.reject_attendence(
            db, attendence_id, user_id, reason
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendence not found"
            )

        return {"message": "Attendence rejected successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rejecting attendence: {str(e)}"
        )