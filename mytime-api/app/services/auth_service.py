# auth_service.py
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.auth_response import AuthResponse
from app.models.change_password import ChangePassword
from app.models.reset_password import ResetPassword
from app.schemas.user_schemas import UserResponse
from app.utils.hash_salt import HashSalt
from app.core.config import settings

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, used_generates_token_key: str, db: Session):
        self.used_generates_token_key = settings.SECRET_KEY
        self.db = db
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user by username from database
        Used by get_current_user dependency
        """
        try:
            logger.info(f"🔍 Looking for user by username: {username}")
            
            # Query user from database
            query = text("""
                SELECT TOP 1 * FROM [user] 
                WHERE LOWER(Email) = LOWER(:username)
            """)
            
            result = self.db.execute(query, {"username": username.strip()})
            db_user = result.fetchone()
            
            if not db_user:
                logger.warning(f"❌ User not found with email: {username}")
                return None
            
            # Convert to dictionary
            user_dict = {}
            if hasattr(db_user, '_mapping'):
                user_dict = dict(db_user._mapping)
            elif hasattr(db_user, '_asdict'):
                user_dict = db_user._asdict()
            
            logger.info(f"📋 User columns found: {list(user_dict.keys())}")
            
            # Helper function to get column value
            def get_col_value(col_variations):
                for col in col_variations:
                    if col in user_dict:
                        return user_dict[col]
                    # Case-insensitive search
                    for key in user_dict.keys():
                        if isinstance(key, str) and key.lower() == col.lower():
                            return user_dict[key]
                return None
            
            # Extract user information
            user_id = get_col_value(['Id', 'id', 'UserID', 'userid', 'User_Id', 'user_id'])
            email = get_col_value(['Email', 'email'])
            is_active = get_col_value(['IsActive', 'isactive', 'Is_Active', 'is_active', 'Active', 'active'])
            
            # Handle is_active - default to True if None
            if is_active is None:
                is_active_value = True
            else:
                # Convert to boolean if it's string or integer
                if isinstance(is_active, str):
                    is_active_value = is_active.lower() in ['true', '1', 'yes', 'y']
                elif isinstance(is_active, int):
                    is_active_value = bool(is_active)
                else:
                    is_active_value = bool(is_active)
            
            user_info = {
                "id": user_id,
                "username": username,
                "email": email,
                "first_name": get_col_value(['FirstName', 'firstname', 'First_Name', 'first_name', 'FName', 'fname']),
                "last_name": get_col_value(['LastName', 'lastname', 'Last_Name', 'last_name', 'LName', 'lname']),
                "is_active": is_active_value,
                "roles": self._get_user_roles(user_id) if user_id else [],  # Get roles from database
                "department_id": get_col_value(['DepartmentId', 'departmentid', 'Department_Id', 'department_id', 'DeptID', 'deptid']),
                "role_id": get_col_value(['RoleId', 'roleid', 'Role_Id', 'role_id', 'RoleID', 'roleid'])
            }
            
            logger.info(f"✅ Found user: ID={user_info['id']}, Email={user_info['email']}, Active={user_info['is_active']}")
            
            return user_info
            
        except Exception as e:
            logger.error(f"💥 Error getting user {username}: {str(e)}", exc_info=True)
            return None
    
    def _get_user_roles(self, user_id: int) -> list:
        """Get user roles from database"""
        try:
            # Assuming you have a user_roles table or roles in user table
            # Adjust this based on your database schema
            query = text("""
                SELECT r.RoleName FROM [role] r
                INNER JOIN [user] u ON u.RoleId = r.Id
                WHERE u.Id = :user_id
            """)
            
            result = self.db.execute(query, {"user_id": user_id})
            roles = [row[0] for row in result.fetchall() if row[0]]
            
            # If no specific roles found, return default
            if not roles:
                # Check if user has a role_id
                query = text("SELECT RoleId FROM [user] WHERE Id = :user_id")
                result = self.db.execute(query, {"user_id": user_id})
                role_row = result.fetchone()
                
                if role_row and role_row[0]:
                    # Map role_id to role name
                    role_mapping = {
                        1: "admin",
                        2: "manager",
                        3: "user",
                        4: "supervisor"
                        # Add more mappings as needed
                    }
                    role_id = role_row[0]
                    role_name = role_mapping.get(role_id, f"role_{role_id}")
                    roles = [role_name]
            
            return roles
            
        except Exception as e:
            logger.error(f"Error getting roles for user {user_id}: {e}")
            return ["user"]  # Default role
    
    def authenticate_user(self, username: str, password: str) -> AuthResponse:
        """Authenticate user with username and password"""
        auth_response = AuthResponse()
        
        try:
            if not username or not password:
                auth_response.status_message = "Username and password required"
                return auth_response
            
            # Table name is 'user' (singular) and needs to be quoted
            # because 'user' is a reserved keyword in SQL Server
            query = text("""
                SELECT * FROM [user] 
                WHERE LOWER(Email) = LOWER(:username)
            """)
            
            result = self.db.execute(query, {"username": username.strip()})
            db_user = result.fetchone()
            
            if not db_user:
                # Try alternative - sometimes tables are in different schemas
                query = text("""
                    SELECT * FROM [dbo].[user] 
                    WHERE LOWER(Email) = LOWER(:username)
                """)
                result = self.db.execute(query, {"username": username.strip()})
                db_user = result.fetchone()
            
            if not db_user:
                auth_response.status_message = "Invalid user"
                auth_response.valid_user = False
                return auth_response
            
            # Debug: Print column names to see actual structure
            if hasattr(db_user, '_mapping'):
                logger.info(f"User found. Available columns: {list(db_user._mapping.keys())}")
            else:
                logger.info(f"User found. Type: {type(db_user)}")
            
            # Get column values - SQL Server returns Row objects that can be accessed by index or column name
            # Convert to dictionary for easier access
            user_dict = {}
            if hasattr(db_user, '_mapping'):
                user_dict = dict(db_user._mapping)
            elif hasattr(db_user, '_asdict'):
                user_dict = db_user._asdict()
            
            # Try to get common column names with different casings
            def get_col_value(col_variations):
                for col in col_variations:
                    # Try exact match first
                    if col in user_dict:
                        return user_dict[col]
                    # Try case-insensitive match
                    for key in user_dict.keys():
                        if key.lower() == col.lower():
                            return user_dict[key]
                return None
            
            password_hash = get_col_value(['PasswordHash', 'passwordhash', 'Password_Hash', 'password_hash'])
            password_salt = get_col_value(['PasswordSalt', 'passwordsalt', 'Password_Salt', 'password_salt'])
            
            # Get IsActive - default to True if not found
            is_active_col = get_col_value(['IsActive', 'isactive', 'Is_Active', 'is_active', 'Active', 'active'])
            is_active = bool(is_active_col) if is_active_col is not None else True
            
            # Debug logging
            logger.info(f"Password hash found: {password_hash is not None}")
            logger.info(f"Password salt found: {password_salt is not None}")
            logger.info(f"IsActive: {is_active}")
            
            if not password_hash or not password_salt:
                logger.error(f"Password hash/salt not found. User columns: {list(user_dict.keys())}")
                auth_response.status_message = "User account configuration error"
                return auth_response
            
            # Verify password using HashSalt helper
            is_valid_user = HashSalt.verify_password(password, password_hash, password_salt)
            
            if is_valid_user:
                # Generate JWT token
                token = self._generate_jwt_token(username)
                
                auth_response.jwt_token = token
                auth_response.valid_password = True
                auth_response.valid_user = True
                auth_response.is_active = is_active
                auth_response.status_code = "200"
                auth_response.status_message = "Success"
                
                # Log successful authentication
                user_id = get_col_value(['Id', 'id', 'UserID', 'userid', 'User_Id', 'user_id'])
                logger.info(f"User {username} (ID: {user_id}) authenticated successfully")
            else:
                auth_response.status_message = "Invalid Password"
                auth_response.valid_user = True
                auth_response.valid_password = False
            
            return auth_response
            
        except Exception as ex:
            logger.error(f"Authentication error: {str(ex)}", exc_info=True)
            auth_response.status_message = f"Authentication error: {str(ex)}"
            auth_response.status_code = "500"
            return auth_response
    
    def generate_user_claims(self, auth_response: AuthResponse) -> Optional[UserResponse]:
        """Generate user claims from JWT token"""
        try:
            if not auth_response.jwt_token:
                raise ValueError("JWT token is required")
            
            # Validate token
            payload = jwt.decode(
                auth_response.jwt_token,
                self.used_generates_token_key,
                algorithms=["HS256"]
            )
            
            username = payload.get("name")
            if not username:
                raise ValueError("Invalid token: no username claim")
            
            # Query user from database - 'user' is a reserved keyword, need brackets
            query = text("""
                SELECT * FROM [user] 
                WHERE (Email = :username COLLATE SQL_Latin1_General_CP1_CI_AS 
                       OR Phone = :username COLLATE SQL_Latin1_General_CP1_CI_AS) 
                AND IsActive = 1
            """)
            
            result = self.db.execute(query, {"username": username})
            user = result.fetchone()
            
            if not user:
                return None
            
            # Convert to dictionary
            user_dict = {}
            if hasattr(user, '_mapping'):
                user_dict = dict(user._mapping)
            elif hasattr(user, '_asdict'):
                user_dict = user._asdict()
            
            # Helper function to get column value
            def get_col_value(col_variations):
                for col in col_variations:
                    if col in user_dict:
                        return user_dict[col]
                    # Case-insensitive search
                    for key in user_dict.keys():
                        if key.lower() == col.lower():
                            return user_dict[key]
                return None
            
            return UserResponse(
                id=get_col_value(['Id', 'id', 'UserID', 'userid', 'User_Id', 'user_id']),
                first_name=get_col_value(['FirstName', 'firstname', 'First_Name', 'first_name', 'FName', 'fname']),
                last_name=get_col_value(['LastName', 'lastname', 'Last_Name', 'last_name', 'LName', 'lname']),
                email=get_col_value(['Email', 'email']),
                phone=get_col_value(['Phone', 'phone', 'PhoneNumber', 'phonenumber', 'Phone_Number', 'phone_number']),
                role_id=get_col_value(['RoleId', 'roleid', 'Role_Id', 'role_id', 'RoleID', 'roleid']),
                department_id=get_col_value(['DepartmentId', 'departmentid', 'Department_Id', 'department_id', 'DeptID', 'deptid']),
                is_active=get_col_value(['IsActive', 'isactive', 'Is_Active', 'is_active', 'Active', 'active']) or True,
                created_by=get_col_value(['CreatedBy', 'createdby', 'Created_By', 'created_by']),
                created_on=get_col_value(['CreatedOn', 'createdon', 'Created_On', 'created_on']),
                modified_by=get_col_value(['ModifiedBy', 'modifiedby', 'Modified_By', 'modified_by']),
                modified_on=get_col_value(['ModifiedOn', 'modifiedon', 'Modified_On', 'modified_on'])
            )
            
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")
        except Exception as ex:
            logger.error(f"Generate user claims error: {str(ex)}", exc_info=True)
            raise
    
    def forgot_password(self, username: str) -> Optional[UserResponse]:
        """Handle forgot password request"""
        try:
            if not username:
                return None
            
            # Query user from database
            query = text("""
                SELECT * FROM [user] 
                WHERE IsActive = 1 
                AND (Email = :username COLLATE SQL_Latin1_General_CP1_CI_AS 
                     OR Phone = :username COLLATE SQL_Latin1_General_CP1_CI_AS)
            """)
            
            result = self.db.execute(query, {"username": username.strip()})
            db_user = result.fetchone()
            
            if not db_user:
                return None
            
            # Convert to dictionary
            user_dict = {}
            if hasattr(db_user, '_mapping'):
                user_dict = dict(db_user._mapping)
            elif hasattr(db_user, '_asdict'):
                user_dict = db_user._asdict()
            
            # Helper function to get column value
            def get_col_value(col_variations):
                for col in col_variations:
                    if col in user_dict:
                        return user_dict[col]
                    # Case-insensitive search
                    for key in user_dict.keys():
                        if key.lower() == col.lower():
                            return user_dict[key]
                return None
            
            return UserResponse(
                id=get_col_value(['Id', 'id', 'UserID', 'userid', 'User_Id', 'user_id']),
                first_name=get_col_value(['FirstName', 'firstname', 'First_Name', 'first_name', 'FName', 'fname']),
                last_name=get_col_value(['LastName', 'lastname', 'Last_Name', 'last_name', 'LName', 'lname']),
                email=get_col_value(['Email', 'email']),
                phone=get_col_value(['Phone', 'phone', 'PhoneNumber', 'phonenumber', 'Phone_Number', 'phone_number']),
                department_id=get_col_value(['DepartmentId', 'departmentid', 'Department_Id', 'department_id', 'DeptID', 'deptid']),
                role_id=get_col_value(['RoleId', 'roleid', 'Role_Id', 'role_id', 'RoleID', 'roleid']),
                is_active=True  # Already filtered by IsActive = 1
            )
            
        except Exception as ex:
            logger.error(f"Forgot password error: {str(ex)}", exc_info=True)
            raise
    
    def reset_password_async(self, reset_password: ResetPassword) -> bool:
        """Reset user password"""
        try:
            # Query user from database
            query = text("SELECT * FROM [user] WHERE Id = :user_id")
            result = self.db.execute(query, {"user_id": reset_password.user_id})
            db_user = result.fetchone()
            
            if not db_user:
                return False
            
            # Generate new password hash and salt
            hash_salt_result = HashSalt.generate_salted_hash(reset_password.new_password)
            
            # Extract hash and salt
            password_hash = hash_salt_result.get("hash")
            password_salt = hash_salt_result.get("salt")
            
            if not password_hash or not password_salt:
                logger.error("HashSalt.generate_salted_hash did not return expected values")
                return False
            
            # Convert to string if they're bytes
            if isinstance(password_hash, bytes):
                try:
                    password_hash = password_hash.decode('utf-8')
                except:
                    password_hash = str(password_hash)
            
            if isinstance(password_salt, bytes):
                try:
                    password_salt = password_salt.decode('utf-8')
                except:
                    password_salt = str(password_salt)
            
            # Update user - note column names might be different
            update_query = text("""
                UPDATE [user] 
                SET PasswordHash = :password_hash,
                    PasswordSalt = :password_salt,
                    PasswordLastChangedBY = :user_id,
                    ModifiedBy = :user_id,
                    ModifiedOn = GETDATE()
                WHERE Id = :user_id
            """)
            
            result = self.db.execute(update_query, {
                "password_hash": password_hash,
                "password_salt": password_salt,
                "user_id": reset_password.user_id
            })
            
            self.db.commit()
            return result.rowcount == 1
            
        except Exception as ex:
            logger.error(f"Reset password error: {str(ex)}", exc_info=True)
            self.db.rollback()
            raise
    
    def change_password_async(self, change_password: ChangePassword) -> bool:
        """Change user password with old password verification"""
        try:
            # First authenticate with old password
            auth_response = self.authenticate_user(
                change_password.username, 
                change_password.old_password
            )
            
            if not auth_response.valid_user or not auth_response.valid_password:
                return False
            
            # Get user ID
            query = text("SELECT Id FROM [user] WHERE Email = :username COLLATE SQL_Latin1_General_CP1_CI_AS")
            result = self.db.execute(query, {"username": change_password.username.strip()})
            db_user = result.fetchone()
            
            if db_user:
                # Get the user ID
                user_dict = {}
                if hasattr(db_user, '_mapping'):
                    user_dict = dict(db_user._mapping)
                elif hasattr(db_user, '_asdict'):
                    user_dict = db_user._asdict()
                
                # Find the ID column
                def get_user_id():
                    id_variations = ['Id', 'id', 'UserID', 'userid', 'User_Id', 'user_id']
                    for col in id_variations:
                        if col in user_dict:
                            return user_dict[col]
                        # Case-insensitive search
                        for key in user_dict.keys():
                            if key.lower() == col.lower():
                                return user_dict[key]
                    return None
                
                user_id = get_user_id()
                
                if user_id:
                    # Create ResetPassword object for reset
                    reset_data = ResetPassword(
                        user_id=user_id,
                        new_password=change_password.new_password,
                        confirm_password=change_password.confirm_password
                    )
                    
                    # Use reset password logic
                    return self.reset_password_async(reset_data)
            
            return False
            
        except Exception as ex:
            logger.error(f"Change password error: {str(ex)}", exc_info=True)
            raise
    
    def _generate_jwt_token(self, username: str) -> str:
        """Generate JWT token"""
        payload = {
            "name": username,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.used_generates_token_key, algorithm="HS256")
        return token