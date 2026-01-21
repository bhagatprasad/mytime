from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List  # Added List import here

from app.core.database import get_db
from app.schemas.role_schemas import (
    RoleCreate, RoleUpdate, RoleResponse, RoleListResponse,
    RoleExistsResponse, RoleDeleteResponse
)
from app.services.role_service import RoleService

router = APIRouter()

# Exact C# controller endpoints
@router.get("/fetchAllRoles", response_model=List[RoleResponse])  # Now List is defined
async def fetch_all_roles(db: Session = Depends(get_db)):
    """Get all roles - matches C# fetchAllRoles endpoint"""
    try:
        roles = RoleService.fetch_all_roles(db)
        return roles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/InsertOrUpdateRole")
async def insert_or_update_role(role: dict, db: Session = Depends(get_db)):
    """Insert or update role - matches C# InsertOrUpdateRole endpoint"""
    try:
        response = RoleService.insert_or_update_role(db, role)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/DeleteRole/{id}", response_model=RoleDeleteResponse)
async def delete_role(id: int, db: Session = Depends(get_db)):
    """Delete role - matches C# DeleteRole endpoint"""
    try:
        response = RoleService.delete_role(db, id)
        if not response["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["message"]
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/fetchRole/{id}", response_model=RoleResponse)
async def fetch_role(id: int, db: Session = Depends(get_db)):
    """Get role by ID - matches C# fetchRole endpoint"""
    try:
        role = RoleService.fetch_role(db, id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        return role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )