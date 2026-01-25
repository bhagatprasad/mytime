from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from typing import Optional,List

from app.schemas.country_schemas import (
    CountryCreate, CountryUpdate, CountryResponse, CountryListResponse,
    CountryExistsResponse, CountryDeleteResponse
)
from app.core.database import get_db
from app.services.country_service import CountryService


router = APIRouter()

@router.get("/fetchAllCountries", response_model = List[CountryListResponse])  # Now List is defined
async def fetch_all_countries(db: Session = Depends(get_db)):
    """Get all countries - matches C# fetch_all_countries endpoint"""
    try:
        countries = CountryService.fetch_all_countries(db)
        print("countries " + countries)
        return countries
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )