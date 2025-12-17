from fastapi import HTTPException
from app.models.user import UserRole

def check_role(user, allowed_roles: list[UserRole]):
    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )
