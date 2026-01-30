from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date


class HolidayCalendarBase(BaseModel):
    """Base schema for HolidayCalendar data"""
    FestivalName: Optional[str] = Field(None, max_length=255, description="Festival/Holiday name")
    HolidayDate: Optional[date] = Field(None, description="Holiday date")
    Year: Optional[int] = Field(None, ge=1900, le=2100, description="Year of the holiday")
    IsActive: Optional[bool] = Field(True, description="Whether the holiday is active")


class HolidayCalendarCreate(HolidayCalendarBase):
    """Schema for creating a new HolidayCalendar"""
    CreatedBy: Optional[int] = Field(None, description="User ID who created the record")


class HolidayCalendarUpdate(BaseModel):
    """Schema for updating an existing HolidayCalendar"""
    FestivalName: Optional[str] = Field(None, max_length=255, description="Festival/Holiday name")
    HolidayDate: Optional[date] = Field(None, description="Holiday date")
    Year: Optional[int] = Field(None, ge=1900, le=2100, description="Year of the holiday")
    ModifiedBy: Optional[int] = Field(None, description="User ID who last modified the record")
    IsActive: Optional[bool] = Field(None, description="Whether the holiday is active")


class HolidayCalendarResponse(BaseModel):
    """Schema for HolidayCalendar response (read operations)"""
    Id: int
    FestivalName: Optional[str] = None
    HolidayDate: Optional[date] = None
    Year: Optional[int] = None
    CreatedBy: Optional[int] = None
    CreatedOn: Optional[datetime] = None
    ModifiedBy: Optional[int] = None
    ModifiedOn: Optional[datetime] = None
    IsActive: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class HolidayCalendarListResponse(BaseModel):
    """Schema for listing multiple HolidayCalendars with pagination"""
    total: int
    items: List[HolidayCalendarResponse]
    page: int
    size: int
    pages: int


class HolidayCalendarExistsResponse(BaseModel):
    """Response for HolidayCalendar existence check"""
    exists: bool


class HolidayCalendarDeleteResponse(BaseModel):
    """Response for delete operation"""
    success: bool
    message: str = "Holiday deleted successfully"


class HolidayByYearResponse(BaseModel):
    """Response for holidays grouped by year"""
    year: int
    holidays: List[HolidayCalendarResponse]