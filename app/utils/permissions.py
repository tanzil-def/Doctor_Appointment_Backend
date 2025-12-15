from fastapi import HTTPException

def check_role(user_role: str, allowed_roles: list[str]):
    """
    Centralized role/permission check.
    Raises HTTP 403 if role not allowed.
    """
    if user_role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Permission denied")
