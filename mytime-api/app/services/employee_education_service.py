from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func, extract
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
    def insert_or_update_employee_education(db: Session, education_data: dict) -> Dict[str, Any]:
        """Insert or update employee education"""
        try:
            from app.models.employee_education import EmployeeEducation
            
            # Map field_of_study to FeildOfStudy if present
            if 'field_of_study' in education_data:
                education_data['FeildOfStudy'] = education_data.pop('field_of_study')
            
            # Handle YearOfCompletion
            if 'YearOfCompletion' in education_data and education_data['YearOfCompletion']:
                try:
                    year_data = education_data['YearOfCompletion']
                    if isinstance(year_data, str) and year_data.isdigit():
                        # Convert year string to datetime (January 1st of that year)
                        year_int = int(year_data)
                        education_data['YearOfCompletion'] = datetime(year_int, 1, 1)
                    elif isinstance(year_data, int):
                        education_data['YearOfCompletion'] = datetime(year_data, 1, 1)
                except Exception as e:
                    logger.warning(f"Error parsing YearOfCompletion {education_data['YearOfCompletion']}: {str(e)}")
                    education_data['YearOfCompletion'] = None
            
            employee_education_id = education_data.get('EmployeeEducationId')
            
            # Handle EmployeeEducationId properly
            if employee_education_id:
                try:
                    employee_education_id = int(employee_education_id)
                except (ValueError, TypeError):
                    employee_education_id = 0
            
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
                if 'CreatedOn' not in education_data or not education_data['CreatedOn']:
                    education_data['CreatedOn'] = datetime.utcnow()
                
                # Set default Active status if not provided
                if 'IsActive' not in education_data:
                    education_data['IsActive'] = True
                
                # Validate required fields
                if 'EmployeeId' not in education_data or not education_data['EmployeeId']:
                    return {
                        "success": False,
                        "message": "EmployeeId is required",
                        "education": None
                    }
                
                if 'Degree' not in education_data or not education_data['Degree']:
                    return {
                        "success": False,
                        "message": "Degree is required",
                        "education": None
                    }
                
                if 'FeildOfStudy' not in education_data or not education_data['FeildOfStudy']:
                    return {
                        "success": False,
                        "message": "FeildOfStudy is required",
                        "education": None
                    }
                
                db_education = EmployeeEducation(**education_data)
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