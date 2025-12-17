from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import GenderEnum

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str]
    dob: Optional[str]
    gender: Optional[GenderEnum] 


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
