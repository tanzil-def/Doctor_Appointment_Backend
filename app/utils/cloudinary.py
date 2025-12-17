import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import UploadFile
from typing import Optional

# Cloudinary configuration
cloudinary.config(
    cloud_name="YOUR_CLOUD_NAME",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    secure=True
)

async def upload_file(file: UploadFile, folder: str = "default") -> str:
    """
    Uploads a file to Cloudinary and returns the secure URL.
    """
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder=folder,
            use_filename=True,
            unique_filename=True,
            overwrite=False
        )
        return result.get("secure_url")
    except Exception as e:
        raise Exception(f"File upload failed: {str(e)}")
