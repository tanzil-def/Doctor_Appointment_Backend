from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Async Engine
engine = create_async_engine(
    str(settings.DATABASE_URL),  # must be string
    echo=True,
    future=True
)

# Async Session
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
