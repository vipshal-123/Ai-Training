import os
from backend.models.User import User
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from uuid import uuid4 as uuid
from backend.utils.jwt import generate_jwt_token
from dotenv import load_dotenv
from backend.utils.verifyGoogleToken import verify_google_token
load_dotenv("local.env")

async def signin(signin_data):
    if not os.getenv("GOOGLE_CLIENT_ID"):
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    
    google_user = verify_google_token(signin_data.id_token)
    
    if not google_user:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    
    if not google_user.get("email_verified", False):
        raise HTTPException(status_code=401, detail="Email not verified with Google")

    user_email = google_user["email"].lower().strip()
    
    is_user_exists = await User.find_one({"email": user_email})
    
    if not is_user_exists:
        user = User(
            email=user_email,
            name=google_user.get("name") or "",
            profilePic=google_user.get("picture") or "",
            email_verified=True
        )
        await user.save()
        is_user_exists = user

    session_id = str(uuid().hex)

    payload_data = {
        "_id": str(is_user_exists.id),
        "session_id": session_id,
        "email": user_email
    }
        
    access_token = generate_jwt_token(payload_data, "access")
    refresh_token = generate_jwt_token(payload_data, "refresh")
    
    return JSONResponse(
        {
            "success": True,
            "message": "User signed in successfully",
            "token": {"accessToken": access_token, "refreshToken": refresh_token},
            "session": session_id,
            "userId": str(is_user_exists.id)
        },
        status_code=200,
    )