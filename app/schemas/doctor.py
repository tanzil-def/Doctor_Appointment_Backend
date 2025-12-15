from pydantic import BaseModel
from typing import Optional, List

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

class DoctorUpdate(BaseModel):
    speciality: Optional[str]
    experience_years: Optional[int]
    about: Optional[str]
    consultation_fee: Optional[float]
    is_available: Optional[bool]
    image_url: Optional[str]  

class DoctorCreateRequest(BaseModel):
    user_id: int
    speciality: str
    experience_years: Optional[int]
    about: Optional[str]
    consultation_fee: float
    image_url: Optional[str]  
