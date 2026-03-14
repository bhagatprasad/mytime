from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.models.user import User
from app.schemas.user_schemas import RegisterUser
from app.utils.hash_salt import HashSalt


class UserService:

    @staticmethod
    def fetch_user(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID - matches fetchUser in C#"""
        return db.query(User).filter(User.Id == user_id).first()

    @staticmethod
    def fetch_all_users(db: Session) -> List[User]:
        """Get all users - matches fetchAllUsers in C#"""
        return db.query(User).all()

    @staticmethod
    def register_user(db: Session, register_user: RegisterUser) -> bool:
        """Register new user - matches RegisterUser in C#"""
        if not register_user.password:
            return False

        hash_salt = HashSalt.generate_salted_hash(register_user.password)

        db_user = User(
            EmployeeId=register_user.employee_id,
            FirstName=register_user.first_name,
            LastName=register_user.last_name,
            RoleId=register_user.role_id,
            DepartmentId=register_user.department_id,
            Email=register_user.email,
            Phone=register_user.phone,
            PasswordHash=hash_salt["hash"],
            PasswordSalt=hash_salt["salt"],
            PasswordlastChangedOn=datetime.utcnow(),  # Set current time for password last changed
            PasswordLastChangedBY=-1,  # System user ID
            UserWorngPasswordCount=0,  # Initialize to 0 (note: typo in model - "Worng" instead of "Wrong")
            UserLastWrongPasswordOn=None,  # Initialize as null
            IsBlocked=False,
            IsActive=True,
            CreatedBy=-1,
            CreatedOn=datetime.utcnow(),
            ModifiedBy=-1,
            ModifiedOn=datetime.utcnow()
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return True

    @staticmethod
    def insert_or_update_user(db: Session, user_data: dict) -> Dict[str, Any]:
        """Insert or update user - matches InsertOrUpdateUser in C#"""
        user_id = user_data.get('Id')

        if user_id:
            db_user = db.query(User).filter(User.Id == user_id).first()
            if not db_user:
                return {"success": False, "message": "User not found", "user": None}

            for key, value in user_data.items():
                if key != 'Id' and value is not None:
                    setattr(db_user, key, value)

            db.commit()
            db.refresh(db_user)
            return {"success": True, "message": "User updated successfully", "user": db_user}
        else:
            user_data.pop('Id', None)
            db_user = User(**user_data)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return {"success": True, "message": "User created successfully", "user": db_user}

    @staticmethod
    def delete_user(db: Session, user_id: int) -> Dict[str, Any]:
        """Delete user - matches DeleteUser in C#"""
        db_user = db.query(User).filter(User.Id == user_id).first()
        if not db_user:
            return {"success": False, "message": "User not found"}

        db.delete(db_user)
        db.commit()
        return {"success": True, "message": "User deleted successfully"}