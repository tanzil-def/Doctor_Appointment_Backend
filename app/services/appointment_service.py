from fastapi import HTTPException
from sqlalchemy import select, and_

from app.models.appointment import Appointment
from app.models.enums import AppointmentStatus, PaymentStatus
from app.db.session import async_session
from app.utils.permissions import check_role


async def create_appointment(user, doctor_id: int, appointment_date, appointment_time):
    check_role(user.role, ["USER"])

    async with async_session() as session:
        stmt = select(Appointment).where(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == appointment_date,
                Appointment.appointment_time == appointment_time
            )
        )
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=400, detail="Slot already booked")

        appointment = Appointment(
            user_id=user.id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status=AppointmentStatus.BOOKED.value,
            payment_status=PaymentStatus.PENDING.value
        )
        session.add(appointment)
        await session.commit()
        await session.refresh(appointment)
        return appointment


async def list_user_appointments(user):
    check_role(user.role, ["USER"])

    async with async_session() as session:
        stmt = select(Appointment).where(Appointment.user_id == user.id)
        result = await session.execute(stmt)
        return result.scalars().all()


async def list_doctor_appointments(user):
    check_role(user.role, ["DOCTOR"])

    async with async_session() as session:
        stmt = select(Appointment).where(Appointment.doctor_id == user.doctor.id)
        result = await session.execute(stmt)
        return result.scalars().all()


async def cancel_appointment(user, appointment_id: int):
    check_role(user.role, ["USER"])

    async with async_session() as session:
        stmt = select(Appointment).where(
            Appointment.id == appointment_id,
            Appointment.user_id == user.id
        )
        result = await session.execute(stmt)
        appointment = result.scalar_one_or_none()

        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

        appointment.status = AppointmentStatus.CANCELLED.value
        await session.commit()
        await session.refresh(appointment)
        return appointment


async def get_appointment_documents(user, appointment_id: int):
    from app.models.appointment_document import AppointmentDocument

    async with async_session() as session:
        stmt = select(AppointmentDocument).where(
            AppointmentDocument.appointment_id == appointment_id
        )
        result = await session.execute(stmt)
        return result.scalars().all()
