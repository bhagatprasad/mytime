from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional, List, Dict, Any

from app.models.task_code import TaskCode
from app.schemas.taskcode_schemas import TaskcodeCreate, TaskcodeUpdate

class TaskcodeService:
    @staticmethod
    def fetch_taskcode(db: Session, taskcodeid: int) -> Optional[TaskCode]:
        return db.query(TaskCode).filter(TaskCode.TaskCodeId == taskcodeid).first()
    
    @staticmethod
    def fetch_all_taskcodes(db: Session) -> List[TaskCode]:
        return db.query(TaskCode).all()
    
    @staticmethod
    def insert_or_update_taskcode(db: Session, taskcode_data: dict) -> Dict[str, Any]:
        taskcode_id = taskcode_data.get("TaskCodeId")

        if taskcode_id:
            db_taskcode = db.query(TaskCode).filter(TaskCode.TaskCodeId == taskcode_id).first()

            if not db_taskcode:
                return {
                    "success": False,
                    "message": "Taskcode not found",
                    "Taskcode": None
                }

            for key, value in taskcode_data.items():
                if key != "TaskCodeId" and value is not None:
                    setattr(db_taskcode, key, value)

            db.commit()
            db.refresh(db_taskcode)

            return {
                "success": True,
                "message": "Taskcode updated successfully",
                "Taskcode": db_taskcode
            }
        else:
            taskcode_data.pop("TaskCodeId", None)
            db_taskcode = TaskCode(**taskcode_data)
            db.add(db_taskcode)
            db.commit()
            db.refresh(db_taskcode)

            return {
                "success": True,
                "message": "Taskcode created successfully",
                "Taskcode": db_taskcode
            }
    
    @staticmethod
    def delete_taskcode(db: Session, taskcode_id: int) -> Dict[str, Any]:
        db_taskcode = db.query(TaskCode).filter(TaskCode.TaskCodeId == taskcode_id).first()
        if not db_taskcode:
            return {"success": False, "message": "Taskcode not found"}
        
        db.delete(db_taskcode)
        db.commit()
        return {"success": True, "message": "Taskcode deleted successfully"}
    
    @staticmethod
    def check_taskcode_exists(db: Session, name: Optional[str] = None, 
                              code: Optional[str] = None, 
                              exclude_id: Optional[int] = None) -> bool:
        query = db.query(TaskCode)
        
        conditions = []
        if name:
            conditions.append(func.lower(TaskCode.Name) == func.lower(name))
        if code:
            conditions.append(func.lower(TaskCode.Code) == func.lower(code))
        
        if not conditions:
            return False
        
        query = query.filter(or_(*conditions))
        
        if exclude_id:
            query = query.filter(TaskCode.TaskCodeId != exclude_id)
        
        return query.first() is not None