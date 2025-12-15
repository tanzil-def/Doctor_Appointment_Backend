from sqlalchemy import Column, BigInteger, Numeric, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger, primary_key=True)
    appointment_id = Column(BigInteger, ForeignKey("appointments.id", ondelete="CASCADE"), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    method = Column(String(20))
    status = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
