from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.leave_models import LeaveRequest, LeaveType


def get_leave_types(db: Session):

    types = db.query(LeaveType).filter(LeaveType.IsActive == True).all()

    return types


def apply_leave(data, db: Session):

    try:

        total_days = (data.toDate - data.fromDate).days + 1

        leave = LeaveRequest(
            UserId=data.userId,
            LeaveTypeId=data.leaveTypeId,
            FromDate=data.fromDate,
            ToDate=data.toDate,
            TotalDays=total_days,
            Reason=data.reason,
            Description=data.description,
            Status="Pending",
            CreatedBy=data.userId,
            CreatedOn=datetime.utcnow(),
            IsActive=True
        )

        db.add(leave)
        db.commit()
        db.refresh(leave)

        return {"message": "Leave applied successfully"}

    except Exception as e:

        db.rollback()

        raise HTTPException(status_code=500, detail=str(e))


def get_user_leaves(user_id: int, db: Session):

    leaves = db.query(LeaveRequest).filter(
        LeaveRequest.UserId == user_id,
        LeaveRequest.IsActive == True
    ).all()

    return leaves


def get_admin_requests(db: Session):

    requests = db.query(LeaveRequest).filter(
        LeaveRequest.IsActive == True
    ).all()

    return requests


def approve_leave(id: int, data, db: Session):

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.Id == id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.Status = "Approved"
    leave.AdminComment = data.adminComment
    leave.ModifiedOn = datetime.utcnow()

    db.commit()

    return {"message": "Leave approved"}


def reject_leave(id: int, data, db: Session):

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.Id == id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.Status = "Rejected"
    leave.AdminComment = data.adminComment
    leave.ModifiedOn = datetime.utcnow()

    db.commit()

    return {"message": "Leave rejected"}


def cancel_leave(id: int, data, db: Session):

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.Id == id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.Status = "Cancelled"
    leave.CancelReason = data.cancelReason
    leave.ModifiedOn = datetime.utcnow()

    db.commit()

    return {"message": "Leave cancelled"}