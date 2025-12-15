from pydantic import BaseModel
from datetime import date, time
from app.models.enums import AppointmentStatus, PaymentStatus

class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: date
    appointment_time: time


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus
    payment_status: PaymentStatus

    class Config:
        orm_mode = True
