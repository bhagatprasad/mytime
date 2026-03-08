from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any

from app.models.role import Role
from app.schemas.role_schemas import RoleCreate, RoleUpdate

class RoleService:
    """Service for Role operations - matching C# controller functionality"""
    
    @staticmethod
    def fetch_role(db: Session, role_id: int) -> Optional[Role]:
        """Get role by ID - matches fetchRole in C#"""
        return db.query(Role).filter(Role.Id == role_id).first()
    
    @staticmethod
    def fetch_all_roles(db: Session) -> List[Role]:
        """Get all roles - matches fetchAllRoles in C#"""
        return db.query(Role).all()
    
    @staticmethod
    def get_roles_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "Id",
        sort_order: str = "desc"
    ) -> Tuple[List[Role], int]:
        """Get paginated roles with filtering and sorting"""
        query = db.query(Role)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(Role.Name, '').ilike(search_term),
                    func.coalesce(Role.Code, '').ilike(search_term)
                )
            )
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(Role.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(Role, sort_by, Role.Id)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def insert_or_update_role(db: Session, role_data: dict) -> Dict[str, Any]:
        """Insert or update role - matches InsertOrUpdateRole in C#"""
        role_id = role_data.get('Id')
        
        if role_id:
            # Update existing role
            db_role = db.query(Role).filter(Role.Id == role_id).first()
            if not db_role:
                return {"success": False, "message": "Role not found", "role": None}
            
            for key, value in role_data.items():
                if key != 'Id' and value is not None:
                    setattr(db_role, key, value)
            
            db.commit()
            db.refresh(db_role)
            return {
                "success": True, 
                "message": "Role updated successfully",
                "role": db_role
            }
        else:
            # Create new role
            # Remove Id if present in create mode
            role_data.pop('Id', None)
            db_role = Role(**role_data)
            db.add(db_role)
            db.commit()
            db.refresh(db_role)
            return {
                "success": True, 
                "message": "Role created successfully",
                "role": db_role
            }
    
    @staticmethod
    def delete_role(db: Session, role_id: int) -> Dict[str, Any]:
        """Delete role - matches DeleteRole in C#"""
        db_role = db.query(Role).filter(Role.Id == role_id).first()
        if not db_role:
            return {"success": False, "message": "Role not found"}
        
        db.delete(db_role)
        db.commit()
        return {"success": True, "message": "Role deleted successfully"}
    
    @staticmethod
    def create_role(db: Session, role: RoleCreate) -> Role:
        """Create new role"""
        db_role = Role(**role.model_dump(exclude_none=True))
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role
    
    @staticmethod
    def update_role(db: Session, role_id: int, role: RoleUpdate) -> Optional[Role]:
        """Update existing role"""
        db_role = db.query(Role).filter(Role.Id == role_id).first()
        if db_role:
            for key, value in role.model_dump(exclude_none=True).items():
                setattr(db_role, key, value)
            db.commit()
            db.refresh(db_role)
        return db_role