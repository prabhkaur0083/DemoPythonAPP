from pydantic import BaseModel


class LoginRequest(BaseModel):
    Email: str
    Password: str
