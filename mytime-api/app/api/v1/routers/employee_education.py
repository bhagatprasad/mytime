from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.schemas.employee_education_schemas import (
    EmployeeEducationCreate, EmployeeEducationUpdate, EmployeeEducationResponse,
    EmployeeEducationListResponse, EmployeeEducationExistsResponse,
    EmployeeEducationDeleteResponse, EmployeeEducationCreateResponse,
    EmployeeEducationUpdateResponse, EmployeeEducationBulkCreate,
    EmployeeEducationFilterParams, EmployeeEducationWithDetailsResponse,
    EmployeeEducationStatistics
)
from app.core.database import get_db
from app.services.employee_education_service import EmployeeEducationService

router = APIRouter()


@router.get("/fetchEmployeeEducation/{employee_education_id}", response_model=EmployeeEducationResponse)
async def fetch_employee_education(employee_education_id: int, db: Session = Depends(get_db)):
    """Get employee education by ID"""
    try:
        education = EmployeeEducationService.fetch_employee_education(db, employee_education_id)
        if not education:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee education record with ID {employee_education_id} not found"
            )
        return education
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee education record: {str(e)}"
        )


@router.get("/fetchEducationsByEmployee/{employee_id}", response_model=List[EmployeeEducationResponse])
async def fetch_educations_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get all education records for a specific employee"""
    try:
        educations = EmployeeEducationService.fetch_educations_by_employee(db, employee_id)
        return educations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching education records for employee: {str(e)}"
        )


@router.get("/fetchActiveEducationsByEmployee/{employee_id}", response_model=List[EmployeeEducationResponse])
async def fetch_active_educations_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get active education records for a specific employee"""
    try:
        educations = EmployeeEducationService.fetch_active_educations_by_employee(db, employee_id)
        return educations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active education records for employee: {str(e)}"
        )


@router.get("/fetchHighestEducationByEmployee/{employee_id}", response_model=Optional[EmployeeEducationResponse])
async def fetch_highest_education_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get highest (latest) education record for an employee"""
    try:
        education = EmployeeEducationService.fetch_highest_education_by_employee(db, employee_id)
        return education
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching highest education for employee: {str(e)}"
        )


@router.get("/fetchAllEmployeeEducations", response_model=List[EmployeeEducationResponse])
async def fetch_all_employee_educations(db: Session = Depends(get_db)):
    """Get all employee education records"""
    try:
        educations = EmployeeEducationService.fetch_all_employee_educations(db)
        return educations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching all employee education records: {str(e)}"
        )


@router.get("/getEmployeeEducations", response_model=EmployeeEducationListResponse)
async def get_employee_educations(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    degree: Optional[str] = Query(None, description="Filter by degree"),
    field_of_study: Optional[str] = Query(None, description="Filter by field of study"),
    institution: Optional[str] = Query(None, description="Filter by institution"),
    year_from: Optional[int] = Query(None, ge=1900, le=2100, description="Completion year from"),
    year_to: Optional[int] = Query(None, ge=1900, le=2100, description="Completion year to"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("EmployeeEducationId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated employee education records with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeEducationService.get_employee_educations_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            employee_id=employee_id,
            degree=degree,
            field_of_study=field_of_study,
            institution=institution,
            year_from=year_from,
            year_to=year_to,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pages = (total + size - 1) // size  # Ceiling division
        
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
            detail=f"Error fetching employee education records: {str(e)}"
        )


@router.post("/InsertOrUpdateEmployeeEducation")
async def insert_or_update_employee_education(education: dict, db: Session = Depends(get_db)):
    """Insert or update employee education record"""
    try:
        response = EmployeeEducationService.insert_or_update_employee_education(db, education)
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
            detail=f"Error saving employee education record: {str(e)}"
        )


@router.delete("/DeleteEmployeeEducation/{employee_education_id}", response_model=EmployeeEducationDeleteResponse)
async def delete_employee_education(employee_education_id: int, db: Session = Depends(get_db)):
    """Delete employee education record"""
    try:
        response = EmployeeEducationService.delete_employee_education(db, employee_education_id)
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
            detail=f"Error deleting employee education record: {str(e)}"
        )


@router.patch("/SoftDeleteEmployeeEducation/{employee_education_id}", response_model=EmployeeEducationResponse)
async def soft_delete_employee_education(
    employee_education_id: int,
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Soft delete employee education record (deactivate)"""
    try:
        response = EmployeeEducationService.soft_delete_employee_education(
            db, employee_education_id, modified_by
        )
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response["education"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deactivating employee education record: {str(e)}"
        )


@router.get("/checkEmployeeEducationExists", response_model=EmployeeEducationExistsResponse)
async def check_employee_education_exists(
    employee_id: int = Query(..., description="Employee ID"),
    degree: str = Query(..., description="Degree"),
    institution: str = Query(..., description="Institution"),
    db: Session = Depends(get_db)
):
    """Check if education record exists for employee"""
    try:
        result = EmployeeEducationService.check_education_exists(db, employee_id, degree, institution)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking employee education existence: {str(e)}"
        )


@router.get("/getEmployeeEducationSummary/{employee_id}", response_model=dict)
async def get_employee_education_summary(employee_id: int, db: Session = Depends(get_db)):
    """Get education summary for an employee"""
    try:
        summary = EmployeeEducationService.get_employee_education_summary(db, employee_id)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching education summary: {str(e)}"
        )


@router.post("/createBulkEducations", response_model=List[EmployeeEducationResponse])
async def create_bulk_educations(
    bulk_data: EmployeeEducationBulkCreate,
    db: Session = Depends(get_db)
):
    """Create multiple education records at once"""
    try:
        educations = EmployeeEducationService.create_bulk_educations(
            db, bulk_data.educations, bulk_data.employee_id
        )
        return educations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating bulk education records: {str(e)}"
        )


# Alternative endpoints using Pydantic models
@router.post("/create", response_model=EmployeeEducationCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_employee_education(
    education: EmployeeEducationCreate, 
    db: Session = Depends(get_db)
):
    """Create a new employee education record using Pydantic model"""
    try:
        # Check if education record already exists
        exists_result = EmployeeEducationService.check_education_exists(
            db, education.EmployeeId, education.Degree, education.Institution
        )
        if exists_result["exists"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Education record already exists for this employee (ID: {exists_result['employee_education_id']})"
            )
        
        db_education = EmployeeEducationService.create_employee_education(db, education)
        return {
            "success": True,
            "message": "Employee education record created successfully",
            "employee_education_id": db_education.EmployeeEducationId
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating employee education record: {str(e)}"
        )


@router.put("/update/{employee_education_id}", response_model=EmployeeEducationUpdateResponse)
async def update_employee_education(
    employee_education_id: int, 
    education: EmployeeEducationUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing employee education record using Pydantic model"""
    try:
        updated_education = EmployeeEducationService.update_employee_education(
            db, employee_education_id, education
        )
        if not updated_education:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee education record with ID {employee_education_id} not found"
            )
        
        # Get list of updated fields
        updated_fields = list(education.model_dump(exclude_none=True).keys())
        
        return {
            "success": True,
            "message": "Employee education record updated successfully",
            "employee_education_id": employee_education_id,
            "modified_fields": updated_fields
        }
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
            detail=f"Error updating employee education record: {str(e)}"
        )


@router.get("/educationStatistics", response_model=EmployeeEducationStatistics)
async def get_education_statistics(db: Session = Depends(get_db)):
    """Get education statistics"""
    try:
        stats = EmployeeEducationService.get_education_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching education statistics: {str(e)}"
        )


@router.get("/searchByDegree/{degree}", response_model=List[EmployeeEducationResponse])
async def search_by_degree(degree: str, db: Session = Depends(get_db)):
    """Search education records by degree"""
    try:
        items, _ = EmployeeEducationService.get_employee_educations_with_pagination(
            db=db,
            skip=0,
            limit=1000,
            degree=degree,
            is_active=True
        )
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching by degree: {str(e)}"
        )


@router.get("/searchByInstitution/{institution}", response_model=List[EmployeeEducationResponse])
async def search_by_institution(institution: str, db: Session = Depends(get_db)):
    """Search education records by institution"""
    try:
        items, _ = EmployeeEducationService.get_employee_educations_with_pagination(
            db=db,
            skip=0,
            limit=1000,
            institution=institution,
            is_active=True
        )
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching by institution: {str(e)}"
        )


@router.post("/searchEmployeeEducations", response_model=EmployeeEducationListResponse)
async def search_employee_educations(
    filters: EmployeeEducationFilterParams,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    sort_by: str = Query("EmployeeEducationId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Advanced employee education search with filters"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeEducationService.get_employee_educations_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=filters.search_term,
            employee_id=filters.employee_id,
            degree=filters.degree,
            field_of_study=filters.field_of_study,
            institution=filters.institution,
            year_from=filters.year_from,
            year_to=filters.year_to,
            is_active=filters.is_active,
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
            detail=f"Error searching employee education records: {str(e)}"
        )