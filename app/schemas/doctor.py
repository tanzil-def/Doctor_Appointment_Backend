from pydantic import BaseModel
from typing import Optional, List
from datetime import time

class DoctorResponse(BaseModel):
    id: int
    user_id: int
    speciality: str
    experience_years: Optional[int]
    about: Optional[str]
    consultation_fee: float
    is_available: bool

    class Config:
        orm_mode = True

class DoctorUpdate(BaseModel):
    speciality: Optional[str]
    experience_years: Optional[int]
    about: Optional[str]
    consultation_fee: Optional[float]
    is_available: Optional[bool]


# -----------------------------
# Dashboard Schema for Doctor
# -----------------------------
class PatientInfo(BaseModel):
    appointment_id: int
    patient_name: str
    appointment_time: str
    status: str
    payment_status: str

class DoctorDashboardResponse(BaseModel):
    today_appointments_count: int
    completed_appointments_count: int
    cancelled_appointments_count: int
    today_patient_list: List[PatientInfo]
