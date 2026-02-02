from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func, extract
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal

from app.models.employee_employment import EmployeeEmployment
from app.schemas.employee_employment_schemas import EmployeeEmploymentCreate, EmployeeEmploymentUpdate

class EmployeeEmploymentService:
    """Service for EmployeeEmployment operations"""
    
    @staticmethod
    def fetch_employee_employment(db: Session, employee_employment_id: int) -> Optional[EmployeeEmployment]:
        """Get employee employment by ID"""
        return db.query(EmployeeEmployment).filter(
            EmployeeEmployment.EmployeeEmploymentId == employee_employment_id
        ).first()
    
    @staticmethod
    def fetch_employments_by_employee(db: Session, employee_id: int) -> List[EmployeeEmployment]:
        """Get all employment records for a specific employee"""
        return db.query(EmployeeEmployment).filter(
            EmployeeEmployment.EmployeeId == employee_id
        ).order_by(
            desc(EmployeeEmployment.StartedOn)
        ).all()
    
    @staticmethod
    def fetch_active_employments_by_employee(db: Session, employee_id: int) -> List[EmployeeEmployment]:
        """Get active employment records for a specific employee"""
        return db.query(EmployeeEmployment).filter(
            EmployeeEmployment.EmployeeId == employee_id,
            EmployeeEmployment.IsActive == True
        ).order_by(
            desc(EmployeeEmployment.StartedOn)
        ).all()
    
    @staticmethod
    def fetch_latest_employment_by_employee(db: Session, employee_id: int) -> Optional[EmployeeEmployment]:
        """Get latest employment record for an employee"""
        return db.query(EmployeeEmployment).filter(
            EmployeeEmployment.EmployeeId == employee_id,
            EmployeeEmployment.IsActive == True
        ).order_by(
            desc(EmployeeEmployment.StartedOn)
        ).first()
    
    @staticmethod
    def fetch_all_employee_employments(db: Session) -> List[EmployeeEmployment]:
        """Get all employee employment records"""
        return db.query(EmployeeEmployment).all()
    
    @staticmethod
    def get_employee_employments_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        employee_id: Optional[int] = None,
        company_name: Optional[str] = None,
        designation: Optional[str] = None,
        start_year_from: Optional[int] = None,
        start_year_to: Optional[int] = None,
        end_year_from: Optional[int] = None,
        end_year_to: Optional[int] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "EmployeeEmploymentId",
        sort_order: str = "desc"
    ) -> Tuple[List[EmployeeEmployment], int]:
        """Get paginated employee employment records with filtering and sorting"""
        query = db.query(EmployeeEmployment)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(EmployeeEmployment.CompanyName, '').ilike(search_term),
                    func.coalesce(EmployeeEmployment.Designation, '').ilike(search_term),
                    func.coalesce(EmployeeEmployment.Address, '').ilike(search_term),
                    func.coalesce(EmployeeEmployment.Reason, '').ilike(search_term),
                    func.coalesce(EmployeeEmployment.ReportingManager, '').ilike(search_term),
                    func.coalesce(EmployeeEmployment.Reference, '').ilike(search_term)
                )
            )
        
        # Apply employee filter
        if employee_id:
            query = query.filter(EmployeeEmployment.EmployeeId == employee_id)
        
        # Apply company name filter
        if company_name:
            query = query.filter(func.lower(EmployeeEmployment.CompanyName) == func.lower(company_name))
        
        # Apply designation filter
        if designation:
            query = query.filter(func.lower(EmployeeEmployment.Designation) == func.lower(designation))
        
        # Apply start year range filters
        if start_year_from:
            query = query.filter(
                extract('year', EmployeeEmployment.StartedOn) >= start_year_from
            )
        if start_year_to:
            query = query.filter(
                extract('year', EmployeeEmployment.StartedOn) <= start_year_to
            )
        
        # Apply end year range filters
        if end_year_from:
            query = query.filter(
                extract('year', EmployeeEmployment.EndedOn) >= end_year_from
            )
        if end_year_to:
            query = query.filter(
                extract('year', EmployeeEmployment.EndedOn) <= end_year_to
            )
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(EmployeeEmployment.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(EmployeeEmployment, sort_by, EmployeeEmployment.EmployeeEmploymentId)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def insert_or_update_employee_employment(db: Session, employment_data: dict) -> Dict[str, Any]:
        """Insert or update employee employment"""
        employee_employment_id = employment_data.get('EmployeeEmploymentId')
        
        if employee_employment_id:
            # Update existing employment record
            db_employment = db.query(EmployeeEmployment).filter(
                EmployeeEmployment.EmployeeEmploymentId == employee_employment_id
            ).first()
            
            if not db_employment:
                return {"success": False, "message": "Employee employment record not found", "employment": None}
            
            # Update only non-null values
            for key, value in employment_data.items():
                if key != 'EmployeeEmploymentId' and value is not None:
                    setattr(db_employment, key, value)
            
            # Set ModifiedOn timestamp
            db_employment.ModifiedOn = datetime.utcnow()
            
            db.commit()
            db.refresh(db_employment)
            return {
                "success": True, 
                "message": "Employee employment record updated successfully",
                "employment": db_employment
            }
        else:
            # Create new employment record
            # Remove EmployeeEmploymentId if present in create mode
            employment_data.pop('EmployeeEmploymentId', None)
            
            # Set CreatedOn timestamp if not provided
            if 'CreatedOn' not in employment_data:
                employment_data['CreatedOn'] = datetime.utcnow()
            
            db_employment = EmployeeEmployment(**employment_data)
            db.add(db_employment)
            db.commit()
            db.refresh(db_employment)
            return {
                "success": True, 
                "message": "Employee employment record created successfully",
                "employment": db_employment
            }
    
    @staticmethod
    def delete_employee_employment(db: Session, employee_employment_id: int) -> Dict[str, Any]:
        """Delete employee employment record"""
        db_employment = db.query(EmployeeEmployment).filter(
            EmployeeEmployment.EmployeeEmploymentId == employee_employment_id
        ).first()
        
        if not db_employment:
            return {"success": False, "message": "Employee employment record not found"}
        
        db.delete(db_employment)
        db.commit()
        return {"success": True, "message": "Employee employment record deleted successfully"}
    
    @staticmethod
    def soft_delete_employee_employment(
        db: Session, 
        employee_employment_id: int, 
        modified_by: int
    ) -> Dict[str, Any]:
        """Soft delete employee employment record (set IsActive = False)"""
        db_employment = db.query(EmployeeEmployment).filter(
            EmployeeEmployment.EmployeeEmploymentId == employee_employment_id
        ).first()
        
        if not db_employment:
            return {"success": False, "message": "Employee employment record not found"}
        
        db_employment.IsActive = False
        db_employment.ModifiedBy = modified_by
        db_employment.ModifiedOn = datetime.utcnow()
        
        db.commit()
        db.refresh(db_employment)
        return {
            "success": True, 
            "message": "Employee employment record deactivated successfully",
            "employment": db_employment
        }
    
    @staticmethod
    def create_employee_employment(db: Session, employment: EmployeeEmploymentCreate) -> EmployeeEmployment:
        """Create new employee employment using Pydantic schema"""
        employment_data = employment.model_dump(exclude_none=True)
        
        # Set CreatedOn timestamp if not provided
        if 'CreatedOn' not in employment_data:
            employment_data['CreatedOn'] = datetime.utcnow()
        
        db_employment = EmployeeEmployment(**employment_data)
        db.add(db_employment)
        db.commit()
        db.refresh(db_employment)
        return db_employment
    
    @staticmethod
    def update_employee_employment(
        db: Session, 
        employee_employment_id: int, 
        employment: EmployeeEmploymentUpdate
    ) -> Optional[EmployeeEmployment]:
        """Update existing employee employment using Pydantic schema"""
        db_employment = db.query(EmployeeEmployment).filter(
            EmployeeEmployment.EmployeeEmploymentId == employee_employment_id
        ).first()
        
        if db_employment:
            update_data = employment.model_dump(exclude_none=True)
            
            # Set ModifiedOn timestamp
            update_data['ModifiedOn'] = datetime.utcnow()
            
            for key, value in update_data.items():
                setattr(db_employment, key, value)
            
            db.commit()
            db.refresh(db_employment)
        
        return db_employment
    
    @staticmethod
    def check_employment_exists(
        db: Session, 
        employee_id: int, 
        company_name: str,
        designation: str,
        started_on: datetime
    ) -> Dict[str, Any]:
        """Check if employment record exists for employee"""
        employment = db.query(EmployeeEmployment).filter(
            EmployeeEmployment.EmployeeId == employee_id,
            func.lower(EmployeeEmployment.CompanyName) == func.lower(company_name),
            func.lower(EmployeeEmployment.Designation) == func.lower(designation),
            extract('year', EmployeeEmployment.StartedOn) == started_on.year,
            extract('month', EmployeeEmployment.StartedOn) == started_on.month
        ).first()
        
        return {
            "exists": employment is not None,
            "employee_employment_id": employment.EmployeeEmploymentId if employment else None
        }
    
    @staticmethod
    def get_employee_employment_summary(db: Session, employee_id: int) -> Dict[str, Any]:
        """Get employment summary for an employee"""
        employments = db.query(EmployeeEmployment).filter(
            EmployeeEmployment.EmployeeId == employee_id,
            EmployeeEmployment.IsActive == True
        ).order_by(
            desc(EmployeeEmployment.StartedOn)
        ).all()
        
        latest_employment = employments[0] if employments else None
        
        # Calculate total experience in months
        total_experience_months = 0
        for emp in employments:
            if emp.StartedOn:
                end_date = emp.EndedOn or datetime.utcnow()
                months = (end_date.year - emp.StartedOn.year) * 12 + (end_date.month - emp.StartedOn.month)
                total_experience_months += max(0, months)
        
        # Group by company
        by_company = {}
        for emp in employments:
            company = emp.CompanyName
            if company not in by_company:
                by_company[company] = []
            by_company[company].append({
                "id": emp.EmployeeEmploymentId,
                "designation": emp.Designation,
                "started_on": emp.StartedOn,
                "ended_on": emp.EndedOn
            })
        
        return {
            "total_records": len(employments),
            "latest_employment": latest_employment,
            "total_experience_months": total_experience_months,
            "total_experience_years": round(total_experience_months / 12, 1),
            "employments_by_company": by_company,
            "all_employments": employments
        }
    
    @staticmethod
    def create_bulk_employments(
        db: Session, 
        employments: List[EmployeeEmploymentCreate],
        employee_id: Optional[int] = None
    ) -> List[EmployeeEmployment]:
        """Create multiple employment records at once"""
        db_employments = []
        
        for employment_data in employments:
            # If employee_id is provided, override the EmployeeId in each employment
            if employee_id:
                employment_data.EmployeeId = employee_id
            
            employment_dict = employment_data.model_dump(exclude_none=True)
            employment_dict['CreatedOn'] = datetime.utcnow()
            
            db_employment = EmployeeEmployment(**employment_dict)
            db.add(db_employment)
            db_employments.append(db_employment)
        
        db.commit()
        
        # Refresh all employments
        for employment in db_employments:
            db.refresh(employment)
        
        return db_employments
    
    @staticmethod
    def get_employment_statistics(db: Session) -> Dict[str, Any]:
        """Get employment statistics"""
        # Total records
        total_records = db.query(func.count(EmployeeEmployment.EmployeeEmploymentId)).scalar()
        
        # Count by company
        company_counts = db.query(
            EmployeeEmployment.CompanyName,
            func.count(EmployeeEmployment.EmployeeEmploymentId).label('count')
        ).filter(
            EmployeeEmployment.CompanyName.isnot(None),
            EmployeeEmployment.IsActive == True
        ).group_by(
            EmployeeEmployment.CompanyName
        ).all()
        
        # Count by designation
        designation_counts = db.query(
            EmployeeEmployment.Designation,
            func.count(EmployeeEmployment.EmployeeEmploymentId).label('count')
        ).filter(
            EmployeeEmployment.Designation.isnot(None),
            EmployeeEmployment.IsActive == True
        ).group_by(
            EmployeeEmployment.Designation
        ).all()
        
        # Count by start year
        year_counts = db.query(
            extract('year', EmployeeEmployment.StartedOn).label('year'),
            func.count(EmployeeEmployment.EmployeeEmploymentId).label('count')
        ).filter(
            EmployeeEmployment.StartedOn.isnot(None),
            EmployeeEmployment.IsActive == True
        ).group_by(
            extract('year', EmployeeEmployment.StartedOn)
        ).all()
        
        # Calculate average duration
        duration_query = db.query(
            func.avg(
                func.extract('epoch', func.coalesce(EmployeeEmployment.EndedOn, func.now())) -
                func.extract('epoch', EmployeeEmployment.StartedOn)
            ).label('avg_duration_seconds')
        ).filter(
            EmployeeEmployment.StartedOn.isnot(None),
            EmployeeEmployment.IsActive == True
        ).scalar()
        
        avg_duration_months = 0
        if duration_query:
            avg_duration_days = duration_query / (60 * 60 * 24)
            avg_duration_months = round(avg_duration_days / 30.44, 1)  # Approximate month calculation
        
        return {
            "total_records": total_records,
            "by_company": {company: count for company, count in company_counts},
            "by_designation": {designation: count for designation, count in designation_counts},
            "by_year": {int(year): count for year, count in year_counts if year},
            "average_duration_months": avg_duration_months
        }
    
    @staticmethod
    def get_employees_by_previous_company(db: Session, company_name: str) -> List[int]:
        """Get employee IDs who worked at a specific company"""
        employees = db.query(
            func.distinct(EmployeeEmployment.EmployeeId)
        ).filter(
            func.lower(EmployeeEmployment.CompanyName) == func.lower(company_name),
            EmployeeEmployment.IsActive == True
        ).all()
        
        return [emp[0] for emp in employees]