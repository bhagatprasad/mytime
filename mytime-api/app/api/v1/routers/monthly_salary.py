from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.monthly_salary_schemas import (
    MonthlySalaryCreate, 
    MonthlySalaryResponse, 
    MonthlySalaryDeleteResponse,
    MonthlySalaryUpdate
)
from app.core.database import get_db
from app.services.monthly_salary_service import MonthlySalaryService

router = APIRouter()    

@router.get("/fetchMonthlySalary/{salary_id}", response_model=MonthlySalaryResponse)
async def fetch_monthly_salary(salary_id: int, db: Session = Depends(get_db)):
    """Get monthly salary by ID"""
    try:
        salary = MonthlySalaryService.fetch_monthly_salary(db, salary_id)
        if not salary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Monthly salary with ID {salary_id} not found"
            )
        return salary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching monthly salary: {str(e)}"
        )
    
@router.get("/fetchAllMonthlySalaries", response_model=List[MonthlySalaryResponse])
async def fetch_all_monthly_salaries(db: Session = Depends(get_db)):
    """Get all monthly salaries (returns a simple list without pagination)"""
    try:
        salaries = MonthlySalaryService.fetch_all_monthly_salaries(db)
        return salaries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching monthly salaries: {str(e)}"
        )
    
@router.post("/InsertOrUpdateMonthlySalary", response_model=MonthlySalaryResponse)
async def insert_or_update_monthly_salary(
    salary_data: MonthlySalaryCreate,
    db: Session = Depends(get_db)
):
    """Insert or update monthly salary"""
    try:
        # Extract salary_id from the data if present
        salary_id = getattr(salary_data, 'MonthlySalaryId', None)
        
        response = MonthlySalaryService.insert_or_update_monthly_salary(
            db, 
            salary_data, 
            salary_id
        )
        return response
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inserting/updating monthly salary: {str(e)}"
        )
    
@router.delete("/deleteMonthlySalary/{salary_id}", response_model=MonthlySalaryDeleteResponse)
async def delete_monthly_salary(salary_id: int, db: Session = Depends(get_db)):
    """Delete monthly salary by ID"""
    try:
        success = MonthlySalaryService.delete_monthly_salary(db, salary_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Monthly salary with ID {salary_id} not found for deletion"
            )
        return MonthlySalaryDeleteResponse(success=True)
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting monthly salary: {str(e)}"
        )