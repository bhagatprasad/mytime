from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.country_schemas import (
    CountryResponse,
    CountryDeleteResponse
)
from app.core.database import get_db
from app.services.country_service import CountryService

router = APIRouter()

@router.get("/fetchCountry/{country_id}", response_model=CountryResponse)
async def fetch_country(country_id: int, db: Session = Depends(get_db)):
    """Get country by ID"""
    try:
        country = CountryService.fetch_country(db, country_id)
        if not country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Country with ID {country_id} not found"
            )
        return country
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching country: {str(e)}"
        )

@router.get("/fetchAllCountries", response_model=List[CountryResponse])  # FIXED: Changed from CountryListResponse
async def fetch_all_countries(db: Session = Depends(get_db)):
    """Get all countries - matches C# fetch_all_countries endpoint"""
    try:
        countries = CountryService.fetch_all_countries(db)
        return countries
    except Exception as e:
        print(f"Error fetching countries: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching countries: {str(e)}"
        )

@router.post("/InsertOrUpdateCountry")
async def insert_or_update_country(country: dict, db: Session = Depends(get_db)):
    """Insert or update country - matches C# InsertOrUpdateCountry endpoint"""
    try:
        response = CountryService.insert_or_update_country(db, country)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,  # Changed from 404 to 400
                detail=response["message"]
            )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving country: {str(e)}"
        )

@router.delete("/DeleteCountry/{country_id}", response_model=CountryDeleteResponse)
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    """Delete country"""
    try:
        response = CountryService.delete_country(db, country_id)
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
            detail=f"Error deleting country: {str(e)}"
        )