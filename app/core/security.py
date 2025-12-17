from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- PASSWORD FUNCTIONS ----------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)  # same as before

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)  # same as before

# ---------- TOKEN FUNCTIONS ----------
def _create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,  # CORRECTION: was settings.SECRET_KEY
        algorithm=settings.JWT_ALGORITHM  # CORRECTION: was hardcoded "HS256"
    )

def create_access_token(user_id: int, role: str):
    return _create_token(
        {"sub": str(user_id), "role": role, "type": "access"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # CORRECTION: use settings
    )

def create_refresh_token(user_id: int):
    return _create_token(
        {"sub": str(user_id), "type": "refresh"},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)  # CORRECTION: use settings
    )

def decode_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,  # CORRECTION: was settings.SECRET_KEY
            algorithms=[settings.JWT_ALGORITHM]  # CORRECTION: was hardcoded
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


