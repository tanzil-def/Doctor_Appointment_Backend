from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.services.doctor_service import create_doctor_by_admin, list_doctors, change_availability
from app.services.admin_service import list_appointments, cancel_appointment, get_dashboard
from app.schemas.doctor import DoctorResponse
from app.core.dependencies import get_current_admin
import os

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/doctors", response_model=DoctorResponse)
async def add_doctor_route(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    dob: str | None = Form(None),
    gender: str | None = Form(None),
    speciality: str = Form(...),
    experience_years: int | None = Form(None),
    about: str | None = Form(None),
    consultation_fee: float = Form(...),
    image: UploadFile | None = File(None),
    current_admin=Depends(get_current_admin)
):
    """
    Admin adds a doctor. Use form-data if uploading an image.
    """
    image_url = None
    if image:
        os.makedirs("media/doctors", exist_ok=True)
        path = f"media/doctors/{email}_{image.filename}"
        with open(path, "wb") as f:
            f.write(await image.read())
        image_url = f"/media/doctors/{email}_{image.filename}"

    doctor = await create_doctor_by_admin(
        name=name,
        email=email,
        password=password,
        dob=dob,
        gender=gender,
        speciality=speciality,
        experience_years=experience_years,
        about=about,
        consultation_fee=consultation_fee,
        image_url=image_url
    )
    return doctor

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
