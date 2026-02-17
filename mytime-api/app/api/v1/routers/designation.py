from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.designation_schemas import (
    DesignationCreate, DesignationUpdate, DesignationResponse, DesignationListResponse,
    DesignationExistsResponse, DesignationDeleteResponse
)
from app.core.database import get_db
from app.services.designation_service import DesignationService

router = APIRouter()


@router.get("/fetchDesignation/{designation_id}", response_model=DesignationResponse)
async def fetch_designation(designation_id: int, db: Session = Depends(get_db)):
    """Get designation by ID"""
    try:
        designation = DesignationService.fetch_designation(db, designation_id)
        if not designation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Designation with ID {designation_id} not found"
            )
        return designation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching designation: {str(e)}"
        )


@router.get("/fetchAllDesignations", response_model=List[DesignationResponse])
async def fetch_all_designations(db: Session = Depends(get_db)):
    """Get all designations"""
    try:
        designations = DesignationService.fetch_all_designations(db)
        return designations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching designations: {str(e)}"
        )

@router.post("/InsertOrUpdateDesignation")
async def insert_or_update_designation(designation: dict, db: Session = Depends(get_db)):
    """Insert or update designation"""
    try:
        response = DesignationService.insert_or_update_designation(db, designation)
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
            detail=f"Error saving designation: {str(e)}"
        )


@router.delete("/DeleteDesignation/{designation_id}", response_model=DesignationDeleteResponse)
async def delete_designation(designation_id: int, db: Session = Depends(get_db)):
    """Delete designation"""
    try:
        response = DesignationService.delete_designation(db, designation_id)
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
            detail=f"Error deleting designation: {str(e)}"
        )