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


@router.get("/fetchActiveDesignations", response_model=List[DesignationResponse])
async def fetch_active_designations(db: Session = Depends(get_db)):
    """Get all active designations"""
    try:
        designations = DesignationService.fetch_active_designations(db)
        return designations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active designations: {str(e)}"
        )


@router.get("/getDesignations", response_model=DesignationListResponse)
async def get_designations(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("DesignationId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated designations with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = DesignationService.get_designations_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pages = (total + size - 1) // size
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "size": size,
            "pages": pages
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching designations: {str(e)}"
        )


@router.get("/checkDesignationExists", response_model=DesignationExistsResponse)
async def check_designation_exists(
    name: Optional[str] = Query(None, description="Designation name"),
    code: Optional[str] = Query(None, description="Designation code"),
    exclude_id: Optional[int] = Query(None, description="Designation ID to exclude (for updates)"),
    db: Session = Depends(get_db)
):
    """Check if designation exists"""
    try:
        exists = DesignationService.check_designation_exists(db, name, code, exclude_id)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking designation existence: {str(e)}"
        )


@router.get("/getDesignationByCode/{code}", response_model=DesignationResponse)
async def get_designation_by_code(code: str, db: Session = Depends(get_db)):
    """Get designation by code"""
    try:
        designation = DesignationService.get_designation_by_code(db, code)
        if not designation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Designation with code '{code}' not found"
            )
        return designation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching designation by code: {str(e)}"
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


@router.post("/create", response_model=DesignationResponse, status_code=status.HTTP_201_CREATED)
async def create_designation(designation: DesignationCreate, db: Session = Depends(get_db)):
    """Create a new designation using Pydantic model"""
    try:
        return DesignationService.create_designation(db, designation)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating designation: {str(e)}"
        )


@router.put("/update/{designation_id}", response_model=DesignationResponse)
async def update_designation(designation_id: int, designation: DesignationUpdate, db: Session = Depends(get_db)):
    """Update an existing designation using Pydantic model"""
    try:
        updated_designation = DesignationService.update_designation(db, designation_id, designation)
        if not updated_designation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Designation with ID {designation_id} not found"
            )
        return updated_designation
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating designation: {str(e)}"
        )


@router.patch("/toggleActiveStatus/{designation_id}", response_model=DesignationResponse)
async def toggle_active_status(
    designation_id: int,
    is_active: bool = Query(..., description="New active status (true/false)"),
    db: Session = Depends(get_db)
):
    """Toggle the active status of a designation"""
    try:
        designation = DesignationService.toggle_active_status(db, designation_id, is_active)
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
            detail=f"Error toggling active status: {str(e)}"
        )


@router.get("/searchDesignations", response_model=List[DesignationResponse])
async def search_designations(
    q: str = Query(..., min_length=2, description="Search term"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """Search designations by name or code"""
    try:
        designations = DesignationService.search_designations(db, q, limit)
        return designations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching designations: {str(e)}"
        )


@router.get("/getDesignationsByIds", response_model=List[DesignationResponse])
async def get_designations_by_ids(
    ids: str = Query(..., description="Comma-separated designation IDs"),
    db: Session = Depends(get_db)
):
    """Get multiple designations by their IDs"""
    try:
        # Convert comma-separated string to list of integers
        designation_ids = [int(id.strip()) for id in ids.split(",") if id.strip().isdigit()]
        
        if not designation_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid designation IDs provided"
            )
        
        designations = DesignationService.get_designations_by_ids(db, designation_ids)
        return designations
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid designation ID format. Provide comma-separated integers."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching designations by IDs: {str(e)}"
        )