from fastapi import APIRouter, Depends
from app.services.admin_service import add_doctor, list_doctors, change_availability, list_appointments, cancel_appointment, get_dashboard
from app.core.dependencies import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/doctors")
async def add_doctor_route(data: dict, current_admin=Depends(get_current_admin)):
    return await add_doctor(data)

@router.get("/doctors")
async def get_all_doctors(current_admin=Depends(get_current_admin)):
    return await list_doctors()

@router.patch("/doctors/{id}/availability")
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
