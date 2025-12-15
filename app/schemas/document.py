from pydantic import BaseModel
from app.models.enums import DocumentUploader, FileType

class AppointmentDocumentCreate(BaseModel):
    file_url: str
    file_type: FileType

class AppointmentDocumentResponse(BaseModel):
    id: int
    appointment_id: int
    uploaded_by: DocumentUploader
    file_url: str
    file_type: FileType

    class Config:
        orm_mode = True
