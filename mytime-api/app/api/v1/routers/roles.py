from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List  # Added List import here

from app.core.database import get_db
from app.schemas.role_schemas import (
    RoleCreate, RoleUpdate, RoleResponse, RoleListResponse,
    RoleExistsResponse, RoleDeleteResponse
)
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])

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

# Additional RESTful endpoints (optional)
@router.get("/", response_model=RoleListResponse)
async def get_roles(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    sort_by: str = Query("Id", regex="^(Id|Name|Code|CreatedOn|ModifiedOn)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """Get paginated roles"""
    try:
        skip = (page - 1) * size
        roles, total = RoleService.get_roles_with_pagination(
            db=db,
            skip=skip,
            limit=size,
            search=search,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        pages = (total + size - 1) // size
        
        return RoleListResponse(
            total=total,
            items=roles,
            page=page,
            size=size,
            pages=pages
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    """Create new role (RESTful)"""
    try:
        return RoleService.create_role(db, role)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int, 
    role: RoleUpdate, 
    db: Session = Depends(get_db)
):
    """Update role (RESTful)"""
    try:
        updated_role = RoleService.update_role(db, role_id, role)
        if not updated_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        return updated_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{role_id}/exists", response_model=RoleExistsResponse)
async def check_role_exists(role_id: int, db: Session = Depends(get_db)):
    """Check if role exists"""
    try:
        exists = RoleService.fetch_role(db, role_id) is not None
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )