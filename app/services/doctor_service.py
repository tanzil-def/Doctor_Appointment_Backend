from fastapi import HTTPException
from sqlalchemy import select
from datetime import date
from app.db.session import async_session
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.user import User
from app.models.enums import AppointmentStatus
from app.utils.permissions import check_role

# --- Get doctor by user_id ---
async def get_doctor_by_id(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(Doctor).where(Doctor.user_id == user_id))
        return result.scalar_one_or_none()

# --- Get doctor profile ---
async def get_doctor_profile(doctor_id: int):
    async with async_session() as session:
        result = await session.execute(select(Doctor).where(Doctor.id == doctor_id))
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor

# --- Update doctor profile ---
async def update_doctor_profile(doctor_id: int, data):
    doctor = await get_doctor_profile(doctor_id)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(doctor, field, value)
    async with async_session() as session:
        session.add(doctor)
        await session.commit()
        await session.refresh(doctor)
    return doctor

# --- Add doctor (Admin) ---
async def add_doctor(data: dict):
    doctor = Doctor(**data)
    async with async_session() as session:
        session.add(doctor)
        await session.commit()
        await session.refresh(doctor)
    return doctor

# --- List doctors (Admin) ---
async def list_doctors():
    async with async_session() as session:
        result = await session.execute(select(Doctor))
        return result.scalars().all()

# --- Change doctor availability ---
async def change_availability(id: int, is_available: bool):
    async with async_session() as session:
        result = await session.execute(select(Doctor).where(Doctor.id == id))
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        doctor.is_available = is_available
        session.add(doctor)
        await session.commit()
        await session.refresh(doctor)
        return doctor

# --- List doctor appointments ---
async def list_doctor_appointments(current_user):
    check_role(current_user.role, ["DOCTOR"])
    if not current_user.doctor:
        raise HTTPException(status_code=400, detail="Doctor profile not found")
    async with async_session() as session:
        result = await session.execute(
            select(Appointment).where(Appointment.doctor_id == current_user.doctor.id)
        )
        return result.scalars().all()

# --- Complete appointment ---
async def complete_appointment(current_user, appointment_id: int):
    check_role(current_user.role, ["DOCTOR"])
    if not current_user.doctor:
        raise HTTPException(status_code=400, detail="Doctor profile not found")
    async with async_session() as session:
        result = await session.execute(
            select(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.doctor_id == current_user.doctor.id
            )
        )
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        appointment.status = AppointmentStatus.COMPLETED.value
        await session.commit()
        await session.refresh(appointment)
        return appointment

# --- Doctor dashboard ---
async def get_doctor_dashboard(current_user):
    check_role(current_user.role, ["DOCTOR"])
    if not current_user.doctor:
        raise HTTPException(status_code=400, detail="Doctor profile not found")

    today = date.today()
    async with async_session() as session:
        result_today = await session.execute(
            select(Appointment).where(
                Appointment.doctor_id == current_user.doctor.id,
                Appointment.appointment_date == today
            )
        )
        today_appointments = result_today.scalars().all()

        result_all = await session.execute(
            select(Appointment).where(Appointment.doctor_id == current_user.doctor.id)
        )
        all_appointments = result_all.scalars().all()

        completed_count = sum(1 for a in all_appointments if a.status == AppointmentStatus.COMPLETED.value)
        cancelled_count = sum(1 for a in all_appointments if a.status == AppointmentStatus.CANCELLED.value)

        patient_list = []
        for app in today_appointments:
            stmt = await session.execute(select(User).where(User.id == app.user_id))
            patient = stmt.scalar_one_or_none()
            patient_list.append({
                "appointment_id": app.id,
                "patient_name": patient.name if patient else "Unknown",
                "appointment_time": str(app.appointment_time),
                "status": app.status,
                "payment_status": app.payment_status
            })

    return {
        "today_appointments_count": len(today_appointments),
        "completed_appointments_count": completed_count,
        "cancelled_appointments_count": cancelled_count,
        "today_patient_list": patient_list
    }
