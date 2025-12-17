from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from app.models.user import GenderEnum
from app.services.user_service import get_user_profile, update_user_profile
from app.services.appointment_service import create_appointment, list_user_appointments, cancel_appointment
from app.services.document_service import upload_appointment_document
from app.services.payment_service import create_payment
from app.schemas.user import UserUpdate, UserResponse
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.schemas.document import AppointmentDocumentResponse
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.core.dependencies import role_guard
import os

router = APIRouter(prefix="/user", tags=["User"])


# ----------------------- USER PROFILE -----------------------
@router.get("/profile", response_model=UserResponse)
async def profile(current_user=Depends(role_guard("USER"))):
    user = await get_user_profile(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    name: str | None = Form(None),
    phone: str | None = Form(None),
    dob: str | None = Form(None),
    gender: str | None = Form(None),
    image: UploadFile | None = File(None),
    current_user=Depends(role_guard("USER"))
):
    image_url = None
    if image:
        upload_dir = "media/users"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{current_user.id}_{image.filename}")
        with open(file_path, "wb") as f:
            f.write(await image.read())
        image_url = f"/media/users/{current_user.id}_{image.filename}"

    gender_enum = None
    if gender:
        gender_clean = gender.strip().lower()
        mapping = {
            "male": GenderEnum.MALE,
            "female": GenderEnum.FEMALE,
            "other": GenderEnum.OTHER
        }
        if gender_clean not in mapping:
            raise HTTPException(status_code=400, detail="Invalid gender value")
        gender_enum = mapping[gender_clean]

    data = UserUpdate(
        name=name,
        phone=phone,
        dob=dob,
        gender=gender_enum,
        image_url=image_url
    )

    updated_user = await update_user_profile(current_user.id, data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


# ----------------------- APPOINTMENTS -----------------------
@router.post("/appointments", response_model=AppointmentResponse)
async def book_appointment(
    data: AppointmentCreate,
    current_user=Depends(role_guard("USER"))
):
    return await create_appointment(
        current_user,
        data.doctor_id,
        data.appointment_date,
        data.appointment_time
    )


@router.get("/appointments", response_model=list[AppointmentResponse])
async def my_appointments(
    skip: int = 0,
    limit: int = 10,
    current_user=Depends(role_guard("USER"))
):
    return await list_user_appointments(current_user, skip, limit)


@router.post("/appointments/{id}/cancel", response_model=AppointmentResponse)
async def cancel(id: int, current_user=Depends(role_guard("USER"))):
    return await cancel_appointment(current_user, id)


# ----------------------- DOCUMENT UPLOAD -----------------------
@router.post("/appointments/{id}/documents", response_model=AppointmentDocumentResponse)
async def upload_docs(
    id: int,
    file: UploadFile = File(...),
    file_type: str = Form(...),
    current_user=Depends(role_guard("USER"))
):
    """
    Upload a document for a user appointment.
    - file: actual file
    - file_type: IMAGE, PDF etc.
    """
    doc = await upload_appointment_document(
        user=current_user,
        appointment_id=id,
        file=file,
        file_type=file_type
    )
    return doc


# ----------------------- PAYMENTS -----------------------
@router.post("/payments", response_model=PaymentResponse)
async def make_payment(
    data: PaymentCreate,
    current_user=Depends(role_guard("USER"))
):
    return await create_payment(
        current_user,
        data.appointment_id,
        data.amount,
        data.method
    )
