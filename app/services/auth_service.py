from app.models.user import User
from app.db.session import async_session
from sqlalchemy import select
from passlib.hash import argon2
from fastapi import HTTPException
from app.core.security import create_access_token
from datetime import datetime

async def register_user(name, email, password, phone=None, dob=None, gender=None, image_url=None):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Email already registered")

        dob_date = None
        if dob:
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()

        user = User(
            name=name,
            email=email,
            password=argon2.hash(password),
            phone=phone,
            dob=dob_date,
            gender=gender,
            image_url=image_url,
            role="USER"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def login_user(email, password):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        try:
            if not argon2.verify(password, user.password):
                raise HTTPException(status_code=401, detail="Invalid email or password")
        except Exception:
            # Catch malformed hash for old users
            raise HTTPException(status_code=401, detail="Password verification failed")

        token = create_access_token({"user_id": user.id, "role": user.role})
        return token, user
