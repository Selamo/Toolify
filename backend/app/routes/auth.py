from fastapi import APIRouter, HTTPException, Depends
from app.config import supabase
from app.dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["Auth"])

@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    """
    Verifies the authentication token and returns the user's profile.
    This endpoint is used to confirm that the backend can correctly validate
    tokens issued by Clerk (via Supabase Native Integration).
    """
    return {
        "user_id": user.id,
        "email": user.email,
        "message": "Backend authentication successful"
    }
    email = creds.email
    password = creds.password
    full_name = creds.full_name
    user_id = None
    is_new_user = False

    try:
        # 1. First, try to sign in (handles existing users)
        try:
            # CRITICAL: Attempts to sign in the user with Supabase to get a session token
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user and res.session:
                # User exists and authenticated successfully
                return TokenResponse(access_token=res.session.access_token)
        except Exception as signin_err:
            # Sign in failed, user likely doesn't exist
            print(f"Sign in failed: {signin_err}")
            pass

        # 2. User doesn't exist, create via Admin API
        try:
            attributes = {
                "email": email,
                "password": password,
                "email_confirm": True,
                "user_metadata": {"full_name": full_name}
            }
            user_response = supabase.auth.admin.create_user(attributes)
            if user_response.user:
                user_id = user_response.user.id
                is_new_user = True
        except Exception as admin_err:
            raise HTTPException(
                status_code=400, 
                detail=f"Could not create user. They may exist but password is incorrect: {str(admin_err)}"
            )

        # 3. Create profile for new user only
        if is_new_user and user_id:
            try:
                supabase.table("profiles").insert({
                    "id": str(user_id),
                    "full_name": full_name,
                    "avatar_url": None
                }).execute()
            except Exception as e:
                # Profile might already exist, that's ok
                print(f"Profile creation warning: {e}")

        # 4. Sign in the newly created user and return token
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.session:
            return TokenResponse(access_token=res.session.access_token)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth process failed: {str(e)}")
    
    raise HTTPException(status_code=500, detail="Could not retrieve token")
