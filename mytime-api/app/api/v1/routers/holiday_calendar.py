from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date, datetime

from app.schemas.holiday_calendar_schemas import (
    HolidayCalendarCreate, HolidayCalendarUpdate, HolidayCalendarResponse, 
    HolidayCalendarListResponse, HolidayCalendarExistsResponse, 
    HolidayCalendarDeleteResponse, HolidayByYearResponse
)
from app.core.database import get_db
from app.services.holiday_calendar_service import HolidayCalendarService

router = APIRouter()


@router.get("/fetchHolidayCalendar/{holiday_id}", response_model=HolidayCalendarResponse)
async def fetch_holiday_calendar(holiday_id: int, db: Session = Depends(get_db)):
    """Get holiday by ID"""
    try:
        holiday = HolidayCalendarService.fetch_holiday_calendar(db, holiday_id)
        if not holiday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Holiday with ID {holiday_id} not found"
            )
        return holiday
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching holiday: {str(e)}"
        )


@router.get("/fetchAllHolidayCalendars", response_model=List[HolidayCalendarResponse])
async def fetch_all_holiday_calendars(db: Session = Depends(get_db)):
    """Get all holidays"""
    try:
        holidays = HolidayCalendarService.fetch_all_holiday_calendars(db)
        return holidays
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching holidays: {str(e)}"
        )


@router.get("/fetchActiveHolidayCalendars", response_model=List[HolidayCalendarResponse])
async def fetch_active_holiday_calendars(db: Session = Depends(get_db)):
    """Get all active holidays"""
    try:
        holidays = HolidayCalendarService.fetch_active_holiday_calendars(db)
        return holidays
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active holidays: {str(e)}"
        )


@router.get("/getHolidayCalendars", response_model=HolidayCalendarListResponse)
async def get_holiday_calendars(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    year: Optional[int] = Query(None, ge=1900, le=2100, description="Filter by year"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Filter by month"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("HolidayDate", description="Sort column"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated holidays with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = HolidayCalendarService.get_holiday_calendars_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            year=year,
            month=month,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pages = (total + size - 1) // size
        
        return {
            "total": total,
            "items": items,
            "page": page,
            "size": size,
            "pages": pages
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching holidays: {str(e)}"
        )


@router.get("/checkHolidayCalendarExists", response_model=HolidayCalendarExistsResponse)
async def check_holiday_calendar_exists(
    festival_name: Optional[str] = Query(None, description="Festival/Holiday name"),
    holiday_date: Optional[date] = Query(None, description="Holiday date"),
    year: Optional[int] = Query(None, description="Year"),
    exclude_id: Optional[int] = Query(None, description="Holiday ID to exclude (for updates)"),
    db: Session = Depends(get_db)
):
    """Check if holiday exists"""
    try:
        exists = HolidayCalendarService.check_holiday_calendar_exists(
            db, festival_name, holiday_date, year, exclude_id
        )
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking holiday existence: {str(e)}"
        )


@router.get("/getHolidaysByYear/{year}", response_model=List[HolidayCalendarResponse])
async def get_holidays_by_year(year: int, db: Session = Depends(get_db)):
    """Get all holidays for a specific year"""
    try:
        holidays = HolidayCalendarService.get_holidays_by_year(db, year)
        return holidays
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching holidays by year: {str(e)}"
        )


@router.get("/getHolidaysByDateRange", response_model=List[HolidayCalendarResponse])
async def get_holidays_by_date_range(
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db)
):
    """Get holidays within a date range"""
    try:
        holidays = HolidayCalendarService.get_holidays_by_date_range(db, start_date, end_date)
        return holidays
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching holidays by date range: {str(e)}"
        )


@router.get("/getHolidaysByMonth", response_model=List[HolidayCalendarResponse])
async def get_holidays_by_month(
    year: int = Query(..., ge=1900, le=2100, description="Year"),
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    db: Session = Depends(get_db)
):
    """Get holidays for a specific month and year"""
    try:
        holidays = HolidayCalendarService.get_holidays_by_month(db, year, month)
        return holidays
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching holidays by month: {str(e)}"
        )


@router.get("/getUpcomingHolidays", response_model=List[HolidayCalendarResponse])
async def get_upcoming_holidays(
    days: int = Query(30, ge=1, le=365, description="Number of days to look ahead"),
    db: Session = Depends(get_db)
):
    """Get upcoming holidays within the next N days"""
    try:
        holidays = HolidayCalendarService.get_upcoming_holidays(db, days)
        return holidays
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching upcoming holidays: {str(e)}"
        )


@router.get("/isHoliday/{check_date}", response_model=dict)
async def is_holiday(check_date: date, db: Session = Depends(get_db)):
    """Check if a specific date is a holiday"""
    try:
        is_holiday = HolidayCalendarService.is_holiday(db, check_date)
        holiday = None
        if is_holiday:
            holiday = db.query(HolidayCalendarService.model).filter(
                func.date(HolidayCalendarService.model.HolidayDate) == check_date,
                HolidayCalendarService.model.IsActive == True
            ).first()
        
        return {
            "is_holiday": is_holiday,
            "holiday": holiday.FestivalName if holiday else None,
            "date": check_date
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking if date is holiday: {str(e)}"
        )


@router.post("/InsertOrUpdateHolidayCalendar")
async def insert_or_update_holiday_calendar(holiday: dict, db: Session = Depends(get_db)):
    """Insert or update holiday"""
    try:
        response = HolidayCalendarService.insert_or_update_holiday_calendar(db, holiday)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving holiday: {str(e)}"
        )


@router.delete("/DeleteHolidayCalendar/{holiday_id}", response_model=HolidayCalendarDeleteResponse)
async def delete_holiday_calendar(holiday_id: int, db: Session = Depends(get_db)):
    """Delete holiday"""
    try:
        response = HolidayCalendarService.delete_holiday_calendar(db, holiday_id)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting holiday: {str(e)}"
        )


@router.post("/create", response_model=HolidayCalendarResponse, status_code=status.HTTP_201_CREATED)
async def create_holiday_calendar(holiday: HolidayCalendarCreate, db: Session = Depends(get_db)):
    """Create a new holiday using Pydantic model"""
    try:
        return HolidayCalendarService.create_holiday_calendar(db, holiday)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating holiday: {str(e)}"
        )


@router.put("/update/{holiday_id}", response_model=HolidayCalendarResponse)
async def update_holiday_calendar(holiday_id: int, holiday: HolidayCalendarUpdate, db: Session = Depends(get_db)):
    """Update an existing holiday using Pydantic model"""
    try:
        updated_holiday = HolidayCalendarService.update_holiday_calendar(db, holiday_id, holiday)
        if not updated_holiday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Holiday with ID {holiday_id} not found"
            )
        return updated_holiday
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating holiday: {str(e)}"
        )


@router.patch("/toggleActiveStatus/{holiday_id}", response_model=HolidayCalendarResponse)
async def toggle_active_status(
    holiday_id: int,
    is_active: bool = Query(..., description="New active status (true/false)"),
    db: Session = Depends(get_db)
):
    """Toggle the active status of a holiday"""
    try:
        holiday = HolidayCalendarService.toggle_active_status(db, holiday_id, is_active)
        if not holiday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Holiday with ID {holiday_id} not found"
            )
        return holiday
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling active status: {str(e)}"
        )


@router.get("/searchHolidayCalendars", response_model=List[HolidayCalendarResponse])
async def search_holiday_calendars(
    q: str = Query(..., min_length=2, description="Search term"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """Search holidays by festival name"""
    try:
        holidays = HolidayCalendarService.search_holiday_calendars(db, q, limit)
        return holidays
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching holidays: {str(e)}"
        )


@router.get("/getHolidayCalendarsByIds", response_model=List[HolidayCalendarResponse])
async def get_holiday_calendars_by_ids(
    ids: str = Query(..., description="Comma-separated holiday IDs"),
    db: Session = Depends(get_db)
):
    """Get multiple holidays by their IDs"""
    try:
        # Convert comma-separated string to list of integers
        holiday_ids = [int(id.strip()) for id in ids.split(",") if id.strip().isdigit()]
        
        if not holiday_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid holiday IDs provided"
            )
        
        holidays = HolidayCalendarService.get_holiday_calendars_by_ids(db, holiday_ids)
        return holidays
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid holiday ID format. Provide comma-separated integers."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching holidays by IDs: {str(e)}"
        )