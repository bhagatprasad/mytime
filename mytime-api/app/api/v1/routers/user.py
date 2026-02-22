from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.user_schemas import UserResponse, RegisterUser
from app.services.user_service import UserService

router = APIRouter()


@router.get("/fetchAllUsers", response_model=List[UserResponse])
async def fetch_all_users(db: Session = Depends(get_db)):
    """Get all users - matches C# fetchAllUsers endpoint"""
    try:
        users = UserService.fetch_all_users(db)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/fetchUser/{id}", response_model=UserResponse)
async def fetch_user(id: int, db: Session = Depends(get_db)):
    """Get user by ID - matches C# fetchUser endpoint"""
    try:
        user = UserService.fetch_user(db, id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/InsertOrUpdateUser")
async def insert_or_update_user(user: dict, db: Session = Depends(get_db)):
    """Insert or update user - matches C# InsertOrUpdateUser endpoint"""
    try:
        response = UserService.insert_or_update_user(db, user)
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


@router.post("/RegisterUser", response_model=bool, status_code=status.HTTP_201_CREATED)
async def register_user(register_user: RegisterUser, db: Session = Depends(get_db)):
    """Register a new user - matches C# RegisterUser endpoint"""
    try:
        response = UserService.register_user(db, register_user)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to register user"
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/DeleteUser/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    """Delete user - matches C# DeleteUser endpoint"""
    try:
        response = UserService.delete_user(db, id)
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