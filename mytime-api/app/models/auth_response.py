from pydantic import BaseModel
from typing import Optional


class AuthResponse(BaseModel):
    jwt_token: Optional[str] = None
    valid_user: bool = False
    valid_password: bool = False
    is_active: bool = False
    status_code: Optional[str] = None
    status_message: Optional[str] = None
