from fastapi import HTTPException, UploadFile, File
from typing import Optional

def image_file_validator(file: UploadFile = File(...)):
    """
    Dependency to validate that an uploaded file is an image.
    Used for required file uploads.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not an image.")
    return file

def optional_image_file_validator(file: Optional[UploadFile] = File(None)):
    """
    Dependency to validate that an optional uploaded file, if present, is an image.
    Used for optional file uploads.
    """
    if file and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not an image.")
    return file
