from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.core.security import decode_token
from app.services.user_service import get_user_by_id

security = HTTPBearer()


def role_guard(required_role: str):
    async def _guard(credentials=Depends(security)):
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise HTTPException(401, "Invalid token type")
        if payload.get("role") != required_role:
            raise HTTPException(403, "Permission denied")
        user = await get_user_by_id(int(payload["sub"]))
        if not user:
            raise HTTPException(404, "User not found")
        return user
    return _guard


async def get_current_active_user(credentials=Depends(security)):
    payload = decode_token(credentials.credentials)
    if payload.get("role") != "USER":
        raise HTTPException(401, "Invalid role")
    user = await get_user_by_id(int(payload.get("sub")))
    if not user:
        raise HTTPException(404, "User not found")
    return user


async def get_current_doctor(credentials=Depends(security)):
    payload = decode_token(credentials.credentials)
    if payload.get("role") != "DOCTOR":
        raise HTTPException(401, "Invalid role")
    user = await get_user_by_id(int(payload.get("sub")))
    if not user:
        raise HTTPException(404, "Doctor profile not found")
    return user


async def get_current_admin(credentials=Depends(security)):
    payload = decode_token(credentials.credentials)
    if payload.get("role") != "ADMIN":
        raise HTTPException(401, "Invalid role")
    user = await get_user_by_id(int(payload.get("sub")))
    if not user:
        raise HTTPException(404, "Admin not found")
    return user

