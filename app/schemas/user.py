from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import GenderEnum
from datetime import date

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    dob: Optional[str]  # API response as string
    role: str
    gender: Optional[GenderEnum]
    image_url: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True  # Pydantic v2

    @classmethod
    def model_post_init(cls, obj):
        """
        Convert `dob` to ISO string if it's a date object.
        This ensures None or string are safe.
        """
        if hasattr(obj, "dob") and isinstance(obj.dob, date):
            obj.dob = obj.dob.isoformat()


class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    dob: Optional[str]  # input string, convert in service
    image_url: Optional[str]
    gender: Optional[GenderEnum]

    class Config:
        from_attributes = True
