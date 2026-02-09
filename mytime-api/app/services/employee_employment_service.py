from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, timedelta
import logging

from app.models.employee_employment import EmployeeEmployment
from app.schemas.employee_employment_schemas import EmployeeEmploymentCreate, EmployeeEmploymentUpdate

logger = logging.getLogger(__name__)

class EmployeeEmploymentService:
    """Service for EmployeeEmployment operations"""
    
    @staticmethod
    def fetch_employee_employment(db: Session, employee_employment_id: int) -> Optional[EmployeeEmployment]:
        """Get employee employment by ID"""
        try:
            return db.query(EmployeeEmployment).filter(
                EmployeeEmployment.EmployeeEmploymentId == employee_employment_id
            ).first()
        except Exception as e:
            logger.error(f"Error fetching employee employment {employee_employment_id}: {str(e)}")
            return None
    
    @staticmethod
    def fetch_employments_by_employee(db: Session, employee_id: int) -> List[EmployeeEmployment]:
        """Get all employment records for a specific employee"""
        try:
            return db.query(EmployeeEmployment).filter(
                EmployeeEmployment.EmployeeId == employee_id
            ).order_by(
                desc(EmployeeEmployment.StartedOn)
            ).all()
        except Exception as e:
            logger.error(f"Error fetching employments for employee {employee_id}: {str(e)}")
            return []
    
    @staticmethod
    def fetch_active_employments_by_employee(db: Session, employee_id: int) -> List[EmployeeEmployment]:
        """Get active employment records for a specific employee"""
        try:
            return db.query(EmployeeEmployment).filter(
                EmployeeEmployment.EmployeeId == employee_id,
                EmployeeEmployment.IsActive == True
            ).order_by(
                desc(EmployeeEmployment.StartedOn)
            ).all()
        except Exception as e:
            logger.error(f"Error fetching active employments for employee {employee_id}: {str(e)}")
            return []
    
    @staticmethod
    def fetch_latest_employment_by_employee(db: Session, employee_id: int) -> Optional[EmployeeEmployment]:
        """Get latest employment record for an employee"""
        try:
            return db.query(EmployeeEmployment).filter(
                EmployeeEmployment.EmployeeId == employee_id,
                EmployeeEmployment.IsActive == True
            ).order_by(
                desc(EmployeeEmployment.StartedOn)
            ).first()
        except Exception as e:
            logger.error(f"Error fetching latest employment for employee {employee_id}: {str(e)}")
            return None
    
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
        try:
            query = db.query(EmployeeEmployment)
            
            # Apply search filter
            if search and search.strip():
                search_term = f"%{search.strip()}%"
                query = query.filter(
                    or_(
                        func.coalesce(EmployeeEmployment.CompanyName, '').ilike(search_term),
                        func.coalesce(EmployeeEmployment.Designation, '').ilike(search_term),
                        func.coalesce(EmployeeEmployment.Address, '').ilike(search_term),
                        func.coalesce(EmployeeEmployment.Reason, '').ilike(search_term),
                        func.coalesce(EmployeeEmployment.ReportingManager, '').ilike(search_term),
                        func.coalesce(EmployeeEmployment.Referance, '').ilike(search_term)  # Fixed field name
                    )
                )
            
            # Apply employee filter
            if employee_id:
                query = query.filter(EmployeeEmployment.EmployeeId == employee_id)
            
            # Apply company name filter
            if company_name and company_name.strip():
                query = query.filter(func.lower(EmployeeEmployment.CompanyName) == func.lower(company_name.strip()))
            
            # Apply designation filter
            if designation and designation.strip():
                query = query.filter(func.lower(EmployeeEmployment.Designation) == func.lower(designation.strip()))
            
            # Apply start year range filters - FIXED: Handle datetime properly
            if start_year_from:
                start_date = datetime(start_year_from, 1, 1)
                query = query.filter(EmployeeEmployment.StartedOn >= start_date)
            
            if start_year_to:
                end_date = datetime(start_year_to, 12, 31, 23, 59, 59)
                query = query.filter(EmployeeEmployment.StartedOn <= end_date)
            
            # Apply end year range filters - FIXED: Handle datetime properly
            if end_year_from:
                start_date = datetime(end_year_from, 1, 1)
                query = query.filter(EmployeeEmployment.EndedOn >= start_date)
            
            if end_year_to:
                end_date = datetime(end_year_to, 12, 31, 23, 59, 59)
                query = query.filter(EmployeeEmployment.EndedOn <= end_date)
            
            # Apply active filter
            if is_active is not None:
                query = query.filter(EmployeeEmployment.IsActive == is_active)
            
            # Get total count
            total = query.count()
            
            # Apply sorting
            sort_column_map = {
                "employee_employment_id": EmployeeEmployment.EmployeeEmploymentId,
                "employee_id": EmployeeEmployment.EmployeeId,
                "company_name": EmployeeEmployment.CompanyName,
                "designation": EmployeeEmployment.Designation,
                "started_on": EmployeeEmployment.StartedOn,
                "ended_on": EmployeeEmployment.EndedOn,
                "created_on": EmployeeEmployment.CreatedOn,
                "is_active": EmployeeEmployment.IsActive
            }
            
            sort_column = sort_column_map.get(
                sort_by.lower().replace(" ", "_"),
                EmployeeEmployment.EmployeeEmploymentId
            )
            
            if sort_order.lower() == "asc":
                query = query.order_by(asc(sort_column))
            else:
                query = query.order_by(desc(sort_column))
            
            # Apply pagination
            items = query.offset(skip).limit(limit).all()
            
            return items, total
            
        except Exception as e:
            logger.error(f"Error in get_employee_employments_with_pagination: {str(e)}")
            return [], 0
    
    @staticmethod
    def insert_or_update_employee_employment(db: Session, employment_data: dict) -> Dict[str, Any]:
        """Insert or update employee employment"""
        try:
            # Map "Reference" to "Referance" if needed (frontend might send correct spelling)
            if 'Reference' in employment_data:
                employment_data['Referance'] = employment_data.pop('Reference')
            
            # Convert EmployeeId to BigInteger if needed
            if 'EmployeeId' in employment_data:
                employment_data['EmployeeId'] = int(employment_data['EmployeeId'])
            
            employee_employment_id = employment_data.get('EmployeeEmploymentId')
            
            # Handle EmployeeEmploymentId properly
            if employee_employment_id:
                try:
                    employee_employment_id = int(employee_employment_id)
                except (ValueError, TypeError):
                    employee_employment_id = 0
            
            if employee_employment_id and employee_employment_id > 0:
                # Update existing employment record
                db_employment = db.query(EmployeeEmployment).filter(
                    EmployeeEmployment.EmployeeEmploymentId == employee_employment_id
                ).first()
                
                if not db_employment:
                    return {
                        "success": False, 
                        "message": "Employee employment record not found", 
                        "employment": None
                    }
                
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
                if 'CreatedOn' not in employment_data or not employment_data['CreatedOn']:
                    employment_data['CreatedOn'] = datetime.utcnow()
                
                # Set default Active status if not provided
                if 'IsActive' not in employment_data:
                    employment_data['IsActive'] = True
                
                # Validate required fields
                if 'EmployeeId' not in employment_data or not employment_data['EmployeeId']:
                    return {
                        "success": False,
                        "message": "EmployeeId is required",
                        "employment": None
                    }
                
                if 'CompanyName' not in employment_data or not employment_data['CompanyName']:
                    return {
                        "success": False,
                        "message": "CompanyName is required",
                        "employment": None
                    }
                
                if 'Designation' not in employment_data or not employment_data['Designation']:
                    return {
                        "success": False,
                        "message": "Designation is required",
                        "employment": None
                    }
                
                if 'StartedOn' not in employment_data or not employment_data['StartedOn']:
                    return {
                        "success": False,
                        "message": "StartedOn is required",
                        "employment": None
                    }
                
                db_employment = EmployeeEmployment(**employment_data)
                db.add(db_employment)
                db.commit()
                db.refresh(db_employment)
                
                return {
                    "success": True, 
                    "message": "Employee employment record created successfully",
                    "employment": db_employment
                }
                
        except Exception as e:
            db.rollback()
            logger.error(f"Error in insert_or_update_employee_employment: {str(e)}")
            return {
                "success": False, 
                "message": f"Error saving employee employment record: {str(e)}",
                "employment": None
            }
    
    @staticmethod
    def delete_employee_employment(db: Session, employee_employment_id: int) -> Dict[str, Any]:
        """Delete employee employment record"""
        try:
            db_employment = db.query(EmployeeEmployment).filter(
                EmployeeEmployment.EmployeeEmploymentId == employee_employment_id
            ).first()
            
            if not db_employment:
                return {
                    "success": False, 
                    "message": "Employee employment record not found"
                }
            
            db.delete(db_employment)
            db.commit()
            
            return {
                "success": True, 
                "message": "Employee employment record deleted successfully"
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting employee employment {employee_employment_id}: {str(e)}")
            return {
                "success": False, 
                "message": f"Error deleting employee employment record: {str(e)}"
            }
    
    @staticmethod
    def get_employee_employment_summary(db: Session, employee_id: int) -> Dict[str, Any]:
        """Get employment summary for an employee"""
        try:
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
                if emp.CompanyName:
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
        except Exception as e:
            logger.error(f"Error getting employment summary for employee {employee_id}: {str(e)}")
            return {
                "total_records": 0,
                "latest_employment": None,
                "total_experience_months": 0,
                "total_experience_years": 0,
                "employments_by_company": {},
                "all_employments": []
            }