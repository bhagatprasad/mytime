
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.leave_balance_model import LeaveBalance
from app.models.leavetype import LeaveType
from datetime import datetime


class LeaveBalanceService:
    """Service for Leave Balance operations"""

    @staticmethod
    def get_by_user(db: Session, user_id: int):
        try:
            balances = db.query(LeaveBalance).filter(
                LeaveBalance.UserId == user_id,
                LeaveBalance.IsActive == True
            ).all()

            if not balances:
                return {
                    "success": True,
                    "message": "No leave balance found for this user",
                    "data": []
                }

            return {
                "success": True,
                "message": "Leave balance fetched successfully",
                "data": balances
            }

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Error fetching leave balance"
            )

    @staticmethod
    def get_all(db: Session):
        try:
            balances = db.query(LeaveBalance)

            if not balances:
                return {
                    "success": True,
                    "message": "No leave balances found",
                    "data": []
                }

            return {
                "success": True,
                "message": "Leave balances fetched successfully",
                "data": balances
            }

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while fetching leave balances"
            )

    @staticmethod
    def update_balance(db: Session, user_id: int, leave_type_id: int, days: int):
        try:
            current_year = datetime.now().year

            balance = db.query(LeaveBalance).filter(
                LeaveBalance.UserId == user_id,
                LeaveBalance.LeaveTypeId == leave_type_id,
                LeaveBalance.Year == current_year,
                LeaveBalance.IsActive == True
            ).first()

            if not balance:
                leave_type = db.query(LeaveType).filter(
                    LeaveType.Id == leave_type_id
                ).first()

                if not leave_type:
                    raise HTTPException(
                        status_code=404,
                        detail="Leave type not found"
                    )

                max_leaves = leave_type.MaxDaysPerYear

                balance = LeaveBalance(
                    UserId=user_id,
                    LeaveTypeId=leave_type_id,
                    Year=current_year,
                    TotalLeaves=max_leaves,
                    UsedLeaves=0,
                    RemainingLeaves=max_leaves,
                    CreatedOn=datetime.utcnow(),
                    IsActive=True
                )

                db.add(balance)
                db.flush()  

            if balance.RemainingLeaves is None:
                balance.RemainingLeaves = 0

            if balance.UsedLeaves is None:
                balance.UsedLeaves = 0

            if days > balance.RemainingLeaves:
                raise HTTPException(
                    status_code=400,
                    detail="Leave balance exceeded"
                )

            balance.UsedLeaves += days
            balance.RemainingLeaves -= days
            balance.ModifiedOn = datetime.utcnow()

            db.commit()

            return {
                "success": True,
                "message": "Leave balance updated successfully",
                "data": {
                    "UserId": balance.UserId,
                    "LeaveTypeId": balance.LeaveTypeId,
                    "UsedLeaves": balance.UsedLeaves,
                    "RemainingLeaves": balance.RemainingLeaves
                }
            }

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error updating leave balance: {str(e)}"
            )