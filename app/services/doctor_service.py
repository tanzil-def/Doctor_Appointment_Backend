from fastapi import HTTPException
from sqlalchemy import select
from datetime import datetime

from app.db.session import async_session
from app.models.user import User, UserRole
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.enums import AppointmentStatus
from app.core.security import get_password_hash


def parse_dob(dob: str | None):
    if not dob:
        return None
    try:
        return datetime.strptime(dob, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="DOB must be YYYY-MM-DD")


async def create_doctor_by_admin(
    name: str,
    email: str,
    password: str,
    dob: str = None,
    gender: str = None,
    speciality: str = None,
    experience_years: int = None,
    about: str = None,
    consultation_fee: float = None,
    image_url: str = None
):
    async with async_session() as session:
        exists = await session.execute(select(User).where(User.email == email))
        if exists.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already exists")

        user = User(
            name=name,
            email=email,
            password=get_password_hash(password),
            role=UserRole.DOCTOR,
            dob=parse_dob(dob),
            gender=gender.upper() if gender else None,
            is_active=True
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        doctor = Doctor(
            user_id=user.id,
            speciality=speciality,
            experience_years=experience_years,
            about=about,
            consultation_fee=consultation_fee,
            image_url=image_url,
            is_available=True
        )
        session.add(doctor)
        await session.commit()
        await session.refresh(doctor)
        return doctor


async def list_doctors(skip: int = 0, limit: int = 100):
    async with async_session() as session:
        result = await session.execute(
            select(Doctor).offset(skip).limit(limit)
        )
        return result.scalars().all()


async def change_availability(doctor_id: int, is_available: bool):
    async with async_session() as session:
        result = await session.execute(select(Doctor).where(Doctor.id == doctor_id))
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        doctor.is_available = is_available
        await session.commit()
        await session.refresh(doctor)
        return doctor


async def get_doctor_profile(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(Doctor).where(Doctor.user_id == user_id))
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        user = await session.get(User, user_id)

        return {
            "id": doctor.id,
            "user_id": user.id,
            "name": user.name,
            "speciality": doctor.speciality,
            "experience_years": doctor.experience_years,
            "about": doctor.about,
            "consultation_fee": doctor.consultation_fee,
            "image_url": doctor.image_url,
            "is_available": doctor.is_available
        }


async def update_doctor_profile(user_id: int, data):
    async with async_session() as session:
        result = await session.execute(select(Doctor).where(Doctor.user_id == user_id))
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(doctor, key, value)

        await session.commit()
        await session.refresh(doctor)

        user = await session.get(User, user_id)

        return {
            "id": doctor.id,
            "user_id": user.id,
            "name": user.name,
            "speciality": doctor.speciality,
            "experience_years": doctor.experience_years,
            "about": doctor.about,
            "consultation_fee": doctor.consultation_fee,
            "image_url": doctor.image_url,
            "is_available": doctor.is_available
        }


async def list_doctor_appointments(doctor_user):
    async with async_session() as session:
        result = await session.execute(
            select(Appointment).where(Appointment.doctor_id == doctor_user.id)
        )
        return result.scalars().all()


async def complete_appointment(doctor_user, appointment_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.doctor_id == doctor_user.id
            )
        )
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

        appointment.status = AppointmentStatus.COMPLETED
        await session.commit()
        await session.refresh(appointment)
        return appointment


async def get_doctor_dashboard(doctor_user):
    async with async_session() as session:
        total = await session.execute(
            select(Appointment).where(Appointment.doctor_id == doctor_user.id)
        )
        today = await session.execute(
            select(Appointment).where(
                Appointment.doctor_id == doctor_user.id,
                Appointment.appointment_date == datetime.today().date()
            )
        )
        cancelled = await session.execute(
            select(Appointment).where(
                Appointment.doctor_id == doctor_user.id,
                Appointment.status == AppointmentStatus.CANCELLED
            )
        )
        paid = await session.execute(
            select(Appointment).where(
                Appointment.doctor_id == doctor_user.id,
                Appointment.payment_status == "PAID"
            )
        )

        return {
            "total_appointments": len(total.scalars().all()),
            "today_appointments": len(today.scalars().all()),
            "cancelled_appointments": len(cancelled.scalars().all()),
            "paid_appointments": len(paid.scalars().all())
        }


async def list_public_doctors():
    async with async_session() as session:
        result = await session.execute(
            select(
                Doctor.id,
                Doctor.speciality,
                Doctor.experience_years,
                Doctor.about,
                Doctor.consultation_fee,
                Doctor.image_url,
                Doctor.is_available,
                User.name
            )
            .join(User, User.id == Doctor.user_id)
            .where(User.is_active == True)
        )

        return [
            {
                "id": row.id,
                "name": row.name,
                "speciality": row.speciality,
                "experience_years": row.experience_years,
                "about": row.about,
                "consultation_fee": row.consultation_fee,
                "image_url": row.image_url,
                "is_available": row.is_available
            }
            for row in result.all()
        ]
