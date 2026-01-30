from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.department_schemas import (
    DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentListResponse,
    DepartmentExistsResponse, DepartmentDeleteResponse
)
from app.core.database import get_db
from app.services.department_service import DepartmentService

router = APIRouter()


@router.get("/fetchDepartment/{department_id}", response_model=DepartmentResponse)
async def fetch_department(department_id: int, db: Session = Depends(get_db)):
    """Get department by ID"""
    try:
        department = DepartmentService.fetch_department(db, department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {department_id} not found"
            )
        return department
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching department: {str(e)}"
        )


@router.get("/fetchAllDepartments", response_model=List[DepartmentResponse])
async def fetch_all_departments(db: Session = Depends(get_db)):
    """Get all departments"""
    try:
        departments = DepartmentService.fetch_all_departments(db)
        return departments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching departments: {str(e)}"
        )


@router.get("/fetchActiveDepartments", response_model=List[DepartmentResponse])
async def fetch_active_departments(db: Session = Depends(get_db)):
    """Get all active departments"""
    try:
        departments = DepartmentService.fetch_active_departments(db)
        return departments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active departments: {str(e)}"
        )


@router.get("/getDepartments", response_model=DepartmentListResponse)
async def get_departments(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("DepartmentId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated departments with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = DepartmentService.get_departments_with_pagination(
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
            detail=f"Error fetching departments: {str(e)}"
        )


@router.get("/checkDepartmentExists", response_model=DepartmentExistsResponse)
async def check_department_exists(
    name: Optional[str] = Query(None, description="Department name"),
    code: Optional[str] = Query(None, description="Department code"),
    exclude_id: Optional[int] = Query(None, description="Department ID to exclude (for updates)"),
    db: Session = Depends(get_db)
):
    """Check if department exists"""
    try:
        exists = DepartmentService.check_department_exists(db, name, code, exclude_id)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking department existence: {str(e)}"
        )


@router.get("/getDepartmentByCode/{code}", response_model=DepartmentResponse)
async def get_department_by_code(code: str, db: Session = Depends(get_db)):
    """Get department by code"""
    try:
        department = DepartmentService.get_department_by_code(db, code)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with code '{code}' not found"
            )
        return department
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching department by code: {str(e)}"
        )


@router.post("/InsertOrUpdateDepartment")
async def insert_or_update_department(department: dict, db: Session = Depends(get_db)):
    """Insert or update department"""
    try:
        response = DepartmentService.insert_or_update_department(db, department)
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
            detail=f"Error saving department: {str(e)}"
        )


@router.delete("/DeleteDepartment/{department_id}", response_model=DepartmentDeleteResponse)
async def delete_department(department_id: int, db: Session = Depends(get_db)):
    """Delete department"""
    try:
        response = DepartmentService.delete_department(db, department_id)
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
            detail=f"Error deleting department: {str(e)}"
        )


@router.post("/create", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new department using Pydantic model"""
    try:
        return DepartmentService.create_department(db, department)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating department: {str(e)}"
        )


@router.put("/update/{department_id}", response_model=DepartmentResponse)
async def update_department(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    """Update an existing department using Pydantic model"""
    try:
        updated_department = DepartmentService.update_department(db, department_id, department)
        if not updated_department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {department_id} not found"
            )
        return updated_department
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
            detail=f"Error updating department: {str(e)}"
        )


@router.patch("/toggleActiveStatus/{department_id}", response_model=DepartmentResponse)
async def toggle_active_status(
    department_id: int,
    is_active: bool = Query(..., description="New active status (true/false)"),
    db: Session = Depends(get_db)
):
    """Toggle the active status of a department"""
    try:
        department = DepartmentService.toggle_active_status(db, department_id, is_active)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with ID {department_id} not found"
            )
        return department
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling active status: {str(e)}"
        )


@router.get("/searchDepartments", response_model=List[DepartmentResponse])
async def search_departments(
    q: str = Query(..., min_length=2, description="Search term"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """Search departments by name, code, or description"""
    try:
        departments = DepartmentService.search_departments(db, q, limit)
        return departments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching departments: {str(e)}"
        )


@router.get("/getDepartmentsByIds", response_model=List[DepartmentResponse])
async def get_departments_by_ids(
    ids: str = Query(..., description="Comma-separated department IDs"),
    db: Session = Depends(get_db)
):
    """Get multiple departments by their IDs"""
    try:
        # Convert comma-separated string to list of integers
        department_ids = [int(id.strip()) for id in ids.split(",") if id.strip().isdigit()]
        
        if not department_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid department IDs provided"
            )
        
        departments = DepartmentService.get_departments_by_ids(db, department_ids)
        return departments
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid department ID format. Provide comma-separated integers."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching departments by IDs: {str(e)}"
        )