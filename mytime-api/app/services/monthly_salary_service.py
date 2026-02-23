from sqlalchemy.orm import Session
from typing import Optional, List, Union, Dict, Any

from app.models.monthly_salary import MonthlySalary
from app.schemas.monthly_salary_schemas import (
    MonthlySalaryCreate, 
    MonthlySalaryUpdate
)

class MonthlySalaryService:
    @staticmethod
    def fetch_monthly_salary(db: Session, salary_id: int) -> Optional[MonthlySalary]:
        """Get monthly salary by ID"""
        return db.query(MonthlySalary).filter(MonthlySalary.MonthlySalaryId == salary_id).first()
    
    @staticmethod
    def fetch_all_monthly_salaries(db: Session) -> List[MonthlySalary]:
        """Get all monthly salaries"""
        return db.query(MonthlySalary).all()
    
    @staticmethod
    def create_monthly_salary(db: Session, salary_data: MonthlySalaryCreate) -> MonthlySalary:
        """Insert new monthly salary record"""
        # Convert Pydantic model to dict, excluding unset fields
        salary_dict = salary_data.model_dump(exclude_unset=True)
        salary = MonthlySalary(**salary_dict)
        db.add(salary)
        db.commit()
        db.refresh(salary)
        return salary
    
    @staticmethod
    def update_monthly_salary(db: Session, salary_id: int, salary_data: MonthlySalaryUpdate) -> MonthlySalary:
        """Update existing monthly salary record"""
        salary = db.query(MonthlySalary).filter(MonthlySalary.MonthlySalaryId == salary_id).first()
        if not salary:
            raise ValueError(f"Monthly salary record with ID {salary_id} not found for update")
        
        # Convert Pydantic model to dict, excluding unset fields
        update_data = salary_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(salary, field, value)
        
        db.commit()
        db.refresh(salary)
        return salary
    
    @staticmethod
    def insert_or_update_monthly_salary(
        db: Session, 
        salary_data: Union[MonthlySalaryCreate, Dict[str, Any]], 
        salary_id: Optional[int] = None
    ) -> MonthlySalary:
        """Insert or update monthly salary record"""
        # If salary_data is a dict, convert to appropriate Pydantic model
        if isinstance(salary_data, dict):
            if salary_id:
                salary_data = MonthlySalaryUpdate(**salary_data)
            else:
                salary_data = MonthlySalaryCreate(**salary_data)
        
        if salary_id:
            # Update existing record
            return MonthlySalaryService.update_monthly_salary(db, salary_id, salary_data)
        else:
            # Insert new record
            return MonthlySalaryService.create_monthly_salary(db, salary_data)
    
    @staticmethod
    def delete_monthly_salary(db: Session, salary_id: int) -> bool:
        """Delete monthly salary record by ID"""
        salary = db.query(MonthlySalary).filter(MonthlySalary.MonthlySalaryId == salary_id).first()
        if not salary:
            raise ValueError(f"Monthly salary record with ID {salary_id} not found for deletion")
        db.delete(salary)
        db.commit()
        return True