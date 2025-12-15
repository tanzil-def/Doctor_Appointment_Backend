from pydantic import BaseModel
from typing import Optional


class DoctorResponse(BaseModel):
    id: int
    user_id: int
    speciality: str
    experience_years: Optional[int]
    about: Optional[str]
    consultation_fee: float
    is_available: bool
    image_url: Optional[str]

    class Config:
        orm_mode = True


class DoctorCreateRequest(BaseModel):
    name: str
    email: str
    password: str
    dob: Optional[str] = None        # YYYY-MM-DD
    gender: Optional[str] = None     # MALE / FEMALE
    speciality: str
    experience_years: Optional[int] = None
    about: Optional[str] = None
    consultation_fee: float
    image_url: Optional[str] = None


class DoctorUpdate(BaseModel):
    speciality: Optional[str] = None
    experience_years: Optional[int] = None
    about: Optional[str] = None
    consultation_fee: Optional[float] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None
