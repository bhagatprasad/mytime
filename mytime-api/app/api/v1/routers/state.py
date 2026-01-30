from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.state_schemas import (
    StateCreate, StateUpdate, StateResponse, StateListResponse,
    StateExistsResponse, StateDeleteResponse
)
from app.core.database import get_db
from app.services.state_service import StateService

router = APIRouter()


@router.get("/fetchState/{state_id}", response_model=StateResponse)
async def fetch_state(state_id: int, db: Session = Depends(get_db)):
    """Get state by ID - matches C# fetchState endpoint"""
    try:
        state = StateService.fetch_state(db, state_id)
        if not state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"State with ID {state_id} not found"
            )
        return state
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching state: {str(e)}"
        )


@router.get("/fetchAllStates", response_model=List[StateResponse])
async def fetch_all_states(db: Session = Depends(get_db)):
    """Get all states - matches C# fetchAllStates endpoint"""
    try:
        states = StateService.fetch_all_states(db)
        return states
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching states: {str(e)}"
        )


@router.get("/getStates", response_model=StateListResponse)
async def get_states(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=500, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    country_id: Optional[int] = Query(None, description="Filter by country ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("StateId", description="Sort column"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get paginated states with filtering and sorting"""
    try:
        skip = (page - 1) * size
        items, total = StateService.get_states_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            country_id=country_id,
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
            detail=f"Error fetching states: {str(e)}"
        )


@router.post("/InsertOrUpdateState")
async def insert_or_update_state(state: dict, db: Session = Depends(get_db)):
    """Insert or update state - matches C# InsertOrUpdateState endpoint"""
    try:
        response = StateService.insert_or_update_state(db, state)
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
            detail=f"Error saving state: {str(e)}"
        )


@router.delete("/DeleteState/{state_id}", response_model=StateDeleteResponse)
async def delete_state(state_id: int, db: Session = Depends(get_db)):
    """Delete state - matches C# DeleteState endpoint"""
    try:
        response = StateService.delete_state(db, state_id)
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
            detail=f"Error deleting state: {str(e)}"
        )


@router.get("/checkStateExists", response_model=StateExistsResponse)
async def check_state_exists(
    name: str = Query(..., description="State name"),
    country_id: int = Query(..., description="Country ID"),
    exclude_id: Optional[int] = Query(None, description="State ID to exclude (for updates)"),
    db: Session = Depends(get_db)
):
    """Check if state exists - matches C# checkStateExists endpoint"""
    try:
        exists = StateService.check_state_exists(db, name, country_id, exclude_id)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking state existence: {str(e)}"
        )


@router.get("/getStatesByCountry/{country_id}", response_model=List[StateResponse])
async def get_states_by_country(country_id: int, db: Session = Depends(get_db)):
    """Get all states for a specific country"""
    try:
        states = StateService.get_states_by_country(db, country_id)
        return states
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching states by country: {str(e)}"
        )


@router.get("/getStatesByCountryCode/{country_code}", response_model=List[StateResponse])
async def get_states_by_country_code(country_code: str, db: Session = Depends(get_db)):
    """Get states by country code"""
    try:
        states = StateService.get_states_by_country_code(db, country_code)
        return states
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching states by country code: {str(e)}"
        )


@router.get("/getStateByCode/{state_code}", response_model=StateResponse)
async def get_state_by_code(
    state_code: str,
    country_code: Optional[str] = Query(None, description="Country code filter"),
    db: Session = Depends(get_db)
):
    """Get state by state code"""
    try:
        state = StateService.get_state_by_code(db, state_code, country_code)
        if not state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"State with code '{state_code}' not found"
            )
        return state
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching state by code: {str(e)}"
        )


@router.patch("/toggleActiveStatus/{state_id}", response_model=StateResponse)
async def toggle_active_status(
    state_id: int,
    is_active: bool = Query(..., description="New active status (true/false)"),
    db: Session = Depends(get_db)
):
    """Toggle the active status of a state"""
    try:
        state = StateService.toggle_active_status(db, state_id, is_active)
        if not state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"State with ID {state_id} not found"
            )
        return state
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling active status: {str(e)}"
        )


# Alternative endpoints using Pydantic models (for API-first approach)
@router.post("/create", response_model=StateResponse, status_code=status.HTTP_201_CREATED)
async def create_state(state: StateCreate, db: Session = Depends(get_db)):
    """Create a new state using Pydantic model"""
    try:
        return StateService.create_state(db, state)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating state: {str(e)}"
        )


@router.put("/update/{state_id}", response_model=StateResponse)
async def update_state(state_id: int, state: StateUpdate, db: Session = Depends(get_db)):
    """Update an existing state using Pydantic model"""
    try:
        updated_state = StateService.update_state(db, state_id, state)
        if not updated_state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"State with ID {state_id} not found"
            )
        return updated_state
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
            detail=f"Error updating state: {str(e)}"
        )