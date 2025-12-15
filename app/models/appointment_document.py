from sqlalchemy import Column, BigInteger, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class AppointmentDocument(Base):
    __tablename__ = "appointment_documents"

    id = Column(BigInteger, primary_key=True)
    appointment_id = Column(BigInteger, ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False)
    uploaded_by = Column(String(20), nullable=False)
    file_url = Column(String, nullable=False)
    file_type = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
