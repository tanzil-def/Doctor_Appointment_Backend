import asyncio
from sqlalchemy import update
from app.db.session import async_session
from app.core.security import get_password_hash

NEW_PASSWORD = "1234"

async def main():
    
    from app.models.user import User

    async with async_session() as session:
        stmt = update(User).values(password=get_password_hash(NEW_PASSWORD))
        await session.execute(stmt)
        await session.commit()
        print(" All users password reset to '1234'")

if __name__ == "__main__":
    asyncio.run(main())
