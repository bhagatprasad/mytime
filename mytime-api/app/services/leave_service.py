from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from typing import List, Optional, Dict, Any

from app.models.leave_request import LeaveRequest
from app.models.leavetype import LeaveType
from app.schemas.leave_schema import LeaveApply, LeaveApprove, LeaveReject, LeaveCancel

class LeaveService:
    """Service for Leave operations - matching C# controller functionality"""
    
    @staticmethod
    def get_leave_types(db: Session) -> List[LeaveType]:
        """Get all active leave types for dropdown"""
        return db.query(LeaveType).filter(LeaveType.IsActive == True).all()

    @staticmethod
    def apply_leave(data: LeaveApply, db: Session) -> Dict[str, Any]:
        """Apply for new leave"""
        try:
            # Validate dates
            if data.fromDate > data.toDate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="From date cannot be greater than to date"
                )
            
            # Calculate total days
            total_days = (data.toDate - data.fromDate).days + 1
            
            # Check if leave type exists and is active
            leave_type = db.query(LeaveType).filter(
                LeaveType.Id == data.leaveTypeId,
                LeaveType.IsActive == True
            ).first()
            
            if not leave_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Leave type not found or inactive"
                )
            
            # Check for overlapping leaves
            overlapping = db.query(LeaveRequest).filter(
                LeaveRequest.UserId == data.userId,
                LeaveRequest.IsActive == True,
                LeaveRequest.Status.in_(["Pending", "Approved"]),
                LeaveRequest.FromDate <= data.toDate,
                LeaveRequest.ToDate >= data.fromDate
            ).first()
            
            if overlapping:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You already have a leave request for this period"
                )
            
            # Create leave request
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

            return {
                "success": True,
                "message": "Leave applied successfully",
                "data": leave
            }

        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error applying leave: {str(e)}"
            )

    @staticmethod
    def get_user_leaves(user_id: int, db: Session) -> List[LeaveRequest]:
        """Get all leaves for a specific user"""
        try:
            leaves = db.query(LeaveRequest).filter(
                LeaveRequest.UserId == user_id,
                LeaveRequest.IsActive == True
            ).order_by(LeaveRequest.CreatedOn.desc()).all()
            
            return leaves
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching user leaves: {str(e)}"
            )

    @staticmethod
    def get_admin_requests(db: Session) -> List[LeaveRequest]:
        """Get all leave requests for admin (pending first)"""
        try:
            requests = db.query(LeaveRequest).filter(
                LeaveRequest.IsActive == True
            ).order_by(
                # Pending first, then by created date
                LeaveRequest.Status == "Pending",
                LeaveRequest.CreatedOn.desc()
            ).all()
            
            return requests
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching admin requests: {str(e)}"
            )

    @staticmethod
    def get_leave_by_id(leave_id: int, db: Session) -> Optional[LeaveRequest]:
        """Get leave request by ID"""
        return db.query(LeaveRequest).filter(
            LeaveRequest.Id == leave_id,
            LeaveRequest.IsActive == True
        ).first()

    @staticmethod
    def approve_leave(leave_id: int, data: LeaveApprove, db: Session) -> Dict[str, Any]:
        """Approve leave request"""
        try:
            leave = db.query(LeaveRequest).filter(
                LeaveRequest.Id == leave_id,
                LeaveRequest.IsActive == True
            ).first()

            if not leave:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Leave request not found"
                )

            if leave.Status != "Pending":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Leave request is already {leave.Status}"
                )

            leave.Status = "Approved"
            leave.AdminComment = data.adminComment
            leave.ModifiedOn = datetime.utcnow()
            leave.ModifiedBy = data.adminComment  # You might want to pass current user ID

            db.commit()
            db.refresh(leave)

            return {
                "success": True,
                "message": "Leave approved successfully",
                "data": leave
            }

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error approving leave: {str(e)}"
            )

    @staticmethod
    def reject_leave(leave_id: int, data: LeaveReject, db: Session) -> Dict[str, Any]:
        """Reject leave request"""
        try:
            leave = db.query(LeaveRequest).filter(
                LeaveRequest.Id == leave_id,
                LeaveRequest.IsActive == True
            ).first()

            if not leave:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Leave request not found"
                )

            if leave.Status != "Pending":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Leave request is already {leave.Status}"
                )

            leave.Status = "Rejected"
            leave.AdminComment = data.adminComment
            leave.ModifiedOn = datetime.utcnow()
            leave.ModifiedBy = data.adminComment  # You might want to pass current user ID

            db.commit()
            db.refresh(leave)

            return {
                "success": True,
                "message": "Leave rejected successfully",
                "data": leave
            }

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error rejecting leave: {str(e)}"
            )

    @staticmethod
    def cancel_leave(leave_id: int, data: LeaveCancel, db: Session) -> Dict[str, Any]:
        """Cancel leave request (by user)"""
        try:
            leave = db.query(LeaveRequest).filter(
                LeaveRequest.Id == leave_id,
                LeaveRequest.IsActive == True
            ).first()

            if not leave:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Leave request not found"
                )

            if leave.Status not in ["Pending", "Approved"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot cancel leave with status: {leave.Status}"
                )

            leave.Status = "Cancelled"
            leave.CancelReason = data.cancelReason
            leave.ModifiedOn = datetime.utcnow()

            db.commit()
            db.refresh(leave)

            return {
                "success": True,
                "message": "Leave cancelled successfully",
                "data": leave
            }

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error cancelling leave: {str(e)}"
            )

    @staticmethod
    def get_leave_statistics(user_id: Optional[int] = None, db: Session = None) -> Dict[str, Any]:
        """Get leave statistics for user or overall"""
        try:
            query = db.query(LeaveRequest).filter(LeaveRequest.IsActive == True)
            
            if user_id:
                query = query.filter(LeaveRequest.UserId == user_id)
            
            total = query.count()
            pending = query.filter(LeaveRequest.Status == "Pending").count()
            approved = query.filter(LeaveRequest.Status == "Approved").count()
            rejected = query.filter(LeaveRequest.Status == "Rejected").count()
            cancelled = query.filter(LeaveRequest.Status == "Cancelled").count()
            
            return {
                "total": total,
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
                "cancelled": cancelled
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching leave statistics: {str(e)}"
            )