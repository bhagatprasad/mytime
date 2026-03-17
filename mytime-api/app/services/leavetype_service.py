from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.models.leavetype import LeaveType

class LeaveTypeService:
    """Service for LeaveType operations - matching C# controller functionality"""
    
    @staticmethod
    def get_leave_types(db: Session) -> List[LeaveType]:
        """Get all active leave types - matches fetchAllLeaveTypes in C#"""
        return db.query(LeaveType).filter(LeaveType.IsActive == True).all()
    
    @staticmethod
    def fetch_leavetype(db: Session, leavetype_id: int) -> Optional[LeaveType]:
        """Get leave type by ID - matches fetchLeaveType in C#"""
        return db.query(LeaveType).filter(
            LeaveType.Id == leavetype_id,
            LeaveType.IsActive == True
        ).first()
    
    @staticmethod
    def insert_or_update_leavetype(db: Session, leavetype_data: dict) -> Dict[str, Any]:
        """Insert or update leave type - matches InsertOrUpdateLeaveType in C#"""
        leavetype_id = leavetype_data.get('Id')
        
        if leavetype_id:
            # Update existing leave type
            db_leavetype = db.query(LeaveType).filter(LeaveType.Id == leavetype_id).first()
            if not db_leavetype:
                return {"success": False, "message": "LeaveType not found"}
            
            # Update fields
            for key, value in leavetype_data.items():
                if key not in ['Id', 'CreatedBy', 'CreatedOn'] and value is not None:
                    setattr(db_leavetype, key, value)
            
            db_leavetype.ModifiedOn = datetime.utcnow()
            
            db.commit()
            db.refresh(db_leavetype)
            return {
                "success": True,
                "message": "LeaveType updated successfully",
                "data": db_leavetype
            }
        else:
            # Create new leave type
            leavetype_data.pop('Id', None)
            leavetype_data['CreatedOn'] = datetime.utcnow()
            
            db_leavetype = LeaveType(**leavetype_data)
            db.add(db_leavetype)
            db.commit()
            db.refresh(db_leavetype)
            return {
                "success": True,
                "message": "LeaveType created successfully",
                "data": db_leavetype
            }
    
    @staticmethod
    def delete_leavetype(db: Session, leavetype_id: int) -> Dict[str, Any]:
        """Delete leave type (soft delete) - matches DeleteLeaveType in C#"""
        db_leavetype = db.query(LeaveType).filter(LeaveType.Id == leavetype_id).first()
        
        if not db_leavetype:
            return {"success": False, "message": "LeaveType not found"}
        
        # Soft delete - set IsActive to False
        db_leavetype.IsActive = False
        db_leavetype.ModifiedOn = datetime.utcnow()
        
        db.commit()
        return {"success": True, "message": "LeaveType deleted successfully"}
    
    @staticmethod
    def check_leavetype_exists(db: Session, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if leave type with given name exists"""
        query = db.query(LeaveType).filter(
            LeaveType.Name == name,
            LeaveType.IsActive == True
        )
        
        if exclude_id:
            query = query.filter(LeaveType.Id != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def get_leavetype_by_name(db: Session, name: str) -> Optional[LeaveType]:
        """Get leave type by name"""
        return db.query(LeaveType).filter(
            LeaveType.Name == name,
            LeaveType.IsActive == True
        ).first()