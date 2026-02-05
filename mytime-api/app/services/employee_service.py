from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime
from decimal import Decimal

from app.models.employee import Employee
from app.schemas.employee_schemas import EmployeeCreate, EmployeeUpdate

class EmployeeService:
    """Service for Employee operations"""
    
    @staticmethod
    def fetch_employee(db: Session, employee_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        return db.query(Employee).filter(Employee.EmployeeId == employee_id).first()
    
    @staticmethod
    def fetch_employee_by_code(db: Session, employee_code: str) -> Optional[Employee]:
        """Get employee by EmployeeCode"""
        return db.query(Employee).filter(Employee.EmployeeCode == employee_code).first()
    
    @staticmethod
    def fetch_employee_by_email(db: Session, email: str) -> Optional[Employee]:
        """Get employee by Email"""
        return db.query(Employee).filter(func.lower(Employee.Email) == func.lower(email)).first()
    
    @staticmethod
    def fetch_employee_by_user_id(db: Session, user_id: int) -> Optional[Employee]:
        """Get employee by UserId"""
        return db.query(Employee).filter(Employee.UserId == user_id).first()
    
    @staticmethod
    def fetch_all_employees(db: Session) -> List[Employee]:
        """Get all employees"""
        return db.query(Employee).all()
    
    @staticmethod
    def get_employees_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        department_id: Optional[int] = None,
        designation_id: Optional[int] = None,
        role_id: Optional[int] = None,
        gender: Optional[str] = None,
        start_date_from: Optional[datetime] = None,
        start_date_to: Optional[datetime] = None,
        sort_by: str = "EmployeeId",
        sort_order: str = "desc"
    ) -> Tuple[List[Employee], int]:
        """Get paginated employees with filtering and sorting"""
        query = db.query(Employee)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(Employee.FirstName, '').ilike(search_term),
                    func.coalesce(Employee.LastName, '').ilike(search_term),
                    func.coalesce(Employee.EmployeeCode, '').ilike(search_term),
                    func.coalesce(Employee.Email, '').ilike(search_term),
                    func.coalesce(Employee.Phone, '').ilike(search_term)
                )
            )
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(Employee.IsActive == is_active)
        
        # Apply department filter
        if department_id:
            query = query.filter(Employee.DepartmentId == department_id)
        
        # Apply designation filter
        if designation_id:
            query = query.filter(Employee.DesignationId == designation_id)
        
        # Apply role filter
        if role_id:
            query = query.filter(Employee.RoleId == role_id)
        
        # Apply gender filter
        if gender:
            query = query.filter(func.lower(Employee.Gender) == func.lower(gender))
        
        # Apply date range filters
        if start_date_from:
            query = query.filter(Employee.StartedOn >= start_date_from)
        if start_date_to:
            query = query.filter(Employee.StartedOn <= start_date_to)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(Employee, sort_by, Employee.EmployeeId)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def insert_or_update_employee(db: Session, employee_data: dict) -> Dict[str, Any]:
        """Insert or update employee"""
        try:
            employee_id = employee_data.get('EmployeeId')
            
            # Fix the typo in OfferReleasedOn
            if 'OfferRelesedOn' in employee_data:
                employee_data['OfferRelesedOn'] = employee_data.pop('OfferRelesedOn')
            
            # Ensure date fields are proper datetime objects
            date_fields = [
                'DateOfBirth', 'StartedOn', 'EndedOn', 'ResignedOn',
                'LastWorkingDay', 'OfferRelesedOn', 'OfferAcceptedOn',
                'CreatedOn', 'ModifiedOn'
            ]
            
            for field in date_fields:
                if field in employee_data and employee_data[field] is not None:
                    if isinstance(employee_data[field], str):
                        try:
                            employee_data[field] = datetime.fromisoformat(
                                employee_data[field].replace('Z', '+00:00')
                            )
                        except (ValueError, AttributeError):
                            # If parsing fails, set to None
                            employee_data[field] = None
                            print(f"WARNING: Failed to parse date field: {field}")
            
            # Ensure numeric fields are proper types
            if 'CreatedBy' in employee_data and isinstance(employee_data['CreatedBy'], str):
                try:
                    employee_data['CreatedBy'] = int(employee_data['CreatedBy'])
                except (ValueError, TypeError):
                    employee_data['CreatedBy'] = None
            
            if 'ModifiedBy' in employee_data and isinstance(employee_data['ModifiedBy'], str):
                try:
                    employee_data['ModifiedBy'] = int(employee_data['ModifiedBy'])
                except (ValueError, TypeError):
                    employee_data['ModifiedBy'] = None
            
            if employee_id:
                # Update existing employee
                db_employee = db.query(Employee).filter(Employee.EmployeeId == employee_id).first()
                if not db_employee:
                    return {"success": False, "message": "Employee not found", "employee": None}
                
                # Update only non-null values
                for key, value in employee_data.items():
                    if key != 'EmployeeId' and value is not None:
                        setattr(db_employee, key, value)
                
                # Set ModifiedOn timestamp
                db_employee.ModifiedOn = datetime.utcnow()
                
                db.commit()
                db.refresh(db_employee)
                return {
                    "success": True, 
                    "message": "Employee updated successfully",
                    "employee": db_employee
                }
            else:
                # Create new employee
                # Remove EmployeeId if present in create mode
                employee_data.pop('EmployeeId', None)
                
                # Set CreatedOn timestamp if not provided
                if 'CreatedOn' not in employee_data:
                    employee_data['CreatedOn'] = datetime.utcnow()
                
                db_employee = Employee(**employee_data)
                db.add(db_employee)
                db.commit()
                db.refresh(db_employee)
                return {
                    "success": True, 
                    "message": "Employee created successfully",
                    "employee": db_employee
                }
                
        except Exception as e:
            print(f"ERROR in insert_or_update_employee: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "message": f"Error saving employee: {str(e)}", "employee": None}
    
    @staticmethod
    def delete_employee(db: Session, employee_id: int) -> Dict[str, Any]:
        """Delete employee"""
        db_employee = db.query(Employee).filter(Employee.EmployeeId == employee_id).first()
        if not db_employee:
            return {"success": False, "message": "Employee not found"}
        
        db.delete(db_employee)
        db.commit()
        return {"success": True, "message": "Employee deleted successfully"}
    
    @staticmethod
    def soft_delete_employee(db: Session, employee_id: int, modified_by: int) -> Dict[str, Any]:
        """Soft delete employee (set IsActive = False)"""
        db_employee = db.query(Employee).filter(Employee.EmployeeId == employee_id).first()
        if not db_employee:
            return {"success": False, "message": "Employee not found"}
        
        db_employee.IsActive = False
        db_employee.ModifiedBy = modified_by
        db_employee.ModifiedOn = datetime.utcnow()
        
        db.commit()
        db.refresh(db_employee)
        return {
            "success": True, 
            "message": "Employee deactivated successfully",
            "employee": db_employee
        }
    
    @staticmethod
    def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
        """Create new employee using Pydantic schema"""
        employee_data = employee.model_dump(exclude_none=True)
        
        # Set CreatedOn timestamp if not provided
        if 'CreatedOn' not in employee_data:
            employee_data['CreatedOn'] = datetime.utcnow()
        
        db_employee = Employee(**employee_data)
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    
    @staticmethod
    def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate) -> Optional[Employee]:
        """Update existing employee using Pydantic schema"""
        db_employee = db.query(Employee).filter(Employee.EmployeeId == employee_id).first()
        if db_employee:
            update_data = employee.model_dump(exclude_none=True)
            
            # Set ModifiedOn timestamp
            update_data['ModifiedOn'] = datetime.utcnow()
            
            for key, value in update_data.items():
                setattr(db_employee, key, value)
            
            db.commit()
            db.refresh(db_employee)
        return db_employee
    
    @staticmethod
    def get_employees_by_department(db: Session, department_id: int) -> List[Employee]:
        """Get all employees in a specific department"""
        return db.query(Employee).filter(
            Employee.DepartmentId == department_id,
            Employee.IsActive == True
        ).all()
    
    @staticmethod
    def get_employees_by_designation(db: Session, designation_id: int) -> List[Employee]:
        """Get all employees with a specific designation"""
        return db.query(Employee).filter(
            Employee.DesignationId == designation_id,
            Employee.IsActive == True
        ).all()
    
    @staticmethod
    def check_employee_exists(db: Session, employee_code: str = None, email: str = None) -> Dict[str, Any]:
        """Check if employee exists by code or email"""
        query = db.query(Employee)
        
        if employee_code:
            query = query.filter(Employee.EmployeeCode == employee_code)
        if email:
            query = query.filter(func.lower(Employee.Email) == func.lower(email))
        
        employee = query.first()
        
        return {
            "exists": employee is not None,
            "employee_id": employee.EmployeeId if employee else None,
            "employee_code": employee.EmployeeCode if employee else None
        }
    
    @staticmethod
    def update_employee_status(
        db: Session, 
        employee_id: int, 
        is_active: bool,
        modified_by: int
    ) -> Optional[Employee]:
        """Update employee active status"""
        db_employee = db.query(Employee).filter(Employee.EmployeeId == employee_id).first()
        if db_employee:
            db_employee.IsActive = is_active
            db_employee.ModifiedBy = modified_by
            db_employee.ModifiedOn = datetime.utcnow()
            db.commit()
            db.refresh(db_employee)
        return db_employee
    
    @staticmethod
    def bulk_update_department(
        db: Session,
        employee_ids: List[int],
        department_id: int,
        modified_by: int
    ) -> int:
        """Bulk update department for multiple employees"""
        result = db.query(Employee).filter(
            Employee.EmployeeId.in_(employee_ids)
        ).update(
            {
                Employee.DepartmentId: department_id,
                Employee.ModifiedBy: modified_by,
                Employee.ModifiedOn: datetime.utcnow()
            },
            synchronize_session=False
        )
        db.commit()
        return result
    
    @staticmethod
    def get_employee_statistics(db: Session) -> Dict[str, Any]:
        """Get employee statistics"""
        total_employees = db.query(func.count(Employee.EmployeeId)).scalar()
        active_employees = db.query(func.count(Employee.EmployeeId)).filter(Employee.IsActive == True).scalar()
        inactive_employees = total_employees - active_employees
        
        # Count by department
        dept_stats = db.query(
            Employee.DepartmentId,
            func.count(Employee.EmployeeId).label('count')
        ).filter(
            Employee.IsActive == True
        ).group_by(
            Employee.DepartmentId
        ).all()
        
        return {
            "total_employees": total_employees,
            "active_employees": active_employees,
            "inactive_employees": inactive_employees,
            "department_statistics": [
                {"department_id": dept_id, "employee_count": count} 
                for dept_id, count in dept_stats
            ]
        }