from sqlalchemy import case
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.models.leave_request import LeaveRequest
from app.models.leavetype import LeaveType
from app.models.leave_balance_model import LeaveBalance  
from app.schemas.leave_schema import LeaveApply, LeaveApprove, LeaveReject, LeaveCancel


class LeaveService:
    """Service for Leave operations"""

    @staticmethod
    def get_leave_types(db: Session) -> List[LeaveType]:
        return db.query(LeaveType).filter(LeaveType.IsActive == True).all()


    @staticmethod
    def apply_leave(data: LeaveApply, db: Session) -> Dict[str, Any]:
        """Apply for new leave"""
        try:
            if data.fromDate > data.toDate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="From date cannot be greater than to date"
                )

            total_days = (data.toDate - data.fromDate).days + 1

            leave_type = db.query(LeaveType).filter(
                LeaveType.Id == data.leaveTypeId,
                LeaveType.IsActive == True
            ).first()

            if not leave_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Leave type not found or inactive"
                )

            
            current_year = datetime.now().year

            balance = db.query(LeaveBalance).filter(
                LeaveBalance.UserId == data.userId,
                LeaveBalance.LeaveTypeId == data.leaveTypeId,
                LeaveBalance.Year == current_year
            ).first()
            
            if balance:
                if balance.RemainingLeaves <= 0:
                    raise HTTPException(
                        status_code=400,
                        detail="No leave balance available"
                    )

                if total_days > balance.RemainingLeaves:
                    raise HTTPException(
                        status_code=400,
                        detail="Requested days exceed remaining leave balance"
                    )
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
                case(
                    (LeaveRequest.Status == "Pending", 0),  # Pending first
                    else_=1
                ),
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
        """Approve leave with balance validation"""
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

            from app.services.leave_balance_service import LeaveBalanceService

            result = LeaveBalanceService.update_balance(
                db,
                leave.UserId,
                leave.LeaveTypeId,
                leave.TotalDays
            )

            if not result["success"]:
                return {
                    "success": False,
                    "message": result["message"]
                }

            leave.Status = "Approved"
            leave.AdminComment = data.adminComment
            leave.ModifiedOn = datetime.utcnow()

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
            # leave.ModifiedBy = data.adminId  

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