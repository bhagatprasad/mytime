from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.country_schemas import (
    CountryCreate, CountryUpdate, CountryResponse, CountryListResponse,
    CountryExistsResponse, CountryDeleteResponse
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

@router.get("/fetchActiveCountries", response_model=List[CountryResponse])
async def fetch_active_countries(db: Session = Depends(get_db)):
    """Get all active countries"""
    try:
        countries = CountryService.fetch_active_countries(db)
        return countries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching active countries: {str(e)}"
        )

@router.get("/getCountries", response_model=CountryListResponse)
async def get_countries(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("Id", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated countries with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = CountryService.get_countries_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pages = (total + size - 1) // size  # Ceiling division
        
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
            detail=f"Error fetching countries: {str(e)}"
        )

@router.get("/checkCountryExists", response_model=CountryExistsResponse)
async def check_country_exists(
    name: Optional[str] = Query(None, description="Country name"),
    code: Optional[str] = Query(None, description="Country code"),
    exclude_id: Optional[int] = Query(None, description="Country ID to exclude (for updates)"),
    db: Session = Depends(get_db)
):
    """Check if country exists"""
    try:
        exists = CountryService.check_country_exists(db, name, code, exclude_id)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking country existence: {str(e)}"
        )

@router.get("/getCountryByCode/{code}", response_model=CountryResponse)
async def get_country_by_code(code: str, db: Session = Depends(get_db)):
    """Get country by code"""
    try:
        country = CountryService.get_country_by_code(db, code)
        if not country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Country with code '{code}' not found"
            )
        return country
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching country by code: {str(e)}"
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

@router.post("/create", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
async def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    """Create a new country using Pydantic model"""
    try:
        return CountryService.create_country(db, country)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating country: {str(e)}"
        )

@router.put("/update/{country_id}", response_model=CountryResponse)
async def update_country(country_id: int, country: CountryUpdate, db: Session = Depends(get_db)):
    """Update an existing country using Pydantic model"""
    try:
        updated_country = CountryService.update_country(db, country_id, country)
        if not updated_country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Country with ID {country_id} not found"
            )
        return updated_country
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
            detail=f"Error updating country: {str(e)}"
        )

@router.patch("/toggleActiveStatus/{country_id}", response_model=CountryResponse)
async def toggle_active_status(
    country_id: int,
    is_active: bool = Query(..., description="New active status (true/false)"),
    db: Session = Depends(get_db)
):
    """Toggle the active status of a country"""
    try:
        country = CountryService.toggle_active_status(db, country_id, is_active)
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
            detail=f"Error toggling active status: {str(e)}"
        )

@router.get("/searchCountries", response_model=List[CountryResponse])
async def search_countries(
    q: str = Query(..., min_length=2, description="Search term"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """Search countries by name or code"""
    try:
        countries = CountryService.search_countries(db, q, limit)
        return countries
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching countries: {str(e)}"
        )

@router.get("/getCountriesByIds", response_model=List[CountryResponse])
async def get_countries_by_ids(
    ids: str = Query(..., description="Comma-separated country IDs"),
    db: Session = Depends(get_db)
):
    """Get multiple countries by their IDs"""
    try:
        # Convert comma-separated string to list of integers
        country_ids = [int(id.strip()) for id in ids.split(",") if id.strip().isdigit()]
        
        if not country_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid country IDs provided"
            )
        
        countries = CountryService.get_countries_by_ids(db, country_ids)
        return countries
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid country ID format. Provide comma-separated integers."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching countries by IDs: {str(e)}"
        )