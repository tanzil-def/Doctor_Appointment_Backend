import os
from fastapi import UploadFile, HTTPException
from app.models.appointment_document import AppointmentDocument
from app.db.session import async_session
from app.utils.permissions import check_role

MEDIA_DIR = "media/appointments"

async def upload_appointment_document(user, appointment_id: int, file: UploadFile, file_type: str):
    check_role(user, ["USER", "DOCTOR"])

    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    os.makedirs(MEDIA_DIR, exist_ok=True)
    file_path = os.path.join(MEDIA_DIR, f"{appointment_id}_{file.filename}")

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    file_url = f"/{MEDIA_DIR}/{appointment_id}_{file.filename}"

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

    return doc

async def get_appointment_documents(user, appointment_id: int):
    check_role(user, ["USER", "DOCTOR"])

    async with async_session() as session:
        result = await session.execute(
            AppointmentDocument.__table__.select().where(
                AppointmentDocument.appointment_id == appointment_id
            )
        )
        documents = result.scalars().all()

    return documents
