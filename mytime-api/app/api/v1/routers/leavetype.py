from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List  # Added List import here

from app.core.database import get_db
from app.schemas.leavetype_schemas import (
    LeaveTypeResponse,LeaveTypeDeleteResponse 
)
from app.services.leavetype_service import LeaveTypeService

#router = APIRouter()

router = APIRouter(
    prefix="/api/v1/leavetype",
    tags=["LeaveType"]
)

# Exact C# controller endpoints
from app.schemas.leavetype_schemas import LeaveTypeListResponse

@router.get("/fetchAllLeaveTypes", response_model=LeaveTypeListResponse)
async def fetch_all_leavetypes(db: Session = Depends(get_db)):
    try:
        leavetypes = LeaveTypeService.fetch_all_leavetypes(db)

        return {
            "total": len(leavetypes),
            "items": leavetypes,
            "page": 1,
            "size": len(leavetypes),
            "pages": 1
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    
@router.post("/InsertOrUpdateLeaveType")
async def insert_or_update_leavetype(leavetype: dict, db: Session = Depends(get_db)):
    """Insert or update leavetype - matches C# InsertOrUpdateLeaveType endpoint"""
    try:
       
        response = LeaveTypeService.insert_or_update_leavetype(db,leavetype)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/DeleteLeaveType/{id}", response_model=LeaveTypeDeleteResponse)
async def delete_leavetype(id: int, db: Session = Depends(get_db)):
    """Delete leavetype - matches C# DeleteLeaveType endpoint"""
    try:
       
       response=LeaveTypeService.delete_leavetype(db,id)
       if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
       return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/fetchLeaveType/{id}", response_model=LeaveTypeResponse)
async def fetch_leavetype(id: int, db: Session = Depends(get_db)):
    """Get leavetype by ID - matches C# fetchLeaveType endpoint"""
    try:
        leavetype = LeaveTypeService.fetch_leavetype(db, id)

        if not leavetype:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="LeaveType not found"
            )

        return leavetype

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )