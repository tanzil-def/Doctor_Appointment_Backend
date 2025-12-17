from fastapi import APIRouter, Form
from app.services.auth_service import register_user, login_user, logout_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str | None = Form(None),
    dob: str | None = Form(None),
    gender: str | None = Form(None),
    image_url: str | None = Form(None)
):
    user = await register_user(
        name=name,
        email=email,
        password=password,
        phone=phone,
        dob=dob,
        gender=gender,
        image_url=image_url
    )
    return {"message": "Registered", "user_id": user.id}

@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    access, refresh, user = await login_user(email, password)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "role": user.role,
        "user_id": user.id
    }

@router.post("/logout")
async def logout(refresh_token: str = Form(...)):
    await logout_user(refresh_token)
    return {"message": "Logged out"}
