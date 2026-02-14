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
            
            # Apply field of study filter
            if field_of_study and field_of_study.strip():
                query = query.filter(func.lower(EmployeeEducation.FeildOfStudy) == func.lower(field_of_study.strip()))
            
            # Apply institution filter
            if institution and institution.strip():
                query = query.filter(func.lower(EmployeeEducation.Institution) == func.lower(institution.strip()))
            
            # Apply year range filters
            if year_from:
                try:
                    start_date = datetime(year_from, 1, 1)
                    query = query.filter(EmployeeEducation.YearOfCompletion >= start_date)
                except Exception as e:
                    logger.warning(f"Invalid year_from {year_from}: {str(e)}")
            
            if year_to:
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
                "employeeeducationid": EmployeeEducation.EmployeeEducationId,
                "employeeid": EmployeeEducation.EmployeeId,
                "degree": EmployeeEducation.Degree,
                "feildofstudy": EmployeeEducation.FeildOfStudy,
                "institution": EmployeeEducation.Institution,
                "yearofcompletion": EmployeeEducation.YearOfCompletion,
                "percentagemarks": EmployeeEducation.PercentageMarks,
                "createdon": EmployeeEducation.CreatedOn,
                "isactive": EmployeeEducation.IsActive
            }
            
            sort_column = sort_column_map.get(
                sort_by.lower().replace(" ", "").replace("_", ""),
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
            
            # Helper function to parse dates
            def parse_date(date_value):
                if date_value is None:
                    return None
                if isinstance(date_value, datetime):
                    return date_value
                if isinstance(date_value, str):
                    try:
                        # Handle ISO format with Z
                        if date_value.endswith('Z'):
                            date_value = date_value.replace('Z', '+00:00')
                        return datetime.fromisoformat(date_value)
                    except (ValueError, TypeError):
                        try:
                            # Try common formats
                            return datetime.strptime(date_value, '%Y-%m-%dT%H:%M:%S.%fZ')
                        except:
                            try:
                                return datetime.strptime(date_value, '%Y-%m-%dT%H:%M:%SZ')
                            except:
                                logger.warning(f"Could not parse date: {date_value}")
                                return datetime.utcnow()
                return datetime.utcnow()
            
            # Helper function to parse integer IDs
            def parse_id(id_value, default=0):
                if id_value is None:
                    return default
                if isinstance(id_value, int):
                    return id_value
                if isinstance(id_value, str):
                    try:
                        return int(id_value.strip()) if id_value.strip() else default
                    except (ValueError, TypeError):
                        return default
                try:
                    return int(id_value)
                except:
                    return default
            
            # Create a copy to avoid modifying the original
            process_data = education_data.copy()
            
            # Parse ID fields
            process_data['EmployeeEducationId'] = parse_id(process_data.get('EmployeeEducationId'), 0)
            process_data['EmployeeId'] = parse_id(process_data.get('EmployeeId'), None)
            process_data['CreatedBy'] = parse_id(process_data.get('CreatedBy'), None)
            process_data['ModifiedBy'] = parse_id(process_data.get('ModifiedBy'), None)
            
            # Parse date fields
            process_data['CreatedOn'] = parse_date(process_data.get('CreatedOn'))
            process_data['ModifiedOn'] = parse_date(process_data.get('ModifiedOn'))
            process_data['YearOfCompletion'] = parse_date(process_data.get('YearOfCompletion'))
            
            # Ensure IsActive is boolean
            if 'IsActive' in process_data and process_data['IsActive'] is not None:
                if isinstance(process_data['IsActive'], str):
                    process_data['IsActive'] = process_data['IsActive'].lower() in ('true', '1', 'yes')
            else:
                process_data['IsActive'] = True
            
            employee_education_id = process_data.get('EmployeeEducationId', 0)
            
            if employee_education_id and employee_education_id > 0:
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
                
                # Update all fields
                db_education.Degree = process_data.get('Degree', db_education.Degree)
                db_education.FeildOfStudy = process_data.get('FeildOfStudy', db_education.FeildOfStudy)
                db_education.Institution = process_data.get('Institution', db_education.Institution)
                db_education.Year = process_data.get('Year', db_education.Year)
                db_education.PercentageMarks = process_data.get('PercentageMarks', db_education.PercentageMarks)
                db_education.YearOfCompletion = process_data.get('YearOfCompletion', db_education.YearOfCompletion)
                db_education.IsActive = process_data.get('IsActive', db_education.IsActive)
                db_education.ModifiedBy = process_data.get('ModifiedBy', db_education.ModifiedBy)
                db_education.ModifiedOn = datetime.utcnow()  # Always update to current time
                
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
                process_data.pop('EmployeeEducationId', None)
                
                # Set timestamps
                if not process_data.get('CreatedOn'):
                    process_data['CreatedOn'] = datetime.utcnow()
                process_data['ModifiedOn'] = datetime.utcnow()
                
                # Ensure required fields are present
                required_fields = ['Degree', 'FeildOfStudy', 'Institution', 'EmployeeId', 'Year']
                missing_fields = [field for field in required_fields if not process_data.get(field)]
                if missing_fields:
                    return {
                        "success": False,
                        "message": f"Missing required fields: {', '.join(missing_fields)}",
                        "education": None
                    }
                
                # Create new record
                db_education = EmployeeEducation(**process_data)
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
            import traceback
            logger.error(traceback.format_exc())
            return {
                "success": False, 
                "message": f"Error saving employee education record: {str(e)}",
                "education": None
            }
    
    @staticmethod
    def delete_employee_education(db: Session, employee_education_id: int) -> Dict[str, Any]:
        """Delete employee education record"""
        try:
            from app.models.employee_education import EmployeeEducation
            
            db_education = db.query(EmployeeEducation).filter(
                EmployeeEducation.EmployeeEducationId == employee_education_id
            ).first()
            
            if not db_education:
                return {
                    "success": False, 
                    "message": "Employee education record not found"
                }
            
            db.delete(db_education)
            db.commit()
            
            return {
                "success": True, 
                "message": "Employee education record deleted successfully"
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting employee education {employee_education_id}: {str(e)}")
            return {
                "success": False, 
                "message": f"Error deleting employee education record: {str(e)}"
            }