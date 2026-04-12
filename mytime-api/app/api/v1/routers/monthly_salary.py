from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.monthly_salary_schemas import (
    MonthlySalaryCreate,
    MonthlySalaryMultiCreate,
    MonthlySalaryResponse,
    MonthlySalaryDeleteResponse,
    MonthlySalaryUpdate,
    MonthlySalaryPublishResponse,
    MonthlySalaryWithEmployees,  # ← new
    MonthlySalaryWithEmployeesListResponse,  # ← new
)
from app.core.database import get_db
from app.services.monthly_salary_service import MonthlySalaryService

router = APIRouter()


@router.get("/fetch/{salary_id}", response_model=MonthlySalaryResponse)
async def fetch_monthly_salary(salary_id: int, db: Session = Depends(get_db)):
    """Get monthly salary by ID"""
    try:
        salary = MonthlySalaryService.fetch_monthly_salary(db, salary_id)
        if not salary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Monthly salary with ID {salary_id} not found",
            )
        return salary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching monthly salary: {str(e)}",
        )


@router.get("/fetch-all", response_model=List[MonthlySalaryResponse])
async def fetch_all_monthly_salaries(db: Session = Depends(get_db)):
    """Get all monthly salaries"""
    try:
        salaries = MonthlySalaryService.fetch_all_monthly_salaries(db)
        return salaries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching monthly salaries: {str(e)}",
        )


# ──────────────────────────────────────────────────────────────────────
# NEW ENDPOINT 1 — Paginated list of monthly salaries,
#                  each with their nested employee salaries
# ──────────────────────────────────────────────────────────────────────
@router.get(
    "/fetch-all-with-employees", response_model=MonthlySalaryWithEmployeesListResponse
)
async def fetch_all_monthly_salaries_with_employees(db: Session = Depends(get_db)):
    """Get all monthly salaries with their employee salaries"""
    try:
        records = MonthlySalaryService.fetch_all_monthly_salaries_with_employees(db)

        items = [
            MonthlySalaryWithEmployees(
                **{col: getattr(r, col) for col in r.__table__.columns.keys()},
                employee_salaries=r.employee_salaries,
                total_employees=len(r.employee_salaries),
            )
            for r in records
        ]

        return MonthlySalaryWithEmployeesListResponse(
            total=len(items),
            items=items,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching monthly salaries with employees: {str(e)}",
        )


@router.get(
    "/fetch-with-employees/{salary_id}", response_model=MonthlySalaryWithEmployees
)
async def fetch_monthly_salary_with_employees(
    salary_id: int,
    is_active_employees: Optional[bool] = Query(
        None, description="Filter employee salaries by active status"
    ),
    db: Session = Depends(get_db),
):
    """Get a single monthly salary with its nested employee salaries"""
    try:
        record = MonthlySalaryService.fetch_monthly_salary_with_employees(
            db,
            salary_id=salary_id,
            is_active_employees=is_active_employees,
        )

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Monthly salary with ID {salary_id} not found",
            )

        return MonthlySalaryWithEmployees(
            **{col: getattr(record, col) for col in record.__table__.columns.keys()},
            employee_salaries=record.employee_salaries,
            total_employees=len(record.employee_salaries),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching monthly salary with employees: {str(e)}",
        )


@router.post(
    "/create", response_model=MonthlySalaryResponse, status_code=status.HTTP_201_CREATED
)
async def create_monthly_salary(
    salary_data: MonthlySalaryCreate, db: Session = Depends(get_db)
):
    """Create a new monthly salary"""
    try:
        response = MonthlySalaryService.create_monthly_salary(db, salary_data)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating monthly salary: {str(e)}",
        )


@router.put("/update/{salary_id}", response_model=MonthlySalaryResponse)
async def update_monthly_salary(
    salary_id: int, salary_data: MonthlySalaryUpdate, db: Session = Depends(get_db)
):
    """Update an existing monthly salary"""
    try:
        response = MonthlySalaryService.update_monthly_salary(
            db, salary_id, salary_data
        )
        return response
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating monthly salary: {str(e)}",
        )


@router.post("/insert-or-update", response_model=MonthlySalaryResponse)
async def insert_or_update_monthly_salary(
    salary_data: MonthlySalaryCreate,
    salary_id: int = None,
    db: Session = Depends(get_db),
):
    """Insert or update monthly salary"""
    try:
        response = MonthlySalaryService.insert_or_update_monthly_salary(
            db, salary_data, salary_id
        )
        return response
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inserting/updating monthly salary: {str(e)}",
        )


@router.post("/publish", response_model=MonthlySalaryPublishResponse)
async def publish_monthly_salary(
    salary_data: MonthlySalaryCreate, db: Session = Depends(get_db)
):
    """Publish monthly salary for all active employees"""
    try:
        monthly_salary = MonthlySalaryService.create_monthly_salary(db, salary_data)
        success = MonthlySalaryService.publish_monthly_salary(db, monthly_salary)

        if success:
            return MonthlySalaryPublishResponse(
                success=True,
                message="Monthly salary published successfully for all active employees",
                monthly_salary_id=monthly_salary.MonthlySalaryId,
            )
        else:
            return MonthlySalaryPublishResponse(
                success=False,
                message="No active employees found to publish salary",
                monthly_salary_id=monthly_salary.MonthlySalaryId,
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error publishing monthly salary: {str(e)}",
        )


@router.post("/publish-multiple", response_model=MonthlySalaryPublishResponse)
async def publish_monthly_salary(
    salary_data: MonthlySalaryMultiCreate, db: Session = Depends(get_db)
):
    """Publish monthly salary for all active employees"""
    try:
        monthly_salary = MonthlySalaryService.create_monthly_salary(db, salary_data)
        success = MonthlySalaryService.publish_monthly_multiple_salary(
            db, monthly_salary
        )

        if success:
            return MonthlySalaryPublishResponse(
                success=True,
                message="Monthly salary published successfully for all active employees",
                monthly_salary_id=monthly_salary.MonthlySalaryId,
            )
        else:
            return MonthlySalaryPublishResponse(
                success=False,
                message="No active employees found to publish salary",
                monthly_salary_id=monthly_salary.MonthlySalaryId,
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error publishing monthly salary: {str(e)}",
        )


@router.post(
    "/publish-existing/{salary_id}", response_model=MonthlySalaryPublishResponse
)
async def publish_existing_monthly_salary(
    salary_id: int, db: Session = Depends(get_db)
):
    """Publish an existing monthly salary for all active employees"""
    try:
        monthly_salary = MonthlySalaryService.fetch_monthly_salary(db, salary_id)
        if not monthly_salary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Monthly salary with ID {salary_id} not found",
            )

        success = MonthlySalaryService.publish_monthly_salary(db, monthly_salary)

        if success:
            return MonthlySalaryPublishResponse(
                success=True,
                message="Monthly salary published successfully for all active employees",
                monthly_salary_id=monthly_salary.MonthlySalaryId,
            )
        else:
            return MonthlySalaryPublishResponse(
                success=False,
                message="No active employees found to publish salary",
                monthly_salary_id=monthly_salary.MonthlySalaryId,
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error publishing monthly salary: {str(e)}",
        )


@router.delete("/delete/{salary_id}", response_model=MonthlySalaryDeleteResponse)
async def delete_monthly_salary(salary_id: int, db: Session = Depends(get_db)):
    """Delete monthly salary by ID"""
    try:
        success = MonthlySalaryService.delete_monthly_salary(db, salary_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Monthly salary with ID {salary_id} not found for deletion",
            )
        return MonthlySalaryDeleteResponse(
            success=True,
            message=f"Monthly salary with ID {salary_id} deleted successfully",
        )
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting monthly salary: {str(e)}",
        )
