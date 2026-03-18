# routers/leave_balance_router.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.leave_balance_service import LeaveBalanceService
from app.schemas.leave_balance_schemas import LeaveBalanceResponse

router = APIRouter()

@router.get("/fetchleavebalancebyuser/{user_id}", response_model=List[LeaveBalanceResponse])
async def get_leave_balance(user_id: int, db: Session = Depends(get_db)):
    try:
        result = LeaveBalanceService.get_by_user(db, user_id)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )

        return result["data"] 

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching leave balance: {str(e)}"
        )
        
@router.get("/fetallleavebalance", response_model=List[LeaveBalanceResponse])
async def get_all_balances(db: Session = Depends(get_db)):
    try:
        result = LeaveBalanceService.get_all(db)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )

        return result["data"]

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching all leave balances: {str(e)}"
        )        
        