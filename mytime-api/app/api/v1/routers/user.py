from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.user_schemas import UserResponse, RegisterUser
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def fetch_users(db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    users = await service.fetch_users()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def fetch_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=bool, status_code=status.HTTP_201_CREATED)
async def register_user(
    register_user: RegisterUser,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    success = await service.register_user(register_user)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to register user")
    return success
