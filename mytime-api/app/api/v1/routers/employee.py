from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.schemas.employee_schemas import (
    EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeListResponse,
    EmployeeExistsResponse, EmployeeDeleteResponse, EmployeeSummaryResponse,
    EmployeeCreateResponse, EmployeeUpdateResponse, EmployeeSearchResponse,
    EmployeeFilterParams
)
from app.core.database import get_db
from app.services.employee_service import EmployeeService

router = APIRouter()


@router.get("/fetchEmployee/{employee_id}", response_model=EmployeeResponse)
async def fetch_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get employee by ID"""
    try:
        employee = EmployeeService.fetch_employee(db, employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee: {str(e)}"
        )


@router.get("/fetchEmployeeByCode/{employee_code}", response_model=EmployeeResponse)
async def fetch_employee_by_code(employee_code: str, db: Session = Depends(get_db)):
    """Get employee by EmployeeCode"""
    try:
        employee = EmployeeService.fetch_employee_by_code(db, employee_code)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with code '{employee_code}' not found"
            )
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee by code: {str(e)}"
        )


@router.get("/fetchEmployeeByEmail/{email}", response_model=EmployeeResponse)
async def fetch_employee_by_email(email: str, db: Session = Depends(get_db)):
    """Get employee by Email"""
    try:
        employee = EmployeeService.fetch_employee_by_email(db, email)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with email '{email}' not found"
            )
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee by email: {str(e)}"
        )


@router.get("/fetchEmployeeByUserId/{user_id}", response_model=EmployeeResponse)
async def fetch_employee_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """Get employee by UserId"""
    try:
        employee = EmployeeService.fetch_employee_by_user_id(db, user_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with UserId {user_id} not found"
            )
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee by user ID: {str(e)}"
        )


@router.get("/fetchAllEmployees", response_model=List[EmployeeResponse])
async def fetch_all_employees(db: Session = Depends(get_db)):
    """Get all employees"""
    try:
        employees = EmployeeService.fetch_all_employees(db)
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employees: {str(e)}"
        )


@router.get("/getEmployees", response_model=EmployeeListResponse)
async def get_employees(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    designation_id: Optional[int] = Query(None, description="Filter by designation ID"),
    role_id: Optional[int] = Query(None, description="Filter by role ID"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    start_date_from: Optional[datetime] = Query(None, description="Start date from"),
    start_date_to: Optional[datetime] = Query(None, description="Start date to"),
    sort_by: str = Query("EmployeeId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated employees with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeService.get_employees_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            is_active=is_active,
            department_id=department_id,
            designation_id=designation_id,
            role_id=role_id,
            gender=gender,
            start_date_from=start_date_from,
            start_date_to=start_date_to,
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
            detail=f"Error fetching employees: {str(e)}"
        )


@router.post("/InsertOrUpdateEmployee")
async def insert_or_update_employee(employee: dict, db: Session = Depends(get_db)):
    """Insert or update employee"""
    try:
        response = EmployeeService.insert_or_update_employee(db, employee)
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
            detail=f"Error saving employee: {str(e)}"
        )


@router.delete("/DeleteEmployee/{employee_id}", response_model=EmployeeDeleteResponse)
async def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete employee"""
    try:
        response = EmployeeService.delete_employee(db, employee_id)
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
            detail=f"Error deleting employee: {str(e)}"
        )


@router.delete("/SoftDeleteEmployee/{employee_id}", response_model=EmployeeResponse)
async def soft_delete_employee(
    employee_id: int,
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Soft delete employee (deactivate)"""
    try:
        response = EmployeeService.soft_delete_employee(db, employee_id, modified_by)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response["employee"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deactivating employee: {str(e)}"
        )


@router.get("/checkEmployeeExists", response_model=EmployeeExistsResponse)
async def check_employee_exists(
    employee_code: Optional[str] = Query(None, description="Employee code"),
    email: Optional[str] = Query(None, description="Email address"),
    db: Session = Depends(get_db)
):
    """Check if employee exists by code or email"""
    try:
        result = EmployeeService.check_employee_exists(db, employee_code, email)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking employee existence: {str(e)}"
        )


@router.get("/getEmployeesByDepartment/{department_id}", response_model=List[EmployeeResponse])
async def get_employees_by_department(department_id: int, db: Session = Depends(get_db)):
    """Get all employees in a specific department"""
    try:
        employees = EmployeeService.get_employees_by_department(db, department_id)
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employees by department: {str(e)}"
        )


@router.get("/getEmployeesByDesignation/{designation_id}", response_model=List[EmployeeResponse])
async def get_employees_by_designation(designation_id: int, db: Session = Depends(get_db)):
    """Get all employees with a specific designation"""
    try:
        employees = EmployeeService.get_employees_by_designation(db, designation_id)
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employees by designation: {str(e)}"
        )


@router.patch("/updateActiveStatus/{employee_id}", response_model=EmployeeResponse)
async def update_active_status(
    employee_id: int,
    is_active: bool = Query(..., description="New active status (true/false)"),
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Update employee active status"""
    try:
        employee = EmployeeService.update_employee_status(db, employee_id, is_active, modified_by)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating employee status: {str(e)}"
        )


@router.post("/bulkUpdateDepartment", response_model=dict)
async def bulk_update_department(
    employee_ids: List[int],
    department_id: int = Query(..., description="New department ID"),
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Bulk update department for multiple employees"""
    try:
        count = EmployeeService.bulk_update_department(db, employee_ids, department_id, modified_by)
        return {
            "success": True,
            "message": f"Successfully updated {count} employees",
            "updated_count": count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error bulk updating department: {str(e)}"
        )


@router.get("/employeeStatistics", response_model=dict)
async def get_employee_statistics(db: Session = Depends(get_db)):
    """Get employee statistics"""
    try:
        stats = EmployeeService.get_employee_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee statistics: {str(e)}"
        )


@router.post("/searchEmployees", response_model=EmployeeSearchResponse)
async def search_employees(
    filters: EmployeeFilterParams,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    sort_by: str = Query("EmployeeId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Advanced employee search with filters"""
    try:
        skip = (page - 1) * size
        
        items, total = EmployeeService.get_employees_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=filters.search_term,
            is_active=filters.is_active,
            department_id=filters.department_id,
            designation_id=filters.designation_id,
            role_id=filters.role_id,
            gender=filters.gender,
            start_date_from=filters.start_date_from,
            start_date_to=filters.start_date_to,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Convert to summary response
        employees = [
            EmployeeSummaryResponse(
                EmployeeId=emp.EmployeeId,
                EmployeeCode=emp.EmployeeCode,
                FirstName=emp.FirstName,
                LastName=emp.LastName,
                Email=emp.Email,
                Phone=emp.Phone,
                DepartmentId=emp.DepartmentId,
                DesignationId=emp.DesignationId,
                IsActive=emp.IsActive,
                FullName=f"{emp.FirstName or ''} {emp.LastName or ''}".strip()
            )
            for emp in items
        ]
        
        return {
            "total": total,
            "employees": employees
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching employees: {str(e)}"
        )


# Alternative endpoints using Pydantic models (for API-first approach)
@router.post("/create", response_model=EmployeeCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee using Pydantic model"""
    try:
        # Check if employee already exists
        exists_result = EmployeeService.check_employee_exists(
            db, 
            employee.EmployeeCode, 
            employee.Email
        )
        if exists_result["exists"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Employee already exists (ID: {exists_result['employee_id']})"
            )
        
        db_employee = EmployeeService.create_employee(db, employee)
        return {
            "success": True,
            "message": "Employee created successfully",
            "employee_id": db_employee.EmployeeId,
            "employee_code": db_employee.EmployeeCode
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
            detail=f"Error creating employee: {str(e)}"
        )


@router.put("/update/{employee_id}", response_model=EmployeeUpdateResponse)
async def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    """Update an existing employee using Pydantic model"""
    try:
        updated_employee = EmployeeService.update_employee(db, employee_id, employee)
        if not updated_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        # Get list of updated fields
        updated_fields = list(employee.model_dump(exclude_none=True).keys())
        
        return {
            "success": True,
            "message": "Employee updated successfully",
            "employee_id": employee_id,
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
            detail=f"Error updating employee: {str(e)}"
        )


@router.get("/activeEmployees", response_model=List[EmployeeResponse])
async def get_active_employees(db: Session = Depends(get_db)):
    """Get all active employees"""
    try:
        employees = EmployeeService.get_employees_with_pagination(
            db=db,
            skip=0,
            limit=1000,
            is_active=True
        )
        return employees[0]  # Return items only
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active employees: {str(e)}"
        )


@router.get("/exportEmployees", response_model=List[EmployeeResponse])
async def export_employees(db: Session = Depends(get_db)):
    """Export all employees (no pagination, for export purposes)"""
    try:
        employees = EmployeeService.fetch_all_employees(db)
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting employees: {str(e)}"
        )