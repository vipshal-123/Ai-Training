from datetime import datetime, timezone
from pydantic import EmailStr
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from typing import Optional
import pymongo


class CandidateReport(Document):
    userId: PydanticObjectId
    offerId: PydanticObjectId
    preferenceId: PydanticObjectId
    report: str
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "candidate_report"
        # indexes = [
        #     pymongo.IndexModel([("deletion_date", 1)], expireAfterSeconds=90*24*60*60)
        # ]
