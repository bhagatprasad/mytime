from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func, extract
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

from app.models.employee_education import EmployeeEducation
from app.schemas.employee_education_schemas import EmployeeEducationCreate, EmployeeEducationUpdate

class EmployeeEducationService:
    """Service for EmployeeEducation operations"""
    
    @staticmethod
    def fetch_employee_education(db: Session, employee_education_id: int) -> Optional[EmployeeEducation]:
        """Get employee education by ID"""
        return db.query(EmployeeEducation).filter(
            EmployeeEducation.EmployeeEducationId == employee_education_id
        ).first()
    
    @staticmethod
    def fetch_educations_by_employee(db: Session, employee_id: int) -> List[EmployeeEducation]:
        """Get all education records for a specific employee"""
        return db.query(EmployeeEducation).filter(
            EmployeeEducation.EmployeeId == employee_id
        ).order_by(
            desc(EmployeeEducation.YearOfCompletion)
        ).all()
    
    @staticmethod
    def fetch_active_educations_by_employee(db: Session, employee_id: int) -> List[EmployeeEducation]:
        """Get active education records for a specific employee"""
        return db.query(EmployeeEducation).filter(
            EmployeeEducation.EmployeeId == employee_id,
            EmployeeEducation.IsActive == True
        ).order_by(
            desc(EmployeeEducation.YearOfCompletion)
        ).all()
    
    @staticmethod
    def fetch_highest_education_by_employee(db: Session, employee_id: int) -> Optional[EmployeeEducation]:
        """Get highest (latest) education record for an employee"""
        return db.query(EmployeeEducation).filter(
            EmployeeEducation.EmployeeId == employee_id,
            EmployeeEducation.IsActive == True
        ).order_by(
            desc(EmployeeEducation.YearOfCompletion)
        ).first()
    
    @staticmethod
    def fetch_all_employee_educations(db: Session) -> List[EmployeeEducation]:
        """Get all employee education records"""
        return db.query(EmployeeEducation).all()
    
    @staticmethod
    def get_employee_educations_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        employee_id: Optional[int] = None,
        degree: Optional[str] = None,
        field_of_study: Optional[str] = None,
        institution: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "EmployeeEducationId",
        sort_order: str = "desc"
    ) -> Tuple[List[EmployeeEducation], int]:
        """Get paginated employee education records with filtering and sorting"""
        query = db.query(EmployeeEducation)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(EmployeeEducation.Degree, '').ilike(search_term),
                    func.coalesce(EmployeeEducation.FieldOfStudy, '').ilike(search_term),
                    func.coalesce(EmployeeEducation.Institution, '').ilike(search_term),
                    func.coalesce(EmployeeEducation.PercentageMarks, '').ilike(search_term)
                )
            )
        
        # Apply employee filter
        if employee_id:
            query = query.filter(EmployeeEducation.EmployeeId == employee_id)
        
        # Apply degree filter
        if degree:
            query = query.filter(func.lower(EmployeeEducation.Degree) == func.lower(degree))
        
        # Apply field of study filter
        if field_of_study:
            query = query.filter(func.lower(EmployeeEducation.FieldOfStudy) == func.lower(field_of_study))
        
        # Apply institution filter
        if institution:
            query = query.filter(func.lower(EmployeeEducation.Institution) == func.lower(institution))
        
        # Apply year range filters
        if year_from:
            query = query.filter(
                extract('year', EmployeeEducation.YearOfCompletion) >= year_from
            )
        if year_to:
            query = query.filter(
                extract('year', EmployeeEducation.YearOfCompletion) <= year_to
            )
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(EmployeeEducation.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(EmployeeEducation, sort_by, EmployeeEducation.EmployeeEducationId)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def insert_or_update_employee_education(db: Session, education_data: dict) -> Dict[str, Any]:
        """Insert or update employee education"""
        employee_education_id = education_data.get('EmployeeEducationId')
        
        if employee_education_id:
            # Update existing education record
            db_education = db.query(EmployeeEducation).filter(
                EmployeeEducation.EmployeeEducationId == employee_education_id
            ).first()
            
            if not db_education:
                return {"success": False, "message": "Employee education record not found", "education": None}
            
            # Update only non-null values
            for key, value in education_data.items():
                if key != 'EmployeeEducationId' and value is not None:
                    setattr(db_education, key, value)
            
            # Set ModifiedOn timestamp
            db_education.ModifiedOn = datetime.utcnow()
            
            db.commit()
            db.refresh(db_education)
            return {
                "success": True, 
                "message": "Employee education record updated successfully",
                "education": db_education
            }
        else:
            # Create new education record
            # Remove EmployeeEducationId if present in create mode
            education_data.pop('EmployeeEducationId', None)
            
            # Set CreatedOn timestamp if not provided
            if 'CreatedOn' not in education_data:
                education_data['CreatedOn'] = datetime.utcnow()
            
            db_education = EmployeeEducation(**education_data)
            db.add(db_education)
            db.commit()
            db.refresh(db_education)
            return {
                "success": True, 
                "message": "Employee education record created successfully",
                "education": db_education
            }
    
    @staticmethod
    def delete_employee_education(db: Session, employee_education_id: int) -> Dict[str, Any]:
        """Delete employee education record"""
        db_education = db.query(EmployeeEducation).filter(
            EmployeeEducation.EmployeeEducationId == employee_education_id
        ).first()
        
        if not db_education:
            return {"success": False, "message": "Employee education record not found"}
        
        db.delete(db_education)
        db.commit()
        return {"success": True, "message": "Employee education record deleted successfully"}
    
    @staticmethod
    def soft_delete_employee_education(
        db: Session, 
        employee_education_id: int, 
        modified_by: int
    ) -> Dict[str, Any]:
        """Soft delete employee education record (set IsActive = False)"""
        db_education = db.query(EmployeeEducation).filter(
            EmployeeEducation.EmployeeEducationId == employee_education_id
        ).first()
        
        if not db_education:
            return {"success": False, "message": "Employee education record not found"}
        
        db_education.IsActive = False
        db_education.ModifiedBy = modified_by
        db_education.ModifiedOn = datetime.utcnow()
        
        db.commit()
        db.refresh(db_education)
        return {
            "success": True, 
            "message": "Employee education record deactivated successfully",
            "education": db_education
        }
    
    @staticmethod
    def create_employee_education(db: Session, education: EmployeeEducationCreate) -> EmployeeEducation:
        """Create new employee education using Pydantic schema"""
        education_data = education.model_dump(exclude_none=True)
        
        # Set CreatedOn timestamp if not provided
        if 'CreatedOn' not in education_data:
            education_data['CreatedOn'] = datetime.utcnow()
        
        db_education = EmployeeEducation(**education_data)
        db.add(db_education)
        db.commit()
        db.refresh(db_education)
        return db_education
    
    @staticmethod
    def update_employee_education(
        db: Session, 
        employee_education_id: int, 
        education: EmployeeEducationUpdate
    ) -> Optional[EmployeeEducation]:
        """Update existing employee education using Pydantic schema"""
        db_education = db.query(EmployeeEducation).filter(
            EmployeeEducation.EmployeeEducationId == employee_education_id
        ).first()
        
        if db_education:
            update_data = education.model_dump(exclude_none=True)
            
            # Set ModifiedOn timestamp
            update_data['ModifiedOn'] = datetime.utcnow()
            
            for key, value in update_data.items():
                setattr(db_education, key, value)
            
            db.commit()
            db.refresh(db_education)
        
        return db_education
    
    @staticmethod
    def check_education_exists(
        db: Session, 
        employee_id: int, 
        degree: str,
        institution: str
    ) -> Dict[str, Any]:
        """Check if education record exists for employee"""
        education = db.query(EmployeeEducation).filter(
            EmployeeEducation.EmployeeId == employee_id,
            func.lower(EmployeeEducation.Degree) == func.lower(degree),
            func.lower(EmployeeEducation.Institution) == func.lower(institution)
        ).first()
        
        return {
            "exists": education is not None,
            "employee_education_id": education.EmployeeEducationId if education else None
        }
    
    @staticmethod
    def get_employee_education_summary(db: Session, employee_id: int) -> Dict[str, Any]:
        """Get education summary for an employee"""
        educations = db.query(EmployeeEducation).filter(
            EmployeeEducation.EmployeeId == employee_id,
            EmployeeEducation.IsActive == True
        ).order_by(
            desc(EmployeeEducation.YearOfCompletion)
        ).all()
        
        highest_education = educations[0] if educations else None
        
        return {
            "total_records": len(educations),
            "highest_education": highest_education,
            "educations": educations,
            "degrees": list(set([e.Degree for e in educations if e.Degree])),
            "institutions": list(set([e.Institution for e in educations if e.Institution]))
        }
    
    @staticmethod
    def create_bulk_educations(
        db: Session, 
        educations: List[EmployeeEducationCreate],
        employee_id: Optional[int] = None
    ) -> List[EmployeeEducation]:
        """Create multiple education records at once"""
        db_educations = []
        
        for education_data in educations:
            # If employee_id is provided, override the EmployeeId in each education
            if employee_id:
                education_data.EmployeeId = employee_id
            
            education_dict = education_data.model_dump(exclude_none=True)
            education_dict['CreatedOn'] = datetime.utcnow()
            
            db_education = EmployeeEducation(**education_dict)
            db.add(db_education)
            db_educations.append(db_education)
        
        db.commit()
        
        # Refresh all educations
        for education in db_educations:
            db.refresh(education)
        
        return db_educations
    
    @staticmethod
    def get_education_statistics(db: Session) -> Dict[str, Any]:
        """Get education statistics"""
        # Total records
        total_records = db.query(func.count(EmployeeEducation.EmployeeEducationId)).scalar()
        
        # Count by degree
        degree_counts = db.query(
            EmployeeEducation.Degree,
            func.count(EmployeeEducation.EmployeeEducationId).label('count')
        ).filter(
            EmployeeEducation.Degree.isnot(None),
            EmployeeEducation.IsActive == True
        ).group_by(
            EmployeeEducation.Degree
        ).all()
        
        # Count by institution
        institution_counts = db.query(
            EmployeeEducation.Institution,
            func.count(EmployeeEducation.EmployeeEducationId).label('count')
        ).filter(
            EmployeeEducation.Institution.isnot(None),
            EmployeeEducation.IsActive == True
        ).group_by(
            EmployeeEducation.Institution
        ).all()
        
        # Count by year
        year_counts = db.query(
            extract('year', EmployeeEducation.YearOfCompletion).label('year'),
            func.count(EmployeeEducation.EmployeeEducationId).label('count')
        ).filter(
            EmployeeEducation.YearOfCompletion.isnot(None),
            EmployeeEducation.IsActive == True
        ).group_by(
            extract('year', EmployeeEducation.YearOfCompletion)
        ).all()
        
        return {
            "total_records": total_records,
            "degrees": {degree: count for degree, count in degree_counts},
            "institutions": {institution: count for institution, count in institution_counts},
            "by_year": {int(year): count for year, count in year_counts if year}
        }