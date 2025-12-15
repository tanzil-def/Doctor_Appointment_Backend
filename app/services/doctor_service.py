from fastapi import HTTPException
from sqlalchemy import select
from datetime import datetime, date

from app.db.session import async_session
from app.models.user import User, UserRole
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.enums import AppointmentStatus
from app.core.security import get_password_hash
from app.utils.permissions import check_role



def parse_dob(dob: str | None):
    if not dob:
        return None
    try:
        return datetime.strptime(dob, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="DOB must be in YYYY-MM-DD format"
        )



async def get_doctor_by_id(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Doctor).where(Doctor.user_id == user_id)
        )
        return result.scalar_one_or_none()


async def get_doctor_profile(doctor_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Doctor).where(Doctor.id == doctor_id)
        )
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor


async def update_doctor_profile(doctor_id: int, data):
    async with async_session() as session:
        result = await session.execute(
            select(Doctor).where(Doctor.id == doctor_id)
        )
        doctor = result.scalar_one_or_none()

        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(doctor, field, value)

        await session.commit()
        await session.refresh(doctor)
        return doctor





async def create_doctor_by_admin(
    name: str,
    email: str,
    password: str,
    phone: str = None,
    dob: str = None,
    gender: str = None,
    speciality: str = None,
    experience_years: int = None,
    about: str = None,
    consultation_fee: float = None,
    image_url: str = None
):
    async with async_session() as session:

        
        result = await session.execute(
            select(User).where(User.email == email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already exists")

        
        dob_date = parse_dob(dob)

        user = User(
            name=name,
            email=email,
            password=get_password_hash(password),
            role=UserRole.DOCTOR,
            phone=phone,
            dob=dob_date,                       
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



async def list_doctors():
    async with async_session() as session:
        result = await session.execute(select(Doctor))
        return result.scalars().all()


async def change_availability(id: int, is_available: bool):
    async with async_session() as session:
        result = await session.execute(
            select(Doctor).where(Doctor.id == id)
        )
        doctor = result.scalar_one_or_none()

        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        doctor.is_available = is_available
        await session.commit()
        await session.refresh(doctor)
        return doctor


async def list_doctor_appointments(current_user):
    check_role(current_user.role, ["DOCTOR"])

    if not current_user.doctor:
        raise HTTPException(status_code=400, detail="Doctor profile not found")

    async with async_session() as session:
        result = await session.execute(
            select(Appointment).where(
                Appointment.doctor_id == current_user.doctor.id
            )
        )
        return result.scalars().all()


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


async def get_doctor_dashboard(current_user):
    check_role(current_user.role, ["DOCTOR"])

    if not current_user.doctor:
        raise HTTPException(status_code=400, detail="Doctor profile not found")

    today = date.today()

    async with async_session() as session:
        today_result = await session.execute(
            select(Appointment).where(
                Appointment.doctor_id == current_user.doctor.id,
                Appointment.appointment_date == today
            )
        )
        today_appointments = today_result.scalars().all()

        all_result = await session.execute(
            select(Appointment).where(
                Appointment.doctor_id == current_user.doctor.id
            )
        )
        all_appointments = all_result.scalars().all()

        completed = sum(1 for a in all_appointments if a.status == AppointmentStatus.COMPLETED.value)
        cancelled = sum(1 for a in all_appointments if a.status == AppointmentStatus.CANCELLED.value)

        patient_list = []
        for app in today_appointments:
            user_result = await session.execute(
                select(User).where(User.id == app.user_id)
            )
            patient = user_result.scalar_one_or_none()

            patient_list.append({
                "appointment_id": app.id,
                "patient_name": patient.name if patient else "Unknown",
                "appointment_time": str(app.appointment_time),
                "status": app.status,
                "payment_status": app.payment_status
            })

    return {
        "today_appointments_count": len(today_appointments),
        "completed_appointments_count": completed,
        "cancelled_appointments_count": cancelled,
        "today_patient_list": patient_list
    }
