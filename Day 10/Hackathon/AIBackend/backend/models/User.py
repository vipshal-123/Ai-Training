from datetime import datetime, timezone
from pydantic import EmailStr
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from typing import Optional
import pymongo


class User(Document):
    email: str
    name: Optional[str]  = None
    profilePic: Optional[str]  = None
    email_verified: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        # indexes = [
        #     pymongo.IndexModel([("deletion_date", 1)], expireAfterSeconds=90*24*60*60)
        # ]
