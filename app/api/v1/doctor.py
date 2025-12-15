from fastapi import APIRouter, Depends

from app.services.doctor_service import (
    get_doctor_profile,
    update_doctor_profile,
    list_doctor_appointments,
    complete_appointment,
    get_doctor_dashboard
)
from app.services.document_service import upload_document

from app.schemas.doctor import DoctorUpdate, DoctorResponse
from app.schemas.appointment import AppointmentResponse
from app.schemas.document import AppointmentDocumentCreate, AppointmentDocumentResponse
from app.core.dependencies import get_current_doctor

router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.get("/profile", response_model=DoctorResponse)
async def profile(current_doctor=Depends(get_current_doctor)):
    return await get_doctor_profile(current_doctor.doctor.id)

@router.patch("/profile", response_model=DoctorResponse)
async def update_profile(
    data: DoctorUpdate,
    current_doctor=Depends(get_current_doctor)
):
    return await update_doctor_profile(current_doctor.doctor.id, data)

@router.get("/appointments", response_model=list[AppointmentResponse])
async def my_appointments(current_doctor=Depends(get_current_doctor)):
    return await list_doctor_appointments(current_doctor)

@router.patch("/appointments/{id}/complete", response_model=AppointmentResponse)
async def complete(
    id: int,
    current_doctor=Depends(get_current_doctor)
):
    return await complete_appointment(current_doctor, id)

@router.post("/appointments/{id}/documents", response_model=AppointmentDocumentResponse)
async def upload_docs(
    id: int,
    data: AppointmentDocumentCreate,
    current_doctor=Depends(get_current_doctor)
):
    return await upload_document(
        user=current_doctor,
        appointment_id=id,
        uploaded_by="DOCTOR",
        file_url=data.file_url,
        file_type=data.file_type
    )

@router.get("/dashboard")
async def dashboard(current_doctor=Depends(get_current_doctor)):
    return await get_doctor_dashboard(current_doctor)
