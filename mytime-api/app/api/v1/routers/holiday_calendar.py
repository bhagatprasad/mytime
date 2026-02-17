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