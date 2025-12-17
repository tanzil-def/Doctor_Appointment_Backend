# app/services/appointment_service.py
from fastapi import HTTPException
from sqlalchemy import select, and_
from app.models.appointment import Appointment
from app.models.enums import AppointmentStatus, PaymentStatus
from app.models.doctor import Doctor
from app.models.appointment_document import AppointmentDocument
from app.db.session import async_session
from app.utils.permissions import check_role

# -------------------
# Appointment CRUD
# -------------------

async def create_appointment(user, doctor_id: int, appointment_date, appointment_time):
    check_role(user, ["USER"])

    async with async_session() as session:
        # Check if slot already booked
        stmt = select(Appointment).where(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == appointment_date,
                Appointment.appointment_time == appointment_time
            )
        )
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Slot already booked")

        # Create appointment
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

        # Get doctor info
        stmt_doc = select(Doctor).where(Doctor.id == doctor_id)
        res_doc = await session.execute(stmt_doc)
        doctor = res_doc.scalar_one_or_none()

        return {
            "id": appointment.id,
            "doctor_id": doctor_id,
            "doctor_name": doctor.user.name if doctor else "Unknown",
            "appointment_date": appointment.appointment_date.isoformat(),
            "appointment_time": appointment.appointment_time.isoformat(),
            "status": appointment.status,
            "payment_status": appointment.payment_status
        }

async def list_user_appointments(user, skip: int = 0, limit: int = 10):
    check_role(user, ["USER"])

    async with async_session() as session:
        stmt = select(Appointment).where(Appointment.user_id == user.id).offset(skip).limit(limit)
        result = await session.execute(stmt)
        appointments = result.scalars().all()

        response = []
        for appt in appointments:
            stmt_doc = select(Doctor).where(Doctor.id == appt.doctor_id)
            res_doc = await session.execute(stmt_doc)
            doctor = res_doc.scalar_one_or_none()
            response.append({
                "id": appt.id,
                "doctor_id": appt.doctor_id,
                "doctor_name": doctor.user.name if doctor else "Unknown",
                "appointment_date": appt.appointment_date.isoformat(),
                "appointment_time": appt.appointment_time.isoformat(),
                "status": appt.status,
                "payment_status": appt.payment_status
            })
        return response

async def list_doctor_appointments(user):
    check_role(user, ["DOCTOR"])

    async with async_session() as session:
        stmt = select(Appointment).where(Appointment.doctor_id == user.doctor.id)
        result = await session.execute(stmt)
        appointments = result.scalars().all()
        return [
            {
                "id": appt.id,
                "user_id": appt.user_id,
                "appointment_date": appt.appointment_date.isoformat(),
                "appointment_time": appt.appointment_time.isoformat(),
                "status": appt.status,
                "payment_status": appt.payment_status
            } for appt in appointments
        ]

async def cancel_appointment(user, appointment_id: int):
    check_role(user, ["USER"])

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

        # Get doctor info
        stmt_doc = select(Doctor).where(Doctor.id == appointment.doctor_id)
        res_doc = await session.execute(stmt_doc)
        doctor = res_doc.scalar_one_or_none()

        return {
            "id": appointment.id,
            "doctor_id": appointment.doctor_id,
            "doctor_name": doctor.user.name if doctor else "Unknown",
            "appointment_date": appointment.appointment_date.isoformat(),
            "appointment_time": appointment.appointment_time.isoformat(),
            "status": appointment.status,
            "payment_status": appointment.payment_status
        }

# -------------------
# Appointment Documents
# -------------------

async def get_appointment_documents(user, appointment_id: int):
    check_role(user, ["USER", "DOCTOR"])

    async with async_session() as session:
        stmt = select(AppointmentDocument).where(AppointmentDocument.appointment_id == appointment_id)
        result = await session.execute(stmt)
        documents = result.scalars().all()
        return [
            {
                "id": doc.id,
                "appointment_id": doc.appointment_id,
                "uploaded_by": doc.uploaded_by,
                "file_url": doc.file_url,
                "file_type": doc.file_type
            } for doc in documents
        ]

async def upload_appointment_document(user, appointment_id: int, file_url: str, file_type: str):
    check_role(user, ["USER", "DOCTOR"])

    async with async_session() as session:
        doc = AppointmentDocument(
            appointment_id=appointment_id,
            uploaded_by=user.role,
            file_url=file_url,
            file_type=file_type
        )
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
        return {
            "id": doc.id,
            "appointment_id": doc.appointment_id,
            "uploaded_by": doc.uploaded_by,
            "file_url": doc.file_url,
            "file_type": doc.file_type
        }
