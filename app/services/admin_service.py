from sqlalchemy import select, func
from fastapi import HTTPException

from app.db.session import async_session
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.user import User
from app.models.enums import AppointmentStatus, UserRole


# =========================
# ADD NEW DOCTOR
# =========================
async def add_doctor(data: dict):
    async with async_session() as session:
        doctor = Doctor(**data)
        session.add(doctor)
        await session.commit()
        await session.refresh(doctor)
        return doctor


# =========================
# LIST ALL DOCTORS
# =========================
async def list_doctors():
    async with async_session() as session:
        result = await session.execute(select(Doctor))
        return result.scalars().all()


# =========================
# CHANGE DOCTOR AVAILABILITY
# =========================
async def change_availability(doctor_id: int, is_available: bool):
    async with async_session() as session:
        doctor = await session.get(Doctor, doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        doctor.is_available = is_available
        await session.commit()
        await session.refresh(doctor)
        return doctor


# =========================
# LIST ALL APPOINTMENTS
# =========================
async def list_appointments():
    async with async_session() as session:
        result = await session.execute(select(Appointment))
        return result.scalars().all()


# =========================
# CANCEL APPOINTMENT (ADMIN)
# =========================
async def cancel_appointment(appointment_id: int):
    async with async_session() as session:
        appointment = await session.get(Appointment, appointment_id)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        appointment.status = AppointmentStatus.CANCELLED.value
        await session.commit()
        await session.refresh(appointment)
        return appointment


# =========================
# DASHBOARD DATA
# =========================
async def get_dashboard():
    async with async_session() as session:
        users_count = await session.scalar(select(func.count()).select_from(User))
        doctors_count = await session.scalar(select(func.count()).select_from(Doctor))
        appointments_count = await session.scalar(select(func.count()).select_from(Appointment))

        return {
            "users": users_count,
            "doctors": doctors_count,
            "appointments": appointments_count
        }