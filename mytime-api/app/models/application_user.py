from pydantic import BaseModel
from typing import Optional

class ApplicationUser(BaseModel):
    id: Optional[int] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    department_id: Optional[int] = None
    role_id: Optional[int] = None
