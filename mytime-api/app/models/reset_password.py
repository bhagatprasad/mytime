from pydantic import BaseModel, Field, root_validator
from typing import Optional


class ResetPasswordModel(BaseModel):
    user_id: int
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @root_validator
    def passwords_match(cls, values):
        new_password = values.get("new_password")
        confirm_password = values.get("confirm_password")

        if new_password != confirm_password:
            raise ValueError("New password and Confirm password must match")

        return values
