from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from app.schemas.auth import TokenResponse
from app.models.user import GenderEnum
from app.services.auth_service import register_user, login_user
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse)
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str | None = Form(None),
    dob: str | None = Form(None),
    gender: str | None = Form(None),
    image: UploadFile | None = File(None)
):
    gender_enum = None
    if gender:
        try:
            gender_enum = GenderEnum(gender.capitalize())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid gender value")

    image_url = None
    if image:
        os.makedirs("media/users", exist_ok=True)
        path = f"media/users/{email}_{image.filename}"
        with open(path, "wb") as f:
            f.write(await image.read())
        image_url = f"/media/users/{email}_{image.filename}"

    user = await register_user(
        name=name,
        email=email,
        password=password,
        phone=phone,
        dob=dob,
        gender=gender_enum,
        image_url=image_url
    )

    token, _ = await login_user(email, password)
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "message": "Successfully registered"
    }

@router.post("/login", response_model=TokenResponse)
async def login(email: str = Form(...), password: str = Form(...)):
    token, user = await login_user(email, password)
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }
