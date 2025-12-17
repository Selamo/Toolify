from fastapi import HTTPException, UploadFile, File, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.config import supabase
from supabase import Client

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
# CRITICAL: HTTPBearer is used to extract the Bearer token from the Authorization header
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # CRITICAL: Validates the token with Supabase Auth and retrieves the user
        response = supabase.auth.get_user(token)
        if not response or not response.user:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Return the user object which has .id property
        return response.user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_user_supabase_client(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Client:
    """
    Creates a Supabase client authenticated with the user's token.
    This ensures RLS policies are respected.
    """
    token = credentials.credentials
    try:
        # Create a new client with the user's token
        # We use the ANON key + the user's Bearer token
        from app.config import settings
        from supabase import create_client
        
        client = create_client(
            settings.supabase_url, 
            settings.supabase_anon_key,
            options={
                "global": {
                    "headers": {
                        "Authorization": f"Bearer {token}"
                    }
                }
            }
        )
        return client
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not create authenticated client: {str(e)}",
        )
