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


@router.get("/fetchCityWithRelations/{city_id}", response_model=CityWithRelationsResponse)
async def fetch_city_with_relations(city_id: int, db: Session = Depends(get_db)):
    """Get city by ID with country and state relations"""
    try:
        city = CityService.fetch_city_with_relations(db, city_id)
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
            detail=f"Error fetching city with relations: {str(e)}"
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


@router.get("/fetchActiveCities", response_model=List[CityResponse])
async def fetch_active_cities(db: Session = Depends(get_db)):
    """Get all active cities"""
    try:
        cities = CityService.fetch_active_cities(db)
        return cities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active cities: {str(e)}"
        )


@router.get("/getCities", response_model=CityListResponse)
async def get_cities(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    country_id: Optional[int] = Query(None, description="Filter by country ID"),
    state_id: Optional[int] = Query(None, description="Filter by state ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("Id", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    with_relations: bool = Query(False, description="Include country/state relations"),
    db: Session = Depends(get_db)
):
    """Get paginated cities with filtering and sorting"""
    try:
        skip = (page - 1) * size
        
        if with_relations:
            items, total = CityService.get_cities_with_relations_pagination(
                db=db,
                skip=skip,
                limit=size,
                search=search,
                country_id=country_id,
                state_id=state_id,
                is_active=is_active
            )
        else:
            items, total = CityService.get_cities_with_pagination(
                db=db,
                skip=skip,
                limit=size,
                search=search,
                country_id=country_id,
                state_id=state_id,
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


@router.get("/checkCityExists", response_model=CityExistsResponse)
async def check_city_exists(
    name: Optional[str] = Query(None, description="City name"),
    code: Optional[str] = Query(None, description="City code"),
    country_id: Optional[int] = Query(None, description="Country ID"),
    state_id: Optional[int] = Query(None, description="State ID"),
    exclude_id: Optional[int] = Query(None, description="City ID to exclude (for updates)"),
    db: Session = Depends(get_db)
):
    """Check if city exists - matches C# checkCityExists endpoint"""
    try:
        exists = CityService.check_city_exists(db, name, code, country_id, state_id, exclude_id)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking city existence: {str(e)}"
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


@router.get("/getCityByCode/{city_code}", response_model=CityResponse)
async def get_city_by_code(
    city_code: str,
    country_id: Optional[int] = Query(None, description="Country ID filter"),
    db: Session = Depends(get_db)
):
    """Get city by city code"""
    try:
        city = CityService.get_city_by_code(db, city_code, country_id)
        if not city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with code '{city_code}' not found"
            )
        return city
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching city by code: {str(e)}"
        )


@router.patch("/toggleActiveStatus/{city_id}", response_model=CityResponse)
async def toggle_active_status(
    city_id: int,
    is_active: bool = Query(..., description="New active status (true/false)"),
    db: Session = Depends(get_db)
):
    """Toggle the active status of a city"""
    try:
        city = CityService.toggle_active_status(db, city_id, is_active)
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
            detail=f"Error toggling active status: {str(e)}"
        )


@router.post("/create", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
async def create_city(city: CityCreate, db: Session = Depends(get_db)):
    """Create a new city using Pydantic model"""
    try:
        return CityService.create_city(db, city)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating city: {str(e)}"
        )


@router.put("/update/{city_id}", response_model=CityResponse)
async def update_city(city_id: int, city: CityUpdate, db: Session = Depends(get_db)):
    """Update an existing city using Pydantic model"""
    try:
        updated_city = CityService.update_city(db, city_id, city)
        if not updated_city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with ID {city_id} not found"
            )
        return updated_city
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
            detail=f"Error updating city: {str(e)}"
        )


@router.get("/searchCities", response_model=List[CityResponse])
async def search_cities(
    q: str = Query(..., min_length=2, description="Search term"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """Search cities by name or code"""
    try:
        cities = CityService.search_cities(db, q, limit)
        return cities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching cities: {str(e)}"
        )