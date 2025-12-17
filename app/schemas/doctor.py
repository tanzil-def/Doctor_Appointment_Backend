from pydantic import BaseModel, EmailStr
from typing import Optional

class DoctorResponse(BaseModel):
    id: int
    user_id: int
    name: str
    speciality: str
    experience_years: Optional[int]
    about: Optional[str]
    consultation_fee: float
    is_available: bool
    image_url: Optional[str]

    class Config:
        from_attributes = True


class DoctorCreateRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    dob: Optional[str] = None
    gender: Optional[str] = None
    speciality: str
    experience_years: Optional[int] = None
    about: Optional[str] = None
    consultation_fee: float
    image_url: Optional[str] = None


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    speciality: Optional[str] = None
    experience_years: Optional[int] = None
    about: Optional[str] = None
    consultation_fee: Optional[float] = None
    image_url: Optional[str] = None
