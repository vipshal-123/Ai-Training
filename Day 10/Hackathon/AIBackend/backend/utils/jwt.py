from jwt import decode, ExpiredSignatureError, InvalidTokenError
import jwt
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

security = HTTPBearer()
load_dotenv("local.env")

def generate_jwt_token(payload: dict, token_type: str) -> str:
    to_encode = payload.copy()

    if token_type == "access":
        expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    elif token_type == "refresh":
        expire = datetime.utcnow() + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
    else:
        raise ValueError("Invalid token type. Use 'access' or 'refresh'.")

    to_encode.update({"exp": expire, "type": token_type})
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
    return encoded_jwt

def verify_jwt_token(token: str, token_type: str = "refresh") -> dict:
    try:
        payload = decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        if payload.get("type") != token_type:
            raise InvalidTokenError("Invalid token type.")
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return verify_jwt_token(credentials.credentials)