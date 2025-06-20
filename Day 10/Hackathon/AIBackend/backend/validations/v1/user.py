from pydantic import BaseModel
from typing import Optional
from beanie import PydanticObjectId


class SignupFormValue(BaseModel):
    id_token: str
    email: Optional[str] = None
    name: Optional[str]  = None
    profilePic: Optional[str]  = None
    email_verified: bool = False

