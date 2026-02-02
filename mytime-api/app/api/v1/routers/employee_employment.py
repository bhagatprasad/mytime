from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.schemas.employee_employment_schemas import (
    EmployeeEmploymentCreate, EmployeeEmploymentUpdate, EmployeeEmploymentResponse,
    EmployeeEmploymentListResponse, EmployeeEmploymentExistsResponse,
    EmployeeEmploymentDeleteResponse, EmployeeEmploymentCreateResponse,
    EmployeeEmploymentUpdateResponse, EmployeeEmploymentBulkCreate,
    EmployeeEmploymentFilterParams, EmployeeEmploymentWithDetailsResponse,
    EmployeeEmploymentStatistics
)
from app.core.database import get_db
from app.services.employee_employment_service import EmployeeEmploymentService

router = APIRouter(prefix="/employee-employments", tags=["employee-employments"])


@router.get("/fetchEmployeeEmployment/{employee_employment_id}", response_model=EmployeeEmploymentResponse)
async def fetch_employee_employment(employee_employment_id: int, db: Session = Depends(get_db)):
    """Get employee employment by ID"""
    try:
        employment = EmployeeEmploymentService.fetch_employee_employment(db, employee_employment_id)
        if not employment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee employment record with ID {employee_employment_id} not found"
            )
        return employment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee employment record: {str(e)}"
        )


@router.get("/fetchEmploymentsByEmployee/{employee_id}", response_model=List[EmployeeEmploymentResponse])
async def fetch_employments_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get all employment records for a specific employee"""
    try:
        employments = EmployeeEmploymentService.fetch_employments_by_employee(db, employee_id)
        return employments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employment records for employee: {str(e)}"
        )


@router.get("/fetchActiveEmploymentsByEmployee/{employee_id}", response_model=List[EmployeeEmploymentResponse])
async def fetch_active_employments_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get active employment records for a specific employee"""
    try:
        employments = EmployeeEmploymentService.fetch_active_employments_by_employee(db, employee_id)
        return employments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active employment records for employee: {str(e)}"
        )


@router.get("/fetchLatestEmploymentByEmployee/{employee_id}", response_model=Optional[EmployeeEmploymentResponse])
async def fetch_latest_employment_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get latest employment record for an employee"""
    try:
        employment = EmployeeEmploymentService.fetch_latest_employment_by_employee(db, employee_id)
        return employment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching latest employment for employee: {str(e)}"
        )


@router.get("/fetchAllEmployeeEmployments", response_model=List[EmployeeEmploymentResponse])
async def fetch_all_employee_employments(db: Session = Depends(get_db)):
    """Get all employee employment records"""
    try:
        employments = EmployeeEmploymentService.fetch_all_employee_employments(db)
        return employments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching all employee employment records: {str(e)}"
        )


@router.get("/getEmployeeEmployments", response_model=EmployeeEmploymentListResponse)
async def get_employee_employments(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    company_name: Optional[str] = Query(None, description="Filter by company name"),
    designation: Optional[str] = Query(None, description="Filter by designation"),
    start_year_from: Optional[int] = Query(None, ge=1900, le=2100, description="Start year from"),
    start_year_to: Optional[int] = Query(None, ge=1900, le=2100, description="Start year to"),
    end_year_from: Optional[int] = Query(None, ge=1900, le=2100, description="End year from"),
    end_year_to: Optional[int] = Query(None, ge=1900, le=2100, description="End year to"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("EmployeeEmploymentId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated employee employment records with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeEmploymentService.get_employee_employments_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            employee_id=employee_id,
            company_name=company_name,
            designation=designation,
            start_year_from=start_year_from,
            start_year_to=start_year_to,
            end_year_from=end_year_from,
            end_year_to=end_year_to,
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
            detail=f"Error fetching employee employment records: {str(e)}"
        )


@router.post("/InsertOrUpdateEmployeeEmployment")
async def insert_or_update_employee_employment(employment: dict, db: Session = Depends(get_db)):
    """Insert or update employee employment record"""
    try:
        response = EmployeeEmploymentService.insert_or_update_employee_employment(db, employment)
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
            detail=f"Error saving employee employment record: {str(e)}"
        )


@router.delete("/DeleteEmployeeEmployment/{employee_employment_id}", response_model=EmployeeEmploymentDeleteResponse)
async def delete_employee_employment(employee_employment_id: int, db: Session = Depends(get_db)):
    """Delete employee employment record"""
    try:
        response = EmployeeEmploymentService.delete_employee_employment(db, employee_employment_id)
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
            detail=f"Error deleting employee employment record: {str(e)}"
        )


@router.patch("/SoftDeleteEmployeeEmployment/{employee_employment_id}", response_model=EmployeeEmploymentResponse)
async def soft_delete_employee_employment(
    employee_employment_id: int,
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Soft delete employee employment record (deactivate)"""
    try:
        response = EmployeeEmploymentService.soft_delete_employee_employment(
            db, employee_employment_id, modified_by
        )
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response["employment"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deactivating employee employment record: {str(e)}"
        )


@router.get("/checkEmployeeEmploymentExists", response_model=EmployeeEmploymentExistsResponse)
async def check_employee_employment_exists(
    employee_id: int = Query(..., description="Employee ID"),
    company_name: str = Query(..., description="Company name"),
    designation: str = Query(..., description="Designation"),
    started_on: datetime = Query(..., description="Start date"),
    db: Session = Depends(get_db)
):
    """Check if employment record exists for employee"""
    try:
        result = EmployeeEmploymentService.check_employment_exists(
            db, employee_id, company_name, designation, started_on
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking employee employment existence: {str(e)}"
        )


@router.get("/getEmployeeEmploymentSummary/{employee_id}", response_model=dict)
async def get_employee_employment_summary(employee_id: int, db: Session = Depends(get_db)):
    """Get employment summary for an employee"""
    try:
        summary = EmployeeEmploymentService.get_employee_employment_summary(db, employee_id)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employment summary: {str(e)}"
        )


@router.post("/createBulkEmployments", response_model=List[EmployeeEmploymentResponse])
async def create_bulk_employments(
    bulk_data: EmployeeEmploymentBulkCreate,
    db: Session = Depends(get_db)
):
    """Create multiple employment records at once"""
    try:
        employments = EmployeeEmploymentService.create_bulk_employments(
            db, bulk_data.employments, bulk_data.employee_id
        )
        return employments
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating bulk employment records: {str(e)}"
        )


# Alternative endpoints using Pydantic models
@router.post("/create", response_model=EmployeeEmploymentCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_employee_employment(
    employment: EmployeeEmploymentCreate, 
    db: Session = Depends(get_db)
):
    """Create a new employee employment record using Pydantic model"""
    try:
        # Check if employment record already exists
        exists_result = EmployeeEmploymentService.check_employment_exists(
            db, employment.EmployeeId, employment.CompanyName, 
            employment.Designation, employment.StartedOn
        )
        if exists_result["exists"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Employment record already exists for this employee (ID: {exists_result['employee_employment_id']})"
            )
        
        db_employment = EmployeeEmploymentService.create_employee_employment(db, employment)
        return {
            "success": True,
            "message": "Employee employment record created successfully",
            "employee_employment_id": db_employment.EmployeeEmploymentId
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
            detail=f"Error creating employee employment record: {str(e)}"
        )


@router.put("/update/{employee_employment_id}", response_model=EmployeeEmploymentUpdateResponse)
async def update_employee_employment(
    employee_employment_id: int, 
    employment: EmployeeEmploymentUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing employee employment record using Pydantic model"""
    try:
        updated_employment = EmployeeEmploymentService.update_employee_employment(
            db, employee_employment_id, employment
        )
        if not updated_employment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee employment record with ID {employee_employment_id} not found"
            )
        
        # Get list of updated fields
        updated_fields = list(employment.model_dump(exclude_none=True).keys())
        
        return {
            "success": True,
            "message": "Employee employment record updated successfully",
            "employee_employment_id": employee_employment_id,
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
            detail=f"Error updating employee employment record: {str(e)}"
        )


@router.get("/employmentStatistics", response_model=EmployeeEmploymentStatistics)
async def get_employment_statistics(db: Session = Depends(get_db)):
    """Get employment statistics"""
    try:
        stats = EmployeeEmploymentService.get_employment_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employment statistics: {str(e)}"
        )


@router.get("/searchByCompany/{company_name}", response_model=List[EmployeeEmploymentResponse])
async def search_by_company(company_name: str, db: Session = Depends(get_db)):
    """Search employment records by company"""
    try:
        items, _ = EmployeeEmploymentService.get_employee_employments_with_pagination(
            db=db,
            skip=0,
            limit=1000,
            company_name=company_name,
            is_active=True
        )
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching by company: {str(e)}"
        )


@router.get("/searchByDesignation/{designation}", response_model=List[EmployeeEmploymentResponse])
async def search_by_designation(designation: str, db: Session = Depends(get_db)):
    """Search employment records by designation"""
    try:
        items, _ = EmployeeEmploymentService.get_employee_employments_with_pagination(
            db=db,
            skip=0,
            limit=1000,
            designation=designation,
            is_active=True
        )
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching by designation: {str(e)}"
        )


@router.get("/employeesByPreviousCompany/{company_name}", response_model=List[int])
async def get_employees_by_previous_company(company_name: str, db: Session = Depends(get_db)):
    """Get employee IDs who worked at a specific company"""
    try:
        employee_ids = EmployeeEmploymentService.get_employees_by_previous_company(db, company_name)
        return employee_ids
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employees by previous company: {str(e)}"
        )


@router.post("/searchEmployeeEmployments", response_model=EmployeeEmploymentListResponse)
async def search_employee_employments(
    filters: EmployeeEmploymentFilterParams,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    sort_by: str = Query("EmployeeEmploymentId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Advanced employee employment search with filters"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeEmploymentService.get_employee_employments_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=filters.search_term,
            employee_id=filters.employee_id,
            company_name=filters.company_name,
            designation=filters.designation,
            start_year_from=filters.start_year_from,
            start_year_to=filters.start_year_to,
            end_year_from=filters.end_year_from,
            end_year_to=filters.end_year_to,
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
            detail=f"Error searching employee employment records: {str(e)}"
        )


@router.get("/calculateTotalExperience/{employee_id}", response_model=dict)
async def calculate_total_experience(employee_id: int, db: Session = Depends(get_db)):
    """Calculate total work experience for an employee"""
    try:
        summary = EmployeeEmploymentService.get_employee_employment_summary(db, employee_id)
        
        return {
            "employee_id": employee_id,
            "total_experience_months": summary.get("total_experience_months", 0),
            "total_experience_years": summary.get("total_experience_years", 0),
            "number_of_companies": len(summary.get("employments_by_company", {})),
            "employment_records": summary.get("total_records", 0)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating total experience: {str(e)}"
        )