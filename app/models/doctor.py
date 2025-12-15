from sqlalchemy import Column, BigInteger, String, Integer, Boolean, ForeignKey, TIMESTAMP, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    speciality = Column(String(100), nullable=False)
    experience_years = Column(Integer, nullable=True)
    about = Column(String, nullable=True)
    consultation_fee = Column(Numeric(10,2), nullable=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="doctor")
