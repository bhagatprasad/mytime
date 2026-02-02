from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from decimal import Decimal

from app.models.employee_salary_structure import EmployeeSalaryStructure
from app.schemas.employee_salary_structure_schemas import (
    EmployeeSalaryStructureCreate, EmployeeSalaryStructureUpdate, EmployeeSalaryStructureResponse,
    EmployeeSalaryStructureListResponse, EmployeeSalaryStructureExistsResponse,
    EmployeeSalaryStructureDeleteResponse, EmployeeSalaryStructureCreateResponse,
    EmployeeSalaryStructureUpdateResponse, SalaryBreakdownResponse,
    EmployeeSalaryStructureFilterParams, EmployeeSalaryStructureWithDetailsResponse,
    SalaryStatisticsResponse
)
from app.core.database import get_db
from app.services.employee_salary_structure_service import EmployeeSalaryStructureService

router = APIRouter(prefix="/employee-salary-structures", tags=["employee-salary-structures"])


@router.get("/fetchEmployeeSalaryStructure/{employee_salary_structure_id}", response_model=EmployeeSalaryStructureResponse)
async def fetch_employee_salary_structure(employee_salary_structure_id: int, db: Session = Depends(get_db)):
    """Get employee salary structure by ID"""
    try:
        salary = EmployeeSalaryStructureService.fetch_employee_salary_structure(db, employee_salary_structure_id)
        if not salary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee salary structure with ID {employee_salary_structure_id} not found"
            )
        return salary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employee salary structure: {str(e)}"
        )


@router.get("/fetchSalaryStructureByEmployee/{employee_id}", response_model=Optional[EmployeeSalaryStructureResponse])
async def fetch_salary_structure_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get salary structure for a specific employee"""
    try:
        salary = EmployeeSalaryStructureService.fetch_salary_structure_by_employee(db, employee_id)
        return salary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching salary structure for employee: {str(e)}"
        )


@router.get("/fetchAllSalaryStructuresByEmployee/{employee_id}", response_model=List[EmployeeSalaryStructureResponse])
async def fetch_all_salary_structures_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get all salary structures for a specific employee"""
    try:
        salaries = EmployeeSalaryStructureService.fetch_all_salary_structures_by_employee(db, employee_id)
        return salaries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching all salary structures for employee: {str(e)}"
        )


@router.get("/fetchActiveSalaryStructures", response_model=List[EmployeeSalaryStructureResponse])
async def fetch_active_salary_structures(db: Session = Depends(get_db)):
    """Get all active salary structures"""
    try:
        salaries = EmployeeSalaryStructureService.fetch_active_salary_structures(db)
        return salaries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active salary structures: {str(e)}"
        )


@router.get("/fetchAllEmployeeSalaryStructures", response_model=List[EmployeeSalaryStructureResponse])
async def fetch_all_employee_salary_structures(db: Session = Depends(get_db)):
    """Get all employee salary structures"""
    try:
        salaries = EmployeeSalaryStructureService.fetch_all_employee_salary_structures(db)
        return salaries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching all employee salary structures: {str(e)}"
        )


@router.get("/getEmployeeSalaryStructures", response_model=EmployeeSalaryStructureListResponse)
async def get_employee_salary_structures(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    designation_id: Optional[int] = Query(None, description="Filter by designation ID"),
    min_basic: Optional[Decimal] = Query(None, ge=0, description="Minimum basic salary"),
    max_basic: Optional[Decimal] = Query(None, ge=0, description="Maximum basic salary"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    has_pan: Optional[bool] = Query(None, description="Filter by PAN availability"),
    has_bank_account: Optional[bool] = Query(None, description="Filter by bank account availability"),
    sort_by: str = Query("EmployeeSalaryStructureId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated employee salary structures with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeSalaryStructureService.get_employee_salary_structures_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            employee_id=employee_id,
            department_id=department_id,
            designation_id=designation_id,
            min_basic=min_basic,
            max_basic=max_basic,
            is_active=is_active,
            has_pan=has_pan,
            has_bank_account=has_bank_account,
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
            detail=f"Error fetching employee salary structures: {str(e)}"
        )


@router.post("/InsertOrUpdateEmployeeSalaryStructure")
async def insert_or_update_employee_salary_structure(salary: dict, db: Session = Depends(get_db)):
    """Insert or update employee salary structure"""
    try:
        response = EmployeeSalaryStructureService.insert_or_update_employee_salary_structure(db, salary)
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
            detail=f"Error saving employee salary structure: {str(e)}"
        )


@router.delete("/DeleteEmployeeSalaryStructure/{employee_salary_structure_id}", response_model=EmployeeSalaryStructureDeleteResponse)
async def delete_employee_salary_structure(employee_salary_structure_id: int, db: Session = Depends(get_db)):
    """Delete employee salary structure"""
    try:
        response = EmployeeSalaryStructureService.delete_employee_salary_structure(db, employee_salary_structure_id)
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
            detail=f"Error deleting employee salary structure: {str(e)}"
        )


@router.patch("/SoftDeleteEmployeeSalaryStructure/{employee_salary_structure_id}", response_model=EmployeeSalaryStructureResponse)
async def soft_delete_employee_salary_structure(
    employee_salary_structure_id: int,
    modified_by: int = Query(..., description="User ID performing the action"),
    db: Session = Depends(get_db)
):
    """Soft delete employee salary structure (deactivate)"""
    try:
        response = EmployeeSalaryStructureService.soft_delete_employee_salary_structure(
            db, employee_salary_structure_id, modified_by
        )
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response["salary"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deactivating employee salary structure: {str(e)}"
        )


@router.get("/checkEmployeeSalaryStructureExists", response_model=EmployeeSalaryStructureExistsResponse)
async def check_employee_salary_structure_exists(
    employee_id: int = Query(..., description="Employee ID"),
    db: Session = Depends(get_db)
):
    """Check if salary structure exists for employee"""
    try:
        result = EmployeeSalaryStructureService.check_salary_structure_exists(db, employee_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking employee salary structure existence: {str(e)}"
        )


@router.get("/getSalaryBreakdown/{employee_salary_structure_id}", response_model=SalaryBreakdownResponse)
async def get_salary_breakdown(employee_salary_structure_id: int, db: Session = Depends(get_db)):
    """Get detailed salary breakdown"""
    try:
        breakdown = EmployeeSalaryStructureService.get_salary_breakdown(db, employee_salary_structure_id)
        if "error" in breakdown:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=breakdown["error"]
            )
        return breakdown
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching salary breakdown: {str(e)}"
        )


@router.get("/salaryStatistics", response_model=SalaryStatisticsResponse)
async def get_salary_statistics(db: Session = Depends(get_db)):
    """Get salary statistics"""
    try:
        stats = EmployeeSalaryStructureService.get_salary_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching salary statistics: {str(e)}"
        )


@router.get("/salaryComparisonReport", response_model=dict)
async def get_salary_comparison_report(
    department_id: Optional[int] = Query(None, description="Department ID"),
    db: Session = Depends(get_db)
):
    """Get salary comparison report"""
    try:
        report = EmployeeSalaryStructureService.get_salary_comparison_report(db, department_id)
        return report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching salary comparison report: {str(e)}"
        )


# Alternative endpoints using Pydantic models
@router.post("/create", response_model=EmployeeSalaryStructureCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_employee_salary_structure(
    salary: EmployeeSalaryStructureCreate, 
    db: Session = Depends(get_db)
):
    """Create a new employee salary structure using Pydantic model"""
    try:
        # Check if salary structure already exists for employee
        exists_result = EmployeeSalaryStructureService.check_salary_structure_exists(db, salary.EmployeeId)
        if exists_result["exists"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Active salary structure already exists for this employee (ID: {exists_result['employee_salary_structure_id']})"
            )
        
        db_salary = EmployeeSalaryStructureService.create_employee_salary_structure(db, salary)
        
        # Calculate net take-home
        totals = EmployeeSalaryStructureService.calculate_salary_totals(db_salary)
        
        return {
            "success": True,
            "message": "Employee salary structure created successfully",
            "employee_salary_structure_id": db_salary.EmployeeSalaryStructureId,
            "net_takehome": totals["NETTAKEHOME"]
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
            detail=f"Error creating employee salary structure: {str(e)}"
        )


@router.put("/update/{employee_salary_structure_id}", response_model=EmployeeSalaryStructureUpdateResponse)
async def update_employee_salary_structure(
    employee_salary_structure_id: int, 
    salary: EmployeeSalaryStructureUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing employee salary structure using Pydantic model"""
    try:
        updated_salary = EmployeeSalaryStructureService.update_employee_salary_structure(
            db, employee_salary_structure_id, salary
        )
        if not updated_salary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee salary structure with ID {employee_salary_structure_id} not found"
            )
        
        # Calculate net take-home
        totals = EmployeeSalaryStructureService.calculate_salary_totals(updated_salary)
        
        # Get list of updated fields
        updated_fields = list(salary.model_dump(exclude_none=True).keys())
        
        return {
            "success": True,
            "message": "Employee salary structure updated successfully",
            "employee_salary_structure_id": employee_salary_structure_id,
            "modified_fields": updated_fields,
            "net_takehome": totals["NETTAKEHOME"]
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
            detail=f"Error updating employee salary structure: {str(e)}"
        )


@router.get("/employeesWithoutSalaryStructure", response_model=List[int])
async def get_employees_without_salary_structure(db: Session = Depends(get_db)):
    """Get list of employee IDs without active salary structures"""
    try:
        from app.models.employee import Employee
        
        # Get employees who don't have active salary structures
        subquery = db.query(EmployeeSalaryStructure.EmployeeId).filter(
            EmployeeSalaryStructure.IsActive == True
        )
        
        employees_without_salary = db.query(Employee.EmployeeId).filter(
            Employee.IsActive == True,
            ~Employee.EmployeeId.in_(subquery)
        ).all()
        
        return [emp.EmployeeId for emp in employees_without_salary]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching employees without salary structure: {str(e)}"
        )


@router.get("/calculateNetSalary/{employee_id}", response_model=dict)
async def calculate_net_salary(employee_id: int, db: Session = Depends(get_db)):
    """Calculate net salary for an employee"""
    try:
        salary = EmployeeSalaryStructureService.fetch_salary_structure_by_employee(db, employee_id)
        if not salary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No active salary structure found for employee ID {employee_id}"
            )
        
        totals = EmployeeSalaryStructureService.calculate_salary_totals(salary)
        
        return {
            "employee_id": employee_id,
            "basic_salary": salary.BASIC,
            "gross_earnings": totals["GROSSEARNINGS"],
            "gross_deductions": totals["GROSSDEDUCTIONS"],
            "net_takehome": totals["NETTAKEHOME"],
            "components": {
                "earnings": {
                    "BASIC": salary.BASIC,
                    "HRA": salary.HRA,
                    "CONVEYANCE": salary.CONVEYANCE,
                    "MEDICALALLOWANCE": salary.MEDICALALLOWANCE,
                    "SPECIALALLOWANCE": salary.SPECIALALLOWANCE,
                    "SPECIALBONUS": salary.SPECIALBONUS,
                    "STATUTORYBONUS": salary.STATUTORYBONUS,
                    "OTHERS": salary.OTHERS
                },
                "deductions": {
                    "PF": salary.PF,
                    "ESIC": salary.ESIC,
                    "PROFESSIONALTAX": salary.PROFESSIONALTAX,
                    "GroupHealthInsurance": salary.GroupHealthInsurance
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating net salary: {str(e)}"
        )


@router.post("/searchEmployeeSalaryStructures", response_model=EmployeeSalaryStructureListResponse)
async def search_employee_salary_structures(
    filters: EmployeeSalaryStructureFilterParams,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    sort_by: str = Query("EmployeeSalaryStructureId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Advanced employee salary structure search with filters"""
    try:
        skip = (page - 1) * size
        items, total = EmployeeSalaryStructureService.get_employee_salary_structures_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=filters.search_term if hasattr(filters, 'search_term') else None,
            employee_id=filters.employee_id,
            department_id=filters.department_id if hasattr(filters, 'department_id') else None,
            designation_id=filters.designation_id if hasattr(filters, 'designation_id') else None,
            min_basic=filters.min_basic,
            max_basic=filters.max_basic,
            is_active=filters.is_active,
            has_pan=filters.has_pan if hasattr(filters, 'has_pan') else None,
            has_bank_account=filters.has_bank_account if hasattr(filters, 'has_bank_account') else None,
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
            detail=f"Error searching employee salary structures: {str(e)}"
        )


@router.get("/payrollSummary", response_model=dict)
async def get_payroll_summary(db: Session = Depends(get_db)):
    """Get payroll summary for all employees"""
    try:
        active_salaries = EmployeeSalaryStructureService.fetch_active_salary_structures(db)
        
        total_monthly_payout = Decimal('0')
        total_deductions = Decimal('0')
        total_gross_earnings = Decimal('0')
        
        for salary in active_salaries:
            totals = EmployeeSalaryStructureService.calculate_salary_totals(salary)
            total_gross_earnings += totals["GROSSEARNINGS"]
            total_deductions += totals["GROSSDEDUCTIONS"]
            total_monthly_payout += totals["NETTAKEHOME"]
        
        return {
            "total_employees": len(active_salaries),
            "total_monthly_gross": total_gross_earnings,
            "total_monthly_deductions": total_deductions,
            "total_monthly_payout": total_monthly_payout,
            "average_salary_per_employee": total_monthly_payout / len(active_salaries) if active_salaries else 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching payroll summary: {str(e)}"
        )