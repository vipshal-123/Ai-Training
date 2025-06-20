from datetime import datetime, timezone
from pydantic import EmailStr
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from typing import Optional
import pymongo


class Preference(Document):
    userId: PydanticObjectId
    offerId: PydanticObjectId
    preferred_location: str
    interests: Optional[list]  = []
    skills: Optional[list]  = []
    career_goals: Optional[str] = None
    expected_ctc: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "preference"
        # indexes = [
        #     pymongo.IndexModel([("deletion_date", 1)], expireAfterSeconds=90*24*60*60)
        # ]
