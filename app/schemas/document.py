from pydantic import BaseModel
from enum import Enum

class FileType(str, Enum):
    IMAGE = "IMAGE"
    PDF = "PDF"
    OTHER = "OTHER"

# Response schema
class AppointmentDocumentResponse(BaseModel):
    id: int
    appointment_id: int
    uploaded_by: str
    file_url: str
    file_type: FileType

    model_config = {
        "from_attributes": True  # V2: orm_mode replacement
    }

# Upload request schema
class AppointmentDocumentUploadRequest(BaseModel):
    file_type: FileType

    model_config = {
        "from_attributes": True
    }

# Alias previous name for backward compatibility
AppointmentDocumentCreate = AppointmentDocumentUploadRequest
