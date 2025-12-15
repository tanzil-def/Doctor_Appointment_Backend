from sqlalchemy import Column, BigInteger, Date, Time, String, ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)

    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(String(20), nullable=False)
    payment_status = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("doctor_id", "appointment_date", "appointment_time", name="uq_doctor_time"),
    )
