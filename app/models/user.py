from sqlalchemy import Column, BigInteger, String, Boolean, Date, TIMESTAMP, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class UserRole(str, enum.Enum):
    USER = "USER"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    phone = Column(String(20))
    dob = Column(Date)
    image_url = Column(String)
    gender = Column(Enum(GenderEnum), default=GenderEnum.OTHER)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    doctor = relationship("Doctor", back_populates="user", uselist=False, cascade="all, delete", lazy="selectin")
