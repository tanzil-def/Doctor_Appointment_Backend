from fastapi import HTTPException
from sqlalchemy import select
from app.db.session import async_session
from app.models.doctor import Doctor
from app.models.appointment import Appointment


async def add_doctor(data: dict):
    
    doctor = Doctor(**data)
    async with async_session() as session:
        session.add(doctor)
        await session.commit()
        await session.refresh(doctor)
    return doctor


async def list_doctors():
    async with async_session() as session:
        result = await session.execute(select(Doctor))
        return result.scalars().all()
            
async def change_availability(id: int, is_available: bool):
    async with async_session() as session:
        result = await session.execute(select(Doctor).where(Doctor.id == id))
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        doctor.is_available = is_available
        await session.commit()
        await session.refresh(doctor)
    return doctor


async def list_appointments():
    async with async_session() as session:
        result = await session.execute(select(Appointment))
        return result.scalars().all()


async def cancel_appointment(id: int):
    async with async_session() as session:
        result = await session.execute(select(Appointment).where(Appointment.id == id))
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        appointment.status = "CANCELLED"
        await session.commit()
        await session.refresh(appointment)
    return appointment


async def get_dashboard():
    return {"message": "Admin dashboard summary"}
