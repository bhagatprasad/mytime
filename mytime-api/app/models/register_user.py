from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterUserModel(BaseModel):
    id: Optional[int] = None
    employee_id: Optional[int] = None

    first_name: str
    last_name: str
    email: EmailStr
    phone: str

    department_id: Optional[int] = None
    role_id: Optional[int] = None

    password: Optional[str] = Field(None, min_length=8)

    class Config:
        orm_mode = True
