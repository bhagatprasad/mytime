from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.leave_schema import (
    LeaveApply, LeaveApprove, LeaveReject, LeaveCancel,
    LeaveResponse, LeaveListResponse
)
from app.services.leave_service import LeaveService

router = APIRouter()

@router.get("/fetchtypes")
async def get_leave_types(db: Session = Depends(get_db)):
    """Get all active leave types for dropdown"""
    try:
        return LeaveService.get_leave_types(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching leave types: {str(e)}"
        )

@router.post("/applyleave")
async def apply_leave(
    data: LeaveApply,
    db: Session = Depends(get_db)
):
    """Apply for new leave"""
    try:
        return LeaveService.apply_leave(data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error applying leave: {str(e)}"
        )

@router.get("/fetchleavesbyuser/{user_id}", response_model=List[LeaveResponse])
async def get_my_leaves(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all leaves for a specific user"""
    try:
        return LeaveService.get_user_leaves(user_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user leaves: {str(e)}"
        )

@router.get("/fetchallleaves", response_model=List[LeaveResponse])
async def get_admin_requests(
    status_filter: Optional[str] = Query(None, regex="^(Pending|Approved|Rejected|Cancelled)$"),
    db: Session = Depends(get_db)
):
    """Get all leave requests for admin (with optional status filter)"""
    try:
        requests = LeaveService.get_admin_requests(db)
        if status_filter:
            requests = [r for r in requests if r.Status == status_filter]
        return requests
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching admin requests: {str(e)}"
        )

@router.get("/fetchleave/{id}", response_model=LeaveResponse)
async def get_leave_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    """Get leave request by ID"""
    try:
        leave = LeaveService.get_leave_by_id(id, db)
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )
        return leave
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching leave: {str(e)}"
        )

@router.put("/approveleave/{id}")
async def approve_leave(
    id: int,
    data: LeaveApprove,
    db: Session = Depends(get_db)
):
    """Approve leave request"""
    try:
        return LeaveService.approve_leave(id, data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error approving leave: {str(e)}"
        )

@router.put("/rejectleave/{id}")
async def reject_leave(
    id: int,
    data: LeaveReject,
    db: Session = Depends(get_db)
):
    """Reject leave request"""
    try:
        return LeaveService.reject_leave(id, data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rejecting leave: {str(e)}"
        )

@router.put("/cancelleave/{id}")
async def cancel_leave(
    id: int,
    data: LeaveCancel,
    db: Session = Depends(get_db)
):
    """Cancel leave request"""
    try:
        return LeaveService.cancel_leave(id, data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cancelling leave: {str(e)}"
        )

@router.get("/statistics")
async def get_leave_statistics(
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get leave statistics (overall or for specific user)"""
    try:
        return LeaveService.get_leave_statistics(user_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}"
        )