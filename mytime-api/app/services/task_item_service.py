from sqlalchemy.orm import Session
from sqlalchemy import func, or_, asc, desc
from typing import Optional, List, Tuple, Dict, Any

from app.models.task_Item import TaskItem
from app.schemas.task_item_schemas import TaskItemCreate, TaskItemUpdate

class TaskItemService:
    @staticmethod
    def fetch_task_item(db: Session, taskitem_id: int) -> Optional[TaskItem]:
        return db.query(TaskItem).filter(TaskItem.TaskItemId == taskitem_id).first()
    
    @staticmethod
    def fetch_all_task_items(db: Session) -> List[TaskItem]:
        return db.query(TaskItem).order_by(TaskItem.Name).all()
    
    @staticmethod
    def fetch_active_task_items(db: Session) -> List[TaskItem]:
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
        query = db.query(TaskItem)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    func.coalesce(TaskItem.Name, '').ilike(search_term),
                    func.coalesce(TaskItem.Code, '').ilike(search_term)
                )
            )
        
        if is_active is not None:
            query = query.filter(TaskItem.IsActive == is_active)
        
        total = query.count()
        
        sort_column = getattr(TaskItem, sort_by, TaskItem.TaskItemId)
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def check_task_item_exists(db: Session, name: Optional[str] = None, 
                               code: Optional[str] = None, 
                               exclude_id: Optional[int] = None) -> bool:
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
    def insert_or_update_task_item(db: Session, taskitem_data: dict) -> Dict[str, Any]:
        taskitem_id = taskitem_data.get('TaskItemId')
        
        if taskitem_id:
            db_taskitem = db.query(TaskItem).filter(TaskItem.TaskItemId == taskitem_id).first()
            if not db_taskitem:
                return {"success": False, "message": "TaskItem not found", "taskitem": None}
            
            for key, value in taskitem_data.items():
                if key != 'TaskItemId' and value is not None:
                    setattr(db_taskitem, key, value)
            
            db.commit()
            db.refresh(db_taskitem)
            return {
                "success": True, 
                "message": "TaskItem updated successfully",
                "taskitem": db_taskitem
            }
        else:
            taskitem_data.pop('TaskItemId', None)
            db_taskitem = TaskItem(**taskitem_data)
            db.add(db_taskitem)
            db.commit()
            db.refresh(db_taskitem)
            return {
                "success": True, 
                "message": "TaskItem created successfully",
                "taskitem": db_taskitem
            }
        
    @staticmethod
    def delete_taskitem(db: Session, taskitem_id: int) -> Dict[str, Any]:
        db_taskitem = db.query(TaskItem).filter(TaskItem.TaskItemId == taskitem_id).first()
        if not db_taskitem:
            return {"success": False, "message": "TaskItem not found"}
        
        db.delete(db_taskitem)
        db.commit()
        return {"success": True, "message": "TaskItem deleted successfully"}