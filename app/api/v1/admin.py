from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.services.admin_service import add_doctor, list_doctors, change_availability, list_appointments, cancel_appointment, get_dashboard
from app.core.dependencies import get_current_admin
from app.schemas.doctor import DoctorResponse
import os  # <<< import os for folder creation

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/doctors", response_model=DoctorResponse)
async def add_doctor_route(
    user_id: int = Form(...),
    speciality: str = Form(...),
    experience_years: int = Form(0),
    about: str = Form(None),
    consultation_fee: float = Form(...),
    image: UploadFile | None = File(None),
    current_admin=Depends(get_current_admin)
):
    """
    Admin adds a doctor. Use form-data if uploading an image.
    """
    doctor_data = {
        "user_id": user_id,
        "speciality": speciality,
        "experience_years": experience_years,
        "about": about,
        "consultation_fee": consultation_fee,
        "image_url": None
    }

    if image:
        os.makedirs("uploads/doctors", exist_ok=True)
        contents = await image.read()
        filename = f"uploads/doctors/{image.filename}"
        with open(filename, "wb") as f:
            f.write(contents)
        doctor_data["image_url"] = filename

    return await add_doctor(doctor_data)

@router.get("/doctors", response_model=list[DoctorResponse])
async def get_all_doctors(current_admin=Depends(get_current_admin)):
    return await list_doctors()

@router.patch("/doctors/{id}/availability", response_model=DoctorResponse)
async def change_doctor_availability(id: int, is_available: bool, current_admin=Depends(get_current_admin)):
    return await change_availability(id, is_available)

@router.get("/appointments")
async def get_all_appointments(current_admin=Depends(get_current_admin)):
    return await list_appointments()

@router.post("/appointments/{id}/cancel")
async def admin_cancel_appointment(id: int, current_admin=Depends(get_current_admin)):
    return await cancel_appointment(id)

@router.get("/dashboard")
async def admin_dashboard(current_admin=Depends(get_current_admin)):
    return await get_dashboard()
