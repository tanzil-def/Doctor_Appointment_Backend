import asyncio
from sqlalchemy.future import select
from app.db.session import async_session
from app.models.user import User
from app.core.security import get_password_hash

async def create_admin():
    async with async_session() as session:
        
        result = await session.execute(select(User).where(User.role == "ADMIN"))
        admin_exists = result.scalar_one_or_none()
        if admin_exists:
            print("Admin already exists")
            return

        
        admin = User(
            name="Admin",
            email="admin@gmail.com",  
            password=get_password_hash("admin123"), 
            role="ADMIN",
        )
        session.add(admin)
        await session.commit()
        print("Admin created successfully")

if __name__ == "__main__":
    asyncio.run(create_admin())
