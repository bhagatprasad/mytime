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
    def get_holiday_calendars_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "HolidayDate",
        sort_order: str = "asc"
    ) -> Tuple[List[HolidayCallender], int]:
        """Get paginated holidays with filtering and sorting"""
        query = db.query(HolidayCallender)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                func.coalesce(HolidayCallender.FestivalName, '').ilike(search_term)
            )
        
        # Apply year filter
        if year is not None:
            query = query.filter(HolidayCallender.Year == year)
        
        # Apply month filter
        if month is not None:
            query = query.filter(extract('month', HolidayCallender.HolidayDate) == month)
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(HolidayCallender.IsActive == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        try:
            sort_column = getattr(HolidayCallender, sort_by, HolidayCallender.HolidayDate)
        except AttributeError:
            sort_column = HolidayCallender.HolidayDate
        
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def check_holiday_calendar_exists(db: Session, festival_name: Optional[str] = None, 
                                     holiday_date: Optional[date] = None,
                                     year: Optional[int] = None,
                                     exclude_id: Optional[int] = None) -> bool:
        """Check if a holiday with the same name or date exists"""
        query = db.query(HolidayCallender)
        
        conditions = []
        if festival_name:
            conditions.append(func.lower(HolidayCallender.FestivalName) == func.lower(festival_name))
        
        if holiday_date:
            # Convert holiday_date to datetime for comparison
            holiday_datetime = datetime.combine(holiday_date, datetime.min.time())
            conditions.append(func.date(HolidayCallender.HolidayDate) == holiday_datetime.date())
        
        if year:
            conditions.append(HolidayCallender.Year == year)
        
        if not conditions:
            return False
        
        query = query.filter(or_(*conditions))
        
        if exclude_id:
            query = query.filter(HolidayCallender.Id != exclude_id)
        
        return query.first() is not None
    
    @staticmethod
    def get_holidays_by_year(db: Session, year: int) -> List[HolidayCallender]:
        """Get all holidays for a specific year"""
        return db.query(HolidayCallender).filter(
            HolidayCallender.Year == year,
            HolidayCallender.IsActive == True
        ).order_by(HolidayCallender.HolidayDate).all()
    
    @staticmethod
    def get_holidays_by_date_range(db: Session, start_date: date, end_date: date) -> List[HolidayCallender]:
        """Get holidays within a date range"""
        return db.query(HolidayCallender).filter(
            HolidayCallender.HolidayDate.between(start_date, end_date),
            HolidayCallender.IsActive == True
        ).order_by(HolidayCallender.HolidayDate).all()
    
    @staticmethod
    def get_holidays_by_month(db: Session, year: int, month: int) -> List[HolidayCallender]:
        """Get holidays for a specific month and year"""
        return db.query(HolidayCallender).filter(
            extract('year', HolidayCallender.HolidayDate) == year,
            extract('month', HolidayCallender.HolidayDate) == month,
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
            
            # Check for duplicate holiday
            festival_name = holiday_data.get('FestivalName')
            holiday_date = holiday_data.get('HolidayDate')
            year = holiday_data.get('Year')
            
            if festival_name or holiday_date or year:
                if HolidayCalendarService.check_holiday_calendar_exists(
                    db, festival_name, holiday_date, year, holiday_id
                ):
                    return {
                        "success": False, 
                        "message": "Holiday with same name or date already exists",
                        "holiday": None
                    }
            
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
            # Create new holiday
            # Check for duplicate holiday
            festival_name = holiday_data.get('FestivalName')
            holiday_date = holiday_data.get('HolidayDate')
            year = holiday_data.get('Year')
            
            if HolidayCalendarService.check_holiday_calendar_exists(db, festival_name, holiday_date, year):
                return {
                    "success": False, 
                    "message": "Holiday with same name or date already exists",
                    "holiday": None
                }
            
            # Remove Id if present in create mode
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
    
    @staticmethod
    def create_holiday_calendar(db: Session, holiday: HolidayCalendarCreate) -> HolidayCallender:
        """Create new holiday"""
        # Check for duplicate holiday
        if HolidayCalendarService.check_holiday_calendar_exists(
            db, holiday.FestivalName, holiday.HolidayDate, holiday.Year
        ):
            raise ValueError("Holiday with same name or date already exists")
        
        db_holiday = HolidayCallender(**holiday.model_dump(exclude_none=True))
        db.add(db_holiday)
        db.commit()
        db.refresh(db_holiday)
        return db_holiday
    
    @staticmethod
    def update_holiday_calendar(db: Session, holiday_id: int, holiday: HolidayCalendarUpdate) -> Optional[HolidayCallender]:
        """Update existing holiday"""
        db_holiday = db.query(HolidayCallender).filter(HolidayCallender.Id == holiday_id).first()
        if db_holiday:
            # Check for duplicate holiday
            update_data = holiday.model_dump(exclude_none=True)
            festival_name = update_data.get('FestivalName')
            holiday_date = update_data.get('HolidayDate')
            year = update_data.get('Year')
            
            if festival_name or holiday_date or year:
                if HolidayCalendarService.check_holiday_calendar_exists(
                    db, festival_name, holiday_date, year, holiday_id
                ):
                    raise ValueError("Holiday with same name or date already exists")
            
            for key, value in update_data.items():
                setattr(db_holiday, key, value)
            db.commit()
            db.refresh(db_holiday)
        return db_holiday
    
    @staticmethod
    def toggle_active_status(db: Session, holiday_id: int, is_active: bool) -> Optional[HolidayCallender]:
        """Toggle the active status of a holiday"""
        db_holiday = db.query(HolidayCallender).filter(HolidayCallender.Id == holiday_id).first()
        if db_holiday:
            db_holiday.IsActive = is_active
            db.commit()
            db.refresh(db_holiday)
        return db_holiday
    
    @staticmethod
    def search_holiday_calendars(db: Session, search_term: str, limit: int = 10) -> List[HolidayCallender]:
        """Search holidays by festival name"""
        search_pattern = f"%{search_term}%"
        return db.query(HolidayCallender).filter(
            func.coalesce(HolidayCallender.FestivalName, '').ilike(search_pattern)
        ).order_by(HolidayCallender.HolidayDate).limit(limit).all()
    
    @staticmethod
    def get_upcoming_holidays(db: Session, days: int = 30) -> List[HolidayCallender]:
        """Get upcoming holidays within the next N days"""
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        future_date = today + timedelta(days=days)
        
        return db.query(HolidayCallender).filter(
            HolidayCallender.HolidayDate >= today,
            HolidayCallender.HolidayDate <= future_date,
            HolidayCallender.IsActive == True
        ).order_by(HolidayCallender.HolidayDate).all()
    
    @staticmethod
    def is_holiday(db: Session, check_date: date) -> bool:
        """Check if a specific date is a holiday"""
        return db.query(HolidayCallender).filter(
            func.date(HolidayCallender.HolidayDate) == check_date,
            HolidayCallender.IsActive == True
        ).first() is not None
    
    @staticmethod
    def get_holiday_calendars_by_ids(db: Session, holiday_ids: List[int]) -> List[HolidayCallender]:
        """Get multiple holidays by their IDs"""
        return db.query(HolidayCallender).filter(HolidayCallender.Id.in_(holiday_ids)).all()