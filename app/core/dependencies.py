from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.user_service import get_user_by_id
from app.services.doctor_service import get_doctor_by_id
from app.models.user import User
from app.core.security import decode_access_token

security = HTTPBearer()

async def get_current_active_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    payload = decode_access_token(credentials.credentials)
    if payload.get("role") != "USER":
        raise HTTPException(status_code=401, detail="Invalid role")
    
    user_id = payload.get("sub")
    user = await get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_doctor(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_access_token(credentials.credentials)
    if payload.get("role") != "DOCTOR":
        raise HTTPException(status_code=401, detail="Invalid role")
    
    user_id = payload.get("sub")
    doctor = await get_doctor_by_id(int(user_id))
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_access_token(credentials.credentials)
    if payload.get("role") != "ADMIN":
        raise HTTPException(status_code=401, detail="Invalid role")
    
    user_id = payload.get("sub")
    admin = await get_user_by_id(int(user_id))
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin
