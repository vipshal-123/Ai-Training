from beanie import Document, PydanticObjectId
from typing import List
from bson import ObjectId 
from typing import Optional
from datetime import datetime, timezone
from pydantic import Field
from enum import Enum
from backend.models.AnalysisResult import PyObjectId


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CandidateStatus(str, Enum):
    PENDING = "pending"
    REVIEW = "review"
    APPROVED = "approved"
    REJECTED = "rejected"

class Candidate(Document):
    offer_analysis: dict
    preference_alignment: dict
    # userId= Optional[PydanticObjectId] = None,
    acceptance_prediction: dict
    upskill_recommendations: dict
    dashboard_summary: dict
    status: str
    candidate_id: str
    
    class Settings:
        name = "candidate"
    
    # class Config:
    #     validate_by_name = True
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}