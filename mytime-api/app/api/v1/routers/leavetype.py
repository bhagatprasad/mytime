from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.schemas.leavetype_schemas import (
    LeaveTypeResponse, LeaveTypeCreate, LeaveTypeUpdate,
    LeaveTypeDeleteResponse, LeaveTypeListResponse,
    LeaveTypeExistsResponse
)
from app.services.leavetype_service import LeaveTypeService

router = APIRouter()

@router.get("/fetchLeaveType/{id}", response_model=LeaveTypeResponse)
async def fetch_leavetype(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Get leave type by ID
    Matches C# fetchLeaveType endpoint
    """
    try:
        leavetype = LeaveTypeService.fetch_leavetype(db, id)

        if not leavetype:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="LeaveType not found"
            )

        return leavetype

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching leave type: {str(e)}"
        )

@router.post("/InsertOrUpdateLeaveType")
async def insert_or_update_leavetype(
    leavetype: dict,
    db: Session = Depends(get_db)
):
    """
    Insert or update leave type
    Matches C# InsertOrUpdateLeaveType endpoint
    """
    try:
        # Validate required fields for new records
        if not leavetype.get('Id') and not leavetype.get('Name'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name is required for new leave types"
            )
        
        # Check for duplicate name if name is provided
        if leavetype.get('Name'):
            exists = LeaveTypeService.check_leavetype_exists(
                db, 
                leavetype['Name'], 
                exclude_id=leavetype.get('Id')
            )
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Leave type with this name already exists"
                )
        
        response = LeaveTypeService.insert_or_update_leavetype(db, leavetype)
        
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
            detail=f"Error saving leave type: {str(e)}"
        )

@router.delete("/DeleteLeaveType/{id}", response_model=LeaveTypeDeleteResponse)
async def delete_leavetype(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Delete leave type (soft delete)
    Matches C# DeleteLeaveType endpoint
    """
    try:
        response = LeaveTypeService.delete_leavetype(db, id)
        
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
            detail=f"Error deleting leave type: {str(e)}"
        )

@router.get("/CheckLeaveTypeExists", response_model=LeaveTypeExistsResponse)
async def check_leavetype_exists(
    name: str = Query(..., min_length=1, max_length=100),
    exclude_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Check if a leave type with the given name exists
    Useful for validation before insert/update
    """
    try:
        exists = LeaveTypeService.check_leavetype_exists(db, name, exclude_id)
        return {"exists": exists}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking leave type existence: {str(e)}"
        )

@router.get("/GetLeaveTypeByName/{name}", response_model=Optional[LeaveTypeResponse])
async def get_leavetype_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    """
    Get leave type by exact name match
    """
    try:
        leavetype = LeaveTypeService.get_leavetype_by_name(db, name)
        
        if not leavetype:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="LeaveType not found"
            )
            
        return leavetype
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching leave type by name: {str(e)}"
        )

@router.get("/fetchAllLeaveTypes", response_model=List[LeaveTypeResponse])
async def get_active_leavetypes(
    db: Session = Depends(get_db)
):
    """
    Get all active leave types (simplified list)
    Useful for dropdowns and select inputs
    """
    try:
        leavetypes = LeaveTypeService.get_leave_types(db)
        return leavetypes
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active leave types: {str(e)}"
        )