from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas.state_schemas import (
    StateResponse, StateDeleteResponse
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