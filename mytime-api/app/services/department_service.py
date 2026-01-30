from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any

from app.models.department import Department
from app.schemas.department_schemas import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    """Service for Department operations"""
    
    @staticmethod
    def fetch_department(db: Session, department_id: int) -> Optional[Department]:
        """Get department by ID"""
        return db.query(Department).filter(Department.DepartmentId == department_id).first()
    
    @staticmethod
    def fetch_all_departments(db: Session) -> List[Department]:
        """Get all departments"""
        return db.query(Department).order_by(Department.Name).all()
    
    @staticmethod
    def fetch_active_departments(db: Session) -> List[Department]:
        """Get all active departments"""
        return db.query(Department).filter(
            Department.IsActive == True
        ).order_by(Department.Name).all()
    
    @staticmethod
    def get_departments_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "DepartmentId",
        sort_order: str = "desc"
    ) -> Tuple[List[Department], int]:
        """Get paginated departments with filtering and sorting"""
        query = db.query(Department)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(Department.Name, '').ilike(search_term),
                    func.coalesce(Department.Code, '').ilike(search_term),
                    func.coalesce(Department.Description, '').ilike(search_term)
                )
            )
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(Department.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        try:
            sort_column = getattr(Department, sort_by, Department.DepartmentId)
        except AttributeError:
            sort_column = Department.DepartmentId
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def check_department_exists(db: Session, name: Optional[str] = None, 
                               code: Optional[str] = None, 
                               exclude_id: Optional[int] = None) -> bool:
        """Check if a department with the same name or code exists"""
        query = db.query(Department)
        
        conditions = []
        if name:
            conditions.append(func.lower(Department.Name) == func.lower(name))
        if code:
            conditions.append(func.lower(Department.Code) == func.lower(code))
        
        if not conditions:
            return False
        
        query = query.filter(or_(*conditions))
        
        if exclude_id:
            query = query.filter(Department.DepartmentId != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def get_department_by_code(db: Session, code: str) -> Optional[Department]:
        """Get department by code"""
        return db.query(Department).filter(
            func.lower(Department.Code) == func.lower(code)
        ).first()
    
    @staticmethod
    def insert_or_update_department(db: Session, department_data: dict) -> Dict[str, Any]:
        """Insert or update department"""
        department_id = department_data.get('DepartmentId')
        
        if department_id:
            # Update existing department
            db_department = db.query(Department).filter(Department.DepartmentId == department_id).first()
            if not db_department:
                return {"success": False, "message": "Department not found", "department": None}
            
            # Check for duplicate name or code
            name = department_data.get('Name')
            code = department_data.get('Code')
            
            if name or code:
                if DepartmentService.check_department_exists(db, name, code, department_id):
                    return {
                        "success": False, 
                        "message": "Department with same name or code already exists",
                        "department": None
                    }
            
            for key, value in department_data.items():
                if key != 'DepartmentId' and value is not None:
                    setattr(db_department, key, value)
            
            db.commit()
            db.refresh(db_department)
            return {
                "success": True, 
                "message": "Department updated successfully",
                "department": db_department
            }
        else:
            # Create new department
            # Check for duplicate name or code
            name = department_data.get('Name')
            code = department_data.get('Code')
            
            if DepartmentService.check_department_exists(db, name, code):
                return {
                    "success": False, 
                    "message": "Department with same name or code already exists",
                    "department": None
                }
            
            # Remove DepartmentId if present in create mode
            department_data.pop('DepartmentId', None)
            db_department = Department(**department_data)
            db.add(db_department)
            db.commit()
            db.refresh(db_department)
            return {
                "success": True, 
                "message": "Department created successfully",
                "department": db_department
            }
    
    @staticmethod
    def delete_department(db: Session, department_id: int) -> Dict[str, Any]:
        """Delete department"""
        db_department = db.query(Department).filter(Department.DepartmentId == department_id).first()
        if not db_department:
            return {"success": False, "message": "Department not found"}
        
        db.delete(db_department)
        db.commit()
        return {"success": True, "message": "Department deleted successfully"}
    
    @staticmethod
    def create_department(db: Session, department: DepartmentCreate) -> Department:
        """Create new department"""
        # Check for duplicate name or code
        if DepartmentService.check_department_exists(db, department.Name, department.Code):
            raise ValueError("Department with same name or code already exists")
        
        db_department = Department(**department.model_dump(exclude_none=True))
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    
    @staticmethod
    def update_department(db: Session, department_id: int, department: DepartmentUpdate) -> Optional[Department]:
        """Update existing department"""
        db_department = db.query(Department).filter(Department.DepartmentId == department_id).first()
        if db_department:
            # Check for duplicate name or code
            update_data = department.model_dump(exclude_none=True)
            name = update_data.get('Name')
            code = update_data.get('Code')
            
            if name or code:
                if DepartmentService.check_department_exists(db, name, code, department_id):
                    raise ValueError("Department with same name or code already exists")
            
            for key, value in update_data.items():
                setattr(db_department, key, value)
            db.commit()
            db.refresh(db_department)
        return db_department
    
    @staticmethod
    def toggle_active_status(db: Session, department_id: int, is_active: bool) -> Optional[Department]:
        """Toggle the active status of a department"""
        db_department = db.query(Department).filter(Department.DepartmentId == department_id).first()
        if db_department:
            db_department.IsActive = is_active
            db.commit()
            db.refresh(db_department)
        return db_department
    
    @staticmethod
    def search_departments(db: Session, search_term: str, limit: int = 10) -> List[Department]:
        """Search departments by name, code, or description"""
        search_pattern = f"%{search_term}%"
        return db.query(Department).filter(
            or_(
                func.coalesce(Department.Name, '').ilike(search_pattern),
                func.coalesce(Department.Code, '').ilike(search_pattern),
                func.coalesce(Department.Description, '').ilike(search_pattern)
            )
        ).order_by(Department.Name).limit(limit).all()
    
    @staticmethod
    def get_departments_by_ids(db: Session, department_ids: List[int]) -> List[Department]:
        """Get multiple departments by their IDs"""
        return db.query(Department).filter(Department.DepartmentId.in_(department_ids)).all()