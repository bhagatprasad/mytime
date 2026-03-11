from sqlalchemy.orm import Session
from sqlalchemy import func,or_, asc, desc
from typing import Optional, List, Tuple, Dict, Any

from app.models.task_Item import TaskItem
from app.schemas.task_item_schemas import TaskItemCreate, TaskItemUpdate


class TaskItemService:
    """Service for TaskItem operations"""
    
    @staticmethod
    def fetch_task_item(db: Session, taskitem_id: int) -> Optional[TaskItem]:
        """Get TaskItem by ID"""
        return db.query(TaskItem).filter(TaskItem.TaskItemId == taskitem_id).first()
    
    @staticmethod
    def fetch_all_task_items(db: Session) -> List[TaskItem]:
        """Get all TaskItemId"""
        return db.query(TaskItem).order_by(TaskItem.Name).all()
    
    @staticmethod
    def fetch_active_task_items(db: Session) -> List[TaskItem]:
        """Get all active TaskItemId"""
        return db.query(TaskItem).filter(
            TaskItem.IsActive == True
        ).order_by(TaskItem.Name).all()
        
    @staticmethod
    def get_task_item_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "TaskItemId",
        sort_order: str = "desc"
    ) -> Tuple[List[TaskItem], int]:
        """Get paginated taskitem with filtering and sorting"""
        query = db.query(TaskItem)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(TaskItem.Name, '').ilike(search_term),
                    func.coalesce(TaskItem.Code, '').ilike(search_term)
                )
            )
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(TaskItem.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        try:
            sort_column = getattr(TaskItem, sort_by, TaskItem.TaskItemId)
        except AttributeError:
            sort_column = TaskItem.TaskItemId
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def check_task_item_exists(db: Session, name: Optional[str] = None, 
                                code: Optional[str] = None, 
                                exclude_id: Optional[int] = None) -> bool:
        """Check if a taskitem with the same name or code exists"""
        query = db.query(TaskItem)
        
        conditions = []
        if name:
            conditions.append(func.lower(TaskItem.Name) == func.lower(name))
        if code:
            conditions.append(func.lower(TaskItem.Code) == func.lower(code))
        
        if not conditions:
            return False
        
        query = query.filter(or_(*conditions))
        
        if exclude_id:
            query = query.filter(TaskItem.TaskItemId != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def get_task_item_by_code(db: Session, code: str) -> Optional[TaskItem]:
        """Get taskitem by code"""
        return db.query(TaskItem).filter(
            func.lower(TaskItem.Code) == func.lower(code)
        ).first()
    
    @staticmethod
    def insert_or_update_task_item(db: Session, taskitem_data: dict) -> Dict[str, Any]:
        """Insert or update taskitem"""
        taskitem_id = taskitem_data.get('TaskItemId')
        
        if taskitem_id:
            # Update existing taskitem
            db_taskitem = db.query(TaskItem).filter(TaskItem.TaskItemId == taskitem_id).first()
            if not db_taskitem:
                return {"success": False, "message": "taskitem not found", "taskitem": None}
            
            # Check for duplicate name or code
            name = taskitem_data.get('Name')
            code = taskitem_data.get('Code')
            
            if name or code:
                if TaskItemService.check_task_item_exists(db, name, code, taskitem_id):
                    return {
                        "success": False, 
                        "message": "taskitem with same name or code already exists",
                        "taskitem": None
                    }
            
            for key, value in taskitem_data.items():
                if key != 'TaskItemId' and value is not None:
                    setattr(db_taskitem, key, value)
            
            db.commit()
            db.refresh(db_taskitem)
            return {
                "success": True, 
                "message": "taskitem updated successfully",
                "taskitem": db_taskitem
            }
        else:
            # Create new taskitem
            # Check for duplicate name or code
            name = taskitem_data.get('Name')
            code = taskitem_data.get('Code')
            
            if TaskItemService.check_task_item_exists(db, name, code):
                return {
                    "success": False, 
                    "message": "taskitem with same name or code already exists",
                    "taskitem": None
                }
            
             # Remove DesignationId if present in create mode
            taskitem_data.pop('TaskItemId', None)
            db_taskitem = TaskItem(**taskitem_data)
            db.add(db_taskitem)
            db.commit()
            db.refresh(db_taskitem)
            return {
                "success": True, 
                "message": "taskitem created successfully",
                "taskitem": db_taskitem
            }
        
    @staticmethod
    def delete_taskitem(db: Session, taskitem_id: int) -> Dict[str, Any]:
        """Delete taskitem"""
        db_taskitem = db.query(TaskItem).filter(TaskItem.TaskItemId == taskitem_id).first()
        if not db_taskitem:
            return {"success": False, "message": "taskitem not found"}
        
        db.delete(db_taskitem)
        db.commit()
        return {"success": True, "message": "taskitem deleted successfully"}
    
    @staticmethod
    def create_taskitem(db: Session, taskitem: TaskItemCreate) -> TaskItem:
        """Create new taskitem"""
        # Check for duplicate name or code
        if TaskItemService.check_task_item_exists(db, TaskItem.Name, TaskItem.Code):
            raise ValueError("TaskItem with same name or code already exists")
        
        db_taskitem= TaskItem(**TaskItem.model_dump(exclude_none=True))
        db.add(db_taskitem)
        db.commit()
        db.refresh(db_taskitem)
        return db_taskitem
    
    @staticmethod
    def update_taskitem(db: Session, taskitem_id: int, taskitem: TaskItemUpdate) -> Optional[TaskItem]:
        """Update existing TaskItem"""
        db_taskitem = db.query(TaskItem).filter(TaskItem.TaskItemId == taskitem_id).first()
        if db_taskitem:
            # Check for duplicate name or code
            update_data = TaskItem.model_dump(exclude_none=True)
            name = update_data.get('Name')
            code = update_data.get('Code')
            
            if name or code:
                if TaskItemService.check_task_item_exists(db, name, code, taskitem_id):
                    raise ValueError("TaskItem with same name or code already exists")
            
            for key, value in update_data.items():
                setattr(db_taskitem, key, value)
            db.commit()
            db.refresh(db_taskitem)
        return db_taskitem
    
    @staticmethod
    def toggle_active_status(db: Session, taskitem_id: int, is_active: bool) -> Optional[TaskItem]:
        """Toggle the active status of a TaskItem"""
        db_taskitem = db.query(TaskItem).filter(TaskItem.TaskItemId == taskitem_id).first()
        if db_taskitem:
            db_taskitem.IsActive = is_active
            db.commit()
            db.refresh(db_taskitem)
        return db_taskitem
    
    @staticmethod
    def search_task_item(db: Session, search_term: str, limit: int = 10) -> List[TaskItem]:
        """Search TaskItem by name or code"""
        search_pattern = f"%{search_term}%"
        return db.query(TaskItem).filter(
            or_(
                func.coalesce(TaskItem.Name, '').ilike(search_pattern),
                func.coalesce(TaskItem.Code, '').ilike(search_pattern)
            )
        ).order_by(TaskItem.Name).limit(limit).all()
    
    @staticmethod
    def get_taskitem_by_ids(db: Session, taskitem_ids: List[int]) -> List[TaskItem]:
        """Get multiple TaskItem by their IDs"""
        return db.query(TaskItem).filter(TaskItem.TaskItemId.in_(taskitem_ids)).all()