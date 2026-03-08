from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.city_schemas import (
    CityCreate, CityUpdate, CityResponse, CityListResponse,
    CityExistsResponse, CityDeleteResponse, CityWithRelationsResponse
)
from app.core.database import get_db
from app.services.city_service import CityService

router = APIRouter()


@router.get("/fetchCity/{city_id}", response_model=CityResponse)
async def fetch_city(city_id: int, db: Session = Depends(get_db)):
    """Get city by ID - matches C# fetchCity endpoint"""
    try:
        city = CityService.fetch_city(db, city_id)
        if not city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with ID {city_id} not found"
            )
        return city
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching city: {str(e)}"
        )

@router.get("/fetchAllCities", response_model=List[CityResponse])
async def fetch_all_cities(db: Session = Depends(get_db)):
    """Get all cities - matches C# fetchAllCities endpoint"""
    try:
        cities = CityService.fetch_all_cities(db)
        return cities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching cities: {str(e)}"
        )

@router.post("/InsertOrUpdateCity")
async def insert_or_update_city(city: dict, db: Session = Depends(get_db)):
    """Insert or update city - matches C# InsertOrUpdateCity endpoint"""
    try:
        response = CityService.insert_or_update_city(db, city)
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
            detail=f"Error saving city: {str(e)}"
        )


@router.delete("/DeleteCity/{city_id}", response_model=CityDeleteResponse)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    """Delete city - matches C# DeleteCity endpoint"""
    try:
        response = CityService.delete_city(db, city_id)
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
            detail=f"Error deleting city: {str(e)}"
        )

@router.get("/getCitiesByCountry/{country_id}", response_model=List[CityResponse])
async def get_cities_by_country(country_id: int, db: Session = Depends(get_db)):
    """Get all cities for a specific country"""
    try:
        cities = CityService.get_cities_by_country(db, country_id)
        return cities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching cities by country: {str(e)}"
        )


@router.get("/getCitiesByState/{state_id}", response_model=List[CityResponse])
async def get_cities_by_state(state_id: int, db: Session = Depends(get_db)):
    """Get all cities for a specific state"""
    try:
        cities = CityService.get_cities_by_state(db, state_id)
        return cities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching cities by state: {str(e)}"
        )


@router.get("/getCitiesByCountryAndState", response_model=List[CityResponse])
async def get_cities_by_country_and_state(
    country_id: int,
    state_id: Optional[int] = Query(None, description="State ID"),
    db: Session = Depends(get_db)
):
    """Get cities by country and optionally state"""
    try:
        cities = CityService.get_cities_by_country_and_state(db, country_id, state_id)
        return cities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching cities by country and state: {str(e)}"
        )