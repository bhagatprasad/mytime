from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func, extract
from typing import Optional, List, Tuple, Dict, Any
from datetime import date, datetime

from app.models.holiday_callender import HolidayCallender
from app.schemas.holiday_calendar_schemas import HolidayCalendarCreate, HolidayCalendarUpdate


class HolidayCalendarService:
    """Service for HolidayCalendar operations"""
    
    @staticmethod
    def fetch_holiday_calendar(db: Session, holiday_id: int) -> Optional[HolidayCallender]:
        """Get holiday by ID"""
        return db.query(HolidayCallender).filter(HolidayCallender.Id == holiday_id).first()
    
    @staticmethod
    def fetch_all_holiday_calendars(db: Session) -> List[HolidayCallender]:
        """Get all holidays"""
        return db.query(HolidayCallender).order_by(HolidayCallender.HolidayDate).all()
    
    @staticmethod
    def fetch_active_holiday_calendars(db: Session) -> List[HolidayCallender]:
        """Get all active holidays"""
        return db.query(HolidayCallender).filter(
            HolidayCallender.IsActive == True
        ).order_by(HolidayCallender.HolidayDate).all()
    
    @staticmethod
    def insert_or_update_holiday_calendar(db: Session, holiday_data: dict) -> Dict[str, Any]:
        """Insert or update holiday"""
        holiday_id = holiday_data.get('Id')
        
        if holiday_id:
            # Update existing holiday
            db_holiday = db.query(HolidayCallender).filter(HolidayCallender.Id == holiday_id).first()
            if not db_holiday:
                return {"success": False, "message": "Holiday not found", "holiday": None}
            
            for key, value in holiday_data.items():
                if key != 'Id' and value is not None:
                    setattr(db_holiday, key, value)
            
            db.commit()
            db.refresh(db_holiday)
            return {
                "success": True, 
                "message": "Holiday updated successfully",
                "holiday": db_holiday
            }
        else:
           
            holiday_data.pop('Id', None)
            db_holiday = HolidayCallender(**holiday_data)
            db.add(db_holiday)
            db.commit()
            db.refresh(db_holiday)
            return {
                "success": True, 
                "message": "Holiday created successfully",
                "holiday": db_holiday
            }
    
    @staticmethod
    def delete_holiday_calendar(db: Session, holiday_id: int) -> Dict[str, Any]:
        """Delete holiday"""
        db_holiday = db.query(HolidayCallender).filter(HolidayCallender.Id == holiday_id).first()
        if not db_holiday:
            return {"success": False, "message": "Holiday not found"}
        
        db.delete(db_holiday)
        db.commit()
        return {"success": True, "message": "Holiday deleted successfully"}