from pydantic import BaseModel
from app.models.enums import PaymentStatus

class PaymentCreate(BaseModel):
    appointment_id: int
    amount: float
    method: str


class PaymentResponse(BaseModel):
    id: int
    appointment_id: int
    amount: float
    method: str
    status: PaymentStatus

    class Config:
        orm_mode = True
