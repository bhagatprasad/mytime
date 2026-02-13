from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EmployeeEducationService:
    """Service for EmployeeEducation operations"""
    
    @staticmethod
    def fetch_employee_education(db: Session, employee_education_id: int) -> Optional[Any]:
        """Get employee education by ID"""
        try:
            from app.models.employee_education import EmployeeEducation
            return db.query(EmployeeEducation).filter(
                EmployeeEducation.EmployeeEducationId == employee_education_id
            ).first()
        except Exception as e:
            logger.error(f"Error fetching employee education {employee_education_id}: {str(e)}")
            return None
    
    @staticmethod
    def fetch_educations_by_employee(db: Session, employee_id: int) -> List[Any]:
        """Get all education records for a specific employee"""
        try:
            from app.models.employee_education import EmployeeEducation
            return db.query(EmployeeEducation).filter(
                EmployeeEducation.EmployeeId == employee_id
            ).order_by(
                desc(EmployeeEducation.YearOfCompletion)
            ).all()
        except Exception as e:
            logger.error(f"Error fetching educations for employee {employee_id}: {str(e)}")
            return []
    
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
    ) -> Tuple[List[Any], int]:
        """Get paginated employee education records with filtering and sorting"""
        try:
            from app.models.employee_education import EmployeeEducation
            
            query = db.query(EmployeeEducation)
            
            # Apply search filter
            if search and search.strip():
                search_term = f"%{search.strip()}%"
                query = query.filter(
                    or_(
                        func.coalesce(EmployeeEducation.Degree, '').ilike(search_term),
                        func.coalesce(EmployeeEducation.FeildOfStudy, '').ilike(search_term),
                        func.coalesce(EmployeeEducation.Institution, '').ilike(search_term),
                        func.coalesce(EmployeeEducation.PercentageMarks, '').ilike(search_term)
                    )
                )
            
            # Apply employee filter
            if employee_id:
                query = query.filter(EmployeeEducation.EmployeeId == employee_id)
            
            # Apply degree filter
            if degree and degree.strip():
                query = query.filter(func.lower(EmployeeEducation.Degree) == func.lower(degree.strip()))
            
            # Apply field of study filter (using FeildOfStudy)
            if field_of_study and field_of_study.strip():
                query = query.filter(func.lower(EmployeeEducation.FeildOfStudy) == func.lower(field_of_study.strip()))
            
            # Apply institution filter
            if institution and institution.strip():
                query = query.filter(func.lower(EmployeeEducation.Institution) == func.lower(institution.strip()))
            
            # Apply year range filters - FIXED: Don't use extract() function
            if year_from:
                # Create start date for the year (January 1st)
                try:
                    start_date = datetime(year_from, 1, 1)
                    query = query.filter(EmployeeEducation.YearOfCompletion >= start_date)
                except Exception as e:
                    logger.warning(f"Invalid year_from {year_from}: {str(e)}")
            
            if year_to:
                # Create end date for the year (December 31st)
                try:
                    end_date = datetime(year_to, 12, 31, 23, 59, 59)
                    query = query.filter(EmployeeEducation.YearOfCompletion <= end_date)
                except Exception as e:
                    logger.warning(f"Invalid year_to {year_to}: {str(e)}")
            
            # Apply active filter
            if is_active is not None:
                query = query.filter(EmployeeEducation.IsActive == is_active)
            
            # Get total count
            total = query.count()
            
            # Apply sorting
            sort_column_map = {
                "employee_education_id": EmployeeEducation.EmployeeEducationId,
                "employee_id": EmployeeEducation.EmployeeId,
                "degree": EmployeeEducation.Degree,
                "feild_of_study": EmployeeEducation.FeildOfStudy,
                "institution": EmployeeEducation.Institution,
                "year_of_completion": EmployeeEducation.YearOfCompletion,
                "percentage_marks": EmployeeEducation.PercentageMarks,
                "created_on": EmployeeEducation.CreatedOn,
                "is_active": EmployeeEducation.IsActive
            }
            
            sort_column = sort_column_map.get(
                sort_by.lower().replace(" ", "_"),
                EmployeeEducation.EmployeeEducationId
            )
            
            if sort_order.lower() == "asc":
                query = query.order_by(asc(sort_column))
            else:
                query = query.order_by(desc(sort_column))
            
            # Apply pagination
            items = query.offset(skip).limit(limit).all()
            
            return items, total
            
        except Exception as e:
            logger.error(f"Error in get_employee_educations_with_pagination: {str(e)}")
            return [], 0
    
    @staticmethod
    def insert_or_update_employee_education(db: Session, education_data: dict) -> Dict[str, Any]:
        """Insert or update employee education"""
        try:
            from app.models.employee_education import EmployeeEducation
            from datetime import datetime
            
            # Get EmployeeEducationId and convert to int if it's a string
            emp_edu_id = education_data.get('EmployeeEducationId')
            
            # Convert to int if it's a string, handle None case
            if emp_edu_id is not None:
                try:
                    employee_education_id = int(emp_edu_id)
                except (ValueError, TypeError):
                    employee_education_id = 0
            else:
                employee_education_id = 0
            
            # Now safe to compare
            if employee_education_id > 0:
                # Update existing education record
                db_education = db.query(EmployeeEducation).filter(
                    EmployeeEducation.EmployeeEducationId == employee_education_id
                ).first()
                
                if not db_education:
                    return {
                        "success": False, 
                        "message": "Employee education record not found", 
                        "education": None
                    }
                
                db_education.Degree = education_data.get('Degree')
                db_education.FeildOfStudy = education_data.get('FeildOfStudy')
                db_education.Institution = education_data.get('Institution')
                db_education.PercentageMarks = education_data.get('PercentageMarks')
                db_education.Year = education_data.get('Year')
                db_education.YearOfCompletion = education_data.get('YearOfCompletion')
                db_education.ModifiedOn = datetime.utcnow()
                db_education.ModifiedBy = education_data.get('ModifiedBy')

                db.commit()
                db.refresh(db_education)
                return {
                    "success": True, 
                    "message": "Employee education record updated successfully",
                    "education": db_education
                }
            else:
                # Create new education record
                # Create a copy to avoid modifying the original
                create_data = education_data.copy()
                
                # Remove EmployeeEducationId if present in create mode
                create_data.pop('EmployeeEducationId', None)
                
                # Convert string IDs to integers for the model
                if 'CreatedBy' in create_data and create_data['CreatedBy']:
                    try:
                        create_data['CreatedBy'] = int(create_data['CreatedBy'])
                    except (ValueError, TypeError):
                        pass
                        
                if 'ModifiedBy' in create_data and create_data['ModifiedBy']:
                    try:
                        create_data['ModifiedBy'] = int(create_data['ModifiedBy'])
                    except (ValueError, TypeError):
                        pass
                
                # Set CreatedOn timestamp if not provided
                if 'CreatedOn' not in create_data or not create_data.get('CreatedOn'):
                    create_data['CreatedOn'] = datetime.utcnow()
                
                # Set ModifiedOn
                create_data['ModifiedOn'] = datetime.utcnow()
                
                # Set default Active status if not provided
                if 'IsActive' not in create_data:
                    create_data['IsActive'] = True
                
                db_education = EmployeeEducation(**create_data)
                db.add(db_education)
                db.commit()
                db.refresh(db_education)
                
                return {
                    "success": True, 
                    "message": "Employee education record created successfully",
                    "education": db_education
                }
                
        except Exception as e:
            db.rollback()
            logger.error(f"Error in insert_or_update_employee_education: {str(e)}")
            return {
                "success": False, 
                "message": f"Error saving employee education record: {str(e)}",
                "education": None
            }