from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any

from app.models.designation import Designation
from app.schemas.designation_schemas import DesignationCreate, DesignationUpdate


class DesignationService:
    """Service for Designation operations"""
    
    @staticmethod
    def fetch_designation(db: Session, designation_id: int) -> Optional[Designation]:
        """Get designation by ID"""
        return db.query(Designation).filter(Designation.DesignationId == designation_id).first()
    
    @staticmethod
    def fetch_all_designations(db: Session) -> List[Designation]:
        """Get all designations"""
        return db.query(Designation).order_by(Designation.Name).all()
    
    @staticmethod
    def fetch_active_designations(db: Session) -> List[Designation]:
        """Get all active designations"""
        return db.query(Designation).filter(
            Designation.IsActive == True
        ).order_by(Designation.Name).all()
    
    @staticmethod
    def get_designations_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "DesignationId",
        sort_order: str = "desc"
    ) -> Tuple[List[Designation], int]:
        """Get paginated designations with filtering and sorting"""
        query = db.query(Designation)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(Designation.Name, '').ilike(search_term),
                    func.coalesce(Designation.Code, '').ilike(search_term)
                )
            )
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(Designation.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        try:
            sort_column = getattr(Designation, sort_by, Designation.DesignationId)
        except AttributeError:
            sort_column = Designation.DesignationId
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def check_designation_exists(db: Session, name: Optional[str] = None, 
                                code: Optional[str] = None, 
                                exclude_id: Optional[int] = None) -> bool:
        """Check if a designation with the same name or code exists"""
        query = db.query(Designation)
        
        conditions = []
        if name:
            conditions.append(func.lower(Designation.Name) == func.lower(name))
        if code:
            conditions.append(func.lower(Designation.Code) == func.lower(code))
        
        if not conditions:
            return False
        
        query = query.filter(or_(*conditions))
        
        if exclude_id:
            query = query.filter(Designation.DesignationId != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def get_designation_by_code(db: Session, code: str) -> Optional[Designation]:
        """Get designation by code"""
        return db.query(Designation).filter(
            func.lower(Designation.Code) == func.lower(code)
        ).first()
    
    @staticmethod
    def insert_or_update_designation(db: Session, designation_data: dict) -> Dict[str, Any]:
        """Insert or update designation"""
        designation_id = designation_data.get('DesignationId')
        
        if designation_id:
            # Update existing designation
            db_designation = db.query(Designation).filter(Designation.DesignationId == designation_id).first()
            if not db_designation:
                return {"success": False, "message": "Designation not found", "designation": None}
            
            # Check for duplicate name or code
            name = designation_data.get('Name')
            code = designation_data.get('Code')
            
            if name or code:
                if DesignationService.check_designation_exists(db, name, code, designation_id):
                    return {
                        "success": False, 
                        "message": "Designation with same name or code already exists",
                        "designation": None
                    }
            
            for key, value in designation_data.items():
                if key != 'DesignationId' and value is not None:
                    setattr(db_designation, key, value)
            
            db.commit()
            db.refresh(db_designation)
            return {
                "success": True, 
                "message": "Designation updated successfully",
                "designation": db_designation
            }
        else:
            # Create new designation
            # Check for duplicate name or code
            name = designation_data.get('Name')
            code = designation_data.get('Code')
            
            if DesignationService.check_designation_exists(db, name, code):
                return {
                    "success": False, 
                    "message": "Designation with same name or code already exists",
                    "designation": None
                }
            
            # Remove DesignationId if present in create mode
            designation_data.pop('DesignationId', None)
            db_designation = Designation(**designation_data)
            db.add(db_designation)
            db.commit()
            db.refresh(db_designation)
            return {
                "success": True, 
                "message": "Designation created successfully",
                "designation": db_designation
            }
    
    @staticmethod
    def delete_designation(db: Session, designation_id: int) -> Dict[str, Any]:
        """Delete designation"""
        db_designation = db.query(Designation).filter(Designation.DesignationId == designation_id).first()
        if not db_designation:
            return {"success": False, "message": "Designation not found"}
        
        db.delete(db_designation)
        db.commit()
        return {"success": True, "message": "Designation deleted successfully"}
    
    @staticmethod
    def create_designation(db: Session, designation: DesignationCreate) -> Designation:
        """Create new designation"""
        # Check for duplicate name or code
        if DesignationService.check_designation_exists(db, designation.Name, designation.Code):
            raise ValueError("Designation with same name or code already exists")
        
        db_designation = Designation(**designation.model_dump(exclude_none=True))
        db.add(db_designation)
        db.commit()
        db.refresh(db_designation)
        return db_designation
    
    @staticmethod
    def update_designation(db: Session, designation_id: int, designation: DesignationUpdate) -> Optional[Designation]:
        """Update existing designation"""
        db_designation = db.query(Designation).filter(Designation.DesignationId == designation_id).first()
        if db_designation:
            # Check for duplicate name or code
            update_data = designation.model_dump(exclude_none=True)
            name = update_data.get('Name')
            code = update_data.get('Code')
            
            if name or code:
                if DesignationService.check_designation_exists(db, name, code, designation_id):
                    raise ValueError("Designation with same name or code already exists")
            
            for key, value in update_data.items():
                setattr(db_designation, key, value)
            db.commit()
            db.refresh(db_designation)
        return db_designation
    
    @staticmethod
    def toggle_active_status(db: Session, designation_id: int, is_active: bool) -> Optional[Designation]:
        """Toggle the active status of a designation"""
        db_designation = db.query(Designation).filter(Designation.DesignationId == designation_id).first()
        if db_designation:
            db_designation.IsActive = is_active
            db.commit()
            db.refresh(db_designation)
        return db_designation
    
    @staticmethod
    def search_designations(db: Session, search_term: str, limit: int = 10) -> List[Designation]:
        """Search designations by name or code"""
        search_pattern = f"%{search_term}%"
        return db.query(Designation).filter(
            or_(
                func.coalesce(Designation.Name, '').ilike(search_pattern),
                func.coalesce(Designation.Code, '').ilike(search_pattern)
            )
        ).order_by(Designation.Name).limit(limit).all()
    
    @staticmethod
    def get_designations_by_ids(db: Session, designation_ids: List[int]) -> List[Designation]:
        """Get multiple designations by their IDs"""
        return db.query(Designation).filter(Designation.DesignationId.in_(designation_ids)).all()