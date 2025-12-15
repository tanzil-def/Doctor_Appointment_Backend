from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.session import async_session
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token



async def register_user(name, email, password, phone=None, dob=None, gender=None, image_url=None):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        
        user = User(
            name=name,
            email=email,
            password=get_password_hash(password),
            role="USER",
            phone=phone,
            dob=dob,
            gender=gender,
            image_url=image_url
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user



async def login_user(email, password):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        
        token = create_access_token({"sub": str(user.id), "role": user.role})
        return token, user
