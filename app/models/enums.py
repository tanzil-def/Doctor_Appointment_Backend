import enum

class UserRole(str, enum.Enum):
    USER = "USER"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"


class AppointmentStatus(str, enum.Enum):
    BOOKED = "BOOKED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    REFUNDED = "REFUNDED"


class DocumentUploader(str, enum.Enum):
    USER = "USER"
    DOCTOR = "DOCTOR"


class FileType(str, enum.Enum):
    IMAGE = "IMAGE"
    PDF = "PDF"

