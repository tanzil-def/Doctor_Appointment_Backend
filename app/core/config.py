from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    POSTGRES_USER: str = "doctor_appointment"
    POSTGRES_PASSWORD: str = "1234"
    POSTGRES_DB: str = "doctor_appointment_system"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    DATABASE_URL: str | None = Field(default=None, env="DATABASE_URL")

    JWT_SECRET_KEY: str = Field(default="super-secret-key", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Fallback DATABASE_URL if not provided
if not settings.DATABASE_URL:
    settings.DATABASE_URL = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
        f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )
