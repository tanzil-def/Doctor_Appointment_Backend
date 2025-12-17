from fastapi import APIRouter, Depends, UploadFile

from app.core.dependencies import get_current_doctor
from app.services.doctor_service import (
    get_doctor_profile,
    update_doctor_profile,
    list_doctor_appointments,
    complete_appointment,
    get_doctor_dashboard,
    list_public_doctors
)
from app.services.document_service import upload_appointment_document
from app.schemas.doctor import DoctorUpdate, DoctorResponse
from app.schemas.appointment import AppointmentResponse
from app.schemas.document import (
    AppointmentDocumentUploadRequest,
    AppointmentDocumentResponse
)

router = APIRouter(prefix="/doctor", tags=["Doctor"])


@router.get("/list")
async def get_public_doctors():
    return await list_public_doctors()


@router.get("/profile", response_model=DoctorResponse)
async def profile(current_doctor=Depends(get_current_doctor)):
    return await get_doctor_profile(current_doctor.id)


@router.patch("/profile", response_model=DoctorResponse)
async def update_profile(
    data: DoctorUpdate,
    current_doctor=Depends(get_current_doctor)
):
    return await update_doctor_profile(current_doctor.id, data)


@router.get("/appointments", response_model=list[AppointmentResponse])
async def my_appointments(current_doctor=Depends(get_current_doctor)):
    return await list_doctor_appointments(current_doctor)


@router.patch(
    "/appointments/{appointment_id}/complete",
    response_model=AppointmentResponse
)
async def complete(
    appointment_id: int,
    current_doctor=Depends(get_current_doctor)
):
    return await complete_appointment(current_doctor, appointment_id)


@router.post(
    "/appointments/{appointment_id}/documents",
    response_model=AppointmentDocumentResponse
)
async def upload_docs(
    appointment_id: int,
    file: UploadFile,
    data: AppointmentDocumentUploadRequest,
    current_doctor=Depends(get_current_doctor)
):
    return await upload_appointment_document(
        user=current_doctor,
        appointment_id=appointment_id,
        file=file,
        file_type=data.file_type
    )


@router.get("/dashboard")
async def dashboard(current_doctor=Depends(get_current_doctor)):
    return await get_doctor_dashboard(current_doctor)
