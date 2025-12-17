from app.db.session import async_session
from sqlalchemy import select
from app.models.user import User
from typing import Optional
from fastapi import HTTPException
from datetime import datetime


def parse_dob(dob: str | None):
    if not dob:
        return None
    try:
        return datetime.strptime(dob, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="DOB must be in YYYY-MM-DD format")


async def get_user_by_id(user_id: int) -> Optional[User]:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


async def get_user_by_email(email: str) -> Optional[User]:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()


async def get_user_profile(user_id: int) -> dict | None:
    user = await get_user_by_id(user_id)
    if not user:
        return None
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "dob": user.dob.isoformat() if user.dob else None,
        "role": user.role,
        "gender": user.gender,
        "image_url": user.image_url,
        "is_active": user.is_active
    }


async def update_user_profile(user_id: int, data) -> dict | None:
    """
    `data` is expected to be a Pydantic UserUpdate model.
    """
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None

        update_data = data.model_dump(exclude_unset=True)

        # Convert dob string to date
        if "dob" in update_data and update_data["dob"]:
            update_data["dob"] = parse_dob(update_data["dob"])

        for key, value in update_data.items():
            setattr(user, key, value)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "dob": user.dob.isoformat() if user.dob else None,
            "role": user.role,
            "gender": user.gender,
            "image_url": user.image_url,
            "is_active": user.is_active
        }
