from sqlalchemy import select
from fastapi import HTTPException
from app.db.session import async_session
from app.models.user import User
from app.models.token import RefreshToken
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token

async def register_user(name, email, password, **kwargs):
    async with async_session() as session:
        if await session.scalar(select(User).where(User.email == email)):
            raise HTTPException(400, "Email already exists")
        user = User(
            name=name,
            email=email,
            password=get_password_hash(password),
            role="USER",
            **kwargs
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def login_user(email: str, password: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.email == email))
        if not user or not verify_password(password, user.password):
            raise HTTPException(401, "Invalid credentials")
        access = create_access_token(user.id, user.role)
        refresh = create_refresh_token(user.id)
        session.add(RefreshToken(user_id=user.id, token=refresh))
        await session.commit()
        return access, refresh, user

async def logout_user(refresh_token: str):
    async with async_session() as session:
        token = await session.scalar(select(RefreshToken).where(RefreshToken.token == refresh_token))
        if token:
            token.is_revoked = True
            await session.commit()
