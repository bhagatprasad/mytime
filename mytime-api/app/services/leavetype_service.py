from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any

from app.models.leavetype import LeaveType
from app.schemas.leavetype_schemas import LeaveTypeCreate, LeaveTypeUpdate

class LeaveTypeService:
    """Service for LeaveType operations - matching C# controller functionality"""
    
    @staticmethod
    def fetch_leavetype(db: Session, leavetype_id: int) -> Optional[LeaveType]:
        """Get leavetype by ID - matches fetchLeaveType in C#"""
        return db.query(LeaveType).filter(LeaveType.Id == leavetype_id).first()
    
    @staticmethod
    def fetch_all_leavetypes(db: Session) -> List[LeaveType]:
        """Get all leavetypes - matches fetchAllLeaveTypes in C#"""
        return db.query(LeaveType).all()
    
    @staticmethod
    def get_leavetypes_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "Id",
        sort_order: str = "desc"
    ) -> Tuple[List[LeaveType], int]:
        """Get paginated leavetypes with filtering and sorting"""
        query = db.query(LeaveType)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(LeaveType.Name, '').ilike(search_term),
                    func.coalesce(LeaveType.MaxDaysPerYear, '').ilike(search_term),
                    func.coalesce(LeaveType.Description, '').ilike(search_term),
                )
            )
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(LeaveType.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(LeaveType, sort_by, LeaveType.Id)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def insert_or_update_leavetype(db: Session, leavetype_data: dict) -> Dict[str, Any]:
        """Insert or update leavetype - matches InsertOrUpdateLeaveType in C#"""
        LeaveType_id = leavetype_data.get('Id')
        
        if LeaveType_id:
            # Update existing leavetype
            db_leavetype = db.query(LeaveType).filter(LeaveType.Id == LeaveType_id).first()
            if not db_leavetype:
                return {"success": False, "message": "LeaveType not found", "leavetype": None}
            
            for key, value in leavetype_data.items():
                if key != 'Id' and value is not None:
                    setattr(db_leavetype, key, value)
            
            db.commit()
            db.refresh(db_leavetype)
            return {
                "success": True, 
                "message": "LeaveType updated successfully",
                "leavetype": db_leavetype
            }
        else:
            # Create new leavetype
            # Remove Id if present in create mode
            leavetype_data.pop('Id', None)
            db_leavetype = LeaveType(**leavetype_data)
            db.add(db_leavetype)
            db.commit()
            db.refresh(db_leavetype)
            return {
                "success": True, 
                "message": "LeaveType created successfully",
                "leavetype": db_leavetype
            }
    
    @staticmethod
    def delete_leavetype(db: Session, leavetype_id: int) -> Dict[str, Any]:
        """Delete leavetype - matches DeleteLeaveType in C#"""
        db_leaveype = db.query(LeaveType).filter(LeaveType.Id == leavetype_id).first()
        if not db_leaveype:
            return {"success": False, "message": "LeaveType not found"}
        
        db.delete(db_leaveype)
        db.commit()
        return {"success": True, "message": "LeaveType deleted successfully"}
    
    @staticmethod
    def create_leavetype(db: Session, leavetype: LeaveTypeCreate) -> LeaveType:
        """Create new leavetype"""
        db_leavetype = LeaveType(**leavetype.model_dump(exclude_none=True))
        db.add(db_leavetype)
        db.commit()
        db.refresh(db_leavetype)
        return db_leavetype
    
    @staticmethod
    def update_leavetype(db: Session, leavetype_id: int, leavetype: LeaveTypeUpdate) -> Optional[LeaveType]:
        """Update existing leavetype"""
        db_leavetype = db.query(LeaveType).filter(LeaveType.Id == leavetype_id).first()
        if db_leavetype:
            for key, value in leavetype.model_dump(exclude_none=True).items():
                setattr(db_leavetype, key, value)
            db.commit()
            db.refresh(db_leavetype)
        return db_leavetype