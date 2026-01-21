from pydantic import BaseModel


class UserAuthentication(BaseModel):
    username: str
    password: str
