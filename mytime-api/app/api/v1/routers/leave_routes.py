from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.leave_models import LeaveRequest
from app.schemas.leave_schema import LeaveApply, LeaveApprove, LeaveCancel, LeaveReject
from app.services import leave_service

router = APIRouter(prefix="/leaves", tags=["Leaves"])



@router.get("/types")

def get_leave_types(db: Session = Depends(get_db)):

    return leave_service.get_leave_types(db)


# @router.get("/leaverequest")
# def get_leave_request(db: Session = Depends(get_db)):
#     """
#     Get all leave types
#     """
#     leave_request = leave_service.get_all_leaves(db)
#     return leave_request


@router.post("/apply")

def apply_leave(data: LeaveApply, db: Session = Depends(get_db)):

    return leave_service.apply_leave(data, db)


@router.get("/user/{user_id}")

def get_my_leaves(user_id: int, db: Session = Depends(get_db)):

    return leave_service.get_user_leaves(user_id, db)


@router.get("/admin")

def get_admin_requests(db: Session = Depends(get_db)):

    return leave_service.get_admin_requests(db)


@router.put("/approve/{id}")

def approve_leave(id: int, data: LeaveApprove, db: Session = Depends(get_db)):

    return leave_service.approve_leave(id, data, db)


@router.put("/reject/{id}")

def reject_leave(id: int, data: LeaveReject, db: Session = Depends(get_db)):

    return leave_service.reject_leave(id, data, db)


@router.put("/cancel/{id}")

def cancel_leave(id: int, data: LeaveCancel, db: Session = Depends(get_db)):

    return leave_service.cancel_leave(id, data, db)