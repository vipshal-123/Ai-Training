from dotenv import load_dotenv
import os
from google.oauth2 import id_token
from google.auth.transport import requests

load_dotenv("local.env")

def verify_google_token(id_token_str: str):
    try:
        id_info = id_token.verify_oauth2_token(
            id_token_str, 
            requests.Request(), 
            audience=os.getenv("GOOGLE_CLIENT_ID") 
        )

        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError("Invalid issuer")

        if id_info['aud'] != os.getenv("GOOGLE_CLIENT_ID"):
            raise ValueError("Invalid audience")

        return {
            "email": id_info.get("email"),
            "name": id_info.get("name"),
            "picture": id_info.get("picture"),
            "email_verified": id_info.get("email_verified", False),
        }

    except ValueError as e:
        print("Token verification error:", str(e))
        return None
    except Exception as e:
        print("Unexpected error during token verification:", str(e))
        return None