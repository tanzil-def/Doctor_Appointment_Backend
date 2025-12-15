from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from app.models.user import GenderEnum
from app.services.user_service import get_user_profile, update_user_profile
from app.services.appointment_service import (
    create_appointment,
    list_user_appointments,
    cancel_appointment,
)
from app.services.document_service import upload_document
from app.services.payment_service import create_payment
from app.schemas.user import UserUpdate, UserResponse
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.schemas.document import AppointmentDocumentCreate, AppointmentDocumentResponse
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.core.dependencies import get_current_active_user
import os

router = APIRouter(prefix="/user", tags=["User"])

# ------------------- PROFILE -------------------
@router.get("/profile", response_model=UserResponse)
async def profile(current_user=Depends(get_current_active_user)):
    """
    Get current logged-in user profile
    """
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
    current_user=Depends(get_current_active_user)
):
    """
    Update user profile with optional image upload.
    Use form-data for PATCH request if image is included.
    """

    # Handle image upload
    image_url = None
    if image:
        upload_dir = "media/users"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{current_user.id}_{image.filename}")
        with open(file_path, "wb") as f:
            f.write(await image.read())
        image_url = f"/media/users/{current_user.id}_{image.filename}"

    # Normalize gender input
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

    # Prepare update model
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


# ------------------- APPOINTMENTS -------------------
@router.post("/appointments", response_model=AppointmentResponse)
async def book_appointment(
    data: AppointmentCreate,
    current_user=Depends(get_current_active_user)
):
    return await create_appointment(
        current_user,
        data.doctor_id,
        data.appointment_date,
        data.appointment_time
    )


@router.get("/appointments", response_model=list[AppointmentResponse])
async def my_appointments(current_user=Depends(get_current_active_user)):
    return await list_user_appointments(current_user)


@router.post("/appointments/{id}/cancel", response_model=AppointmentResponse)
async def cancel(id: int, current_user=Depends(get_current_active_user)):
    return await cancel_appointment(current_user, id)


@router.post("/appointments/{id}/documents", response_model=AppointmentDocumentResponse)
async def upload_docs(
    id: int,
    data: AppointmentDocumentCreate,
    current_user=Depends(get_current_active_user)
):
    return await upload_document(
        user=current_user,
        appointment_id=id,
        uploaded_by="USER",
        file_url=data.file_url,
        file_type=data.file_type
    )


# ------------------- PAYMENTS -------------------
@router.post("/payments", response_model=PaymentResponse)
async def make_payment(
    data: PaymentCreate,
    current_user=Depends(get_current_active_user)
):
    return await create_payment(
        current_user,
        data.appointment_id,
        data.amount,
        data.method
    )
