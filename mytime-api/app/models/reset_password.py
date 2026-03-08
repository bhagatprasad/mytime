from pydantic import BaseModel, Field, root_validator
from typing import Optional


class ResetPassword(BaseModel):
    user_id: int
    new_password: str = Field(..., min_length=8)
    confirm_password: str