# app/services/user_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from typing import Optional, List

from app.models.user import User
from app.schemas.user_schemas import RegisterUser   # ✅ FIX HERE
from app.utils.hash_salt import HashSalt


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Task<User> fetchUser(long id)
    async def fetch_user(self, user_id: int) -> Optional[User]:
        result = await self.db_session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()

    # Task<List<User>> fetchUsers()
    async def fetch_users(self) -> List[User]:
        result = await self.db_session.execute(select(User))
        return result.scalars().all()

    # Task<bool> RegisterUser(RegisterUser registerUser)
    async def register_user(self, register_user: RegisterUser) -> bool:
        if not register_user.id or register_user.id == 0:
            if not register_user.password:
                return False

            hash_salt = HashSalt.generate_salted_hash(register_user.password)

            user = User(
                employee_id=register_user.employee_id,
                first_name=register_user.first_name,
                last_name=register_user.last_name,
                role_id=register_user.role_id,
                department_id=register_user.department_id,
                email=register_user.email,
                phone=register_user.phone,
                password_hash=hash_salt["hash"],
                password_salt=hash_salt["salt"],
                created_by=-1,
                created_on=datetime.utcnow(),
                modified_by=-1,
                modified_on=datetime.utcnow(),
                is_active=True,
                user_wrong_password_count=0,
                is_blocked=False
            )

            self.db_session.add(user)

        try:
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            print(f"Error saving user: {e}")
            return False
