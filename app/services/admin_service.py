from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import date

from app.db.session import async_session
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorResponse

async def list_appointments(skip: int = 0, limit: int = 100):
    async with async_session() as session:
        result = await session.execute(select(Appointment).offset(skip).limit(limit))
        return result.scalars().all()

async def cancel_appointment(appointment_id: int):
    async with async_session() as session:
        result = await session.execute(select(Appointment).where(Appointment.id == appointment_id))
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        appointment.status = "CANCELLED"
        await session.commit()
        await session.refresh(appointment)
        return appointment

async def get_dashboard(skip: int = 0, limit: int = 100):
    async with async_session() as session:
        result = await session.execute(select(Appointment).offset(skip).limit(limit))
        all_appointments = result.scalars().all()

        total = len(all_appointments)
        completed = sum(1 for a in all_appointments if a.status == "COMPLETED")
        cancelled = sum(1 for a in all_appointments if a.status == "CANCELLED")
        today = date.today()
        today_appointments = [a for a in all_appointments if a.appointment_date == today]

        doctor_result = await session.execute(select(Doctor).options(selectinload(Doctor.user)))
        doctors = doctor_result.scalars().all()

        all_doctors_list = [
            DoctorResponse(
                id=d.id,
                user_id=d.user_id,
                name=d.user.name,
                speciality=d.speciality,
                experience_years=d.experience_years,
                about=d.about,
                consultation_fee=float(d.consultation_fee),
                is_available=d.is_available,
                image_url=d.image_url
            )
            for d in doctors
        ]

        return {
            "total_appointments": total,
            "completed_appointments": completed,
            "cancelled_appointments": cancelled,
            "today_appointments_count": len(today_appointments),
            "all_doctors_count": len(doctors),
            "all_doctors": all_doctors_list
        }
