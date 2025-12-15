from app.models.appointment_document import AppointmentDocument
from app.db.session import async_session
from app.utils.permissions import check_role


async def upload_document(user, appointment_id: int, uploaded_by: str, file_url: str, file_type: str):
    check_role(user.role, ["USER", "DOCTOR"])

    async with async_session() as session:
        doc = AppointmentDocument(
            appointment_id=appointment_id,
            uploaded_by=uploaded_by,
            file_url=file_url,
            file_type=file_type
        )
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
        return doc


async def list_documents(user, appointment_id: int):
    async with async_session() as session:
        stmt = AppointmentDocument.__table__.select().where(
            AppointmentDocument.appointment_id == appointment_id
        )
        result = await session.execute(stmt)
        return result.scalars().all()
