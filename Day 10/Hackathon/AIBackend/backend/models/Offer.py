from datetime import datetime, timezone
from pydantic import EmailStr
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from typing import Optional
import pymongo


class Offer(Document):
    userId: PydanticObjectId
    job_title: str
    salary: Optional[dict]  = None
    location: str
    joining_date: Optional[datetime] = None
    bond_terms: Optional[str] = None
    acceptance: Optional[int] = 0
    confidence: Optional[int] = 0
    reason: Optional[str] = None
    recommended_courses: Optional[list] = []
    onboarding_resources: Optional[list] = []
    skill_gap_analysis: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "offer"
        # indexes = [
        #     pymongo.IndexModel([("deletion_date", 1)], expireAfterSeconds=90*24*60*60)
        # ]
