from fastapi import APIRouter, Depends, UploadFile, HTTPException
from typing import List
from app.schemas.appointment import AppointmentResponse
from app.schemas.document import AppointmentDocumentResponse, AppointmentDocumentCreate
from app.services.appointment_service import get_appointment_documents, create_appointment, list_user_appointments, cancel_appointment
from app.services.document_service import upload_appointment_document
from app.core.dependencies import get_current_active_user  # JWT user dependency
from app.models.user import User

router = APIRouter(prefix="/appointments", tags=["Appointments"])


# List user's appointments
@router.get("/", response_model=List[AppointmentResponse])
async def my_appointments(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    return await list_user_appointments(current_user, skip, limit)


# Create an appointment
@router.post("/", response_model=AppointmentResponse)
async def book_appointment(
    doctor_id: int,
    appointment_date: str,
    appointment_time: str,
    current_user: User = Depends(get_current_active_user)
):
    return await create_appointment(
        current_user,
        doctor_id,
        appointment_date,
        appointment_time
    )


# Cancel appointment
@router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
async def cancel(appointment_id: int, current_user: User = Depends(get_current_active_user)):
    return await cancel_appointment(current_user, appointment_id)


# Upload document for an appointment
@router.post("/{appointment_id}/documents", response_model=AppointmentDocumentResponse)
async def upload_docs(
    appointment_id: int,
    file: UploadFile,
    file_type: str,
    current_user: User = Depends(get_current_active_user)
):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    return await upload_appointment_document(
        user=current_user,
        appointment_id=appointment_id,
        file=file,
        file_type=file_type
    )



@router.get("/{appointment_id}/documents", response_model=List[AppointmentDocumentResponse])
async def list_documents(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user)
):
    return await get_appointment_documents(current_user, appointment_id)
