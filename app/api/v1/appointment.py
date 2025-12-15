from fastapi import APIRouter
from app.services.appointment_service import get_appointment_documents
from app.schemas.document import AppointmentDocumentResponse

router = APIRouter(prefix="/appointments", tags=["Shared"])

@router.get("/{id}/documents", response_model=list[AppointmentDocumentResponse])
async def documents(id: int):
    return await get_appointment_documents(id)
