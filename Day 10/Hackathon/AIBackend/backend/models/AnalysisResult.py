from beanie import Document
from typing import List
from bson import ObjectId 
from typing import Optional
from datetime import datetime, timezone
from pydantic import Field
from enum import Enum

class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        from pydantic import GetCoreSchemaHandler
        from pydantic_core import core_schema

        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

        
class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class AcceptanceLikelihood(Document):
    probability: int
    confidence: int
    risk_factors: List[str]
    positive_factors: List[str]
    
class OfferAnalysis(Document):
    position: str
    salary: str
    location: str
    benefits: List[str]
    start_date: str
    company: Optional[str] = None
    additional_perks: Optional[List[str]] = []
    

class UpskillRecommendation(Document):
    skill: str
    priority: Priority
    resources: int
    description: Optional[str] = None
    estimated_time: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
class CandidatePreference(Document):
    alignment_score: int
    preferred_salary: str
    location_preference: str
    key_skills: List[str]
    experience_level: Optional[str] = None
    industry_preference: Optional[List[str]] = []

class AnalysisResult(Document):
    candidate_id: Optional[PyObjectId] = None
    offer_analysis: OfferAnalysis
    candidate_preference: CandidatePreference
    acceptance_likelihood: AcceptanceLikelihood
    upskill_recommendations: List[UpskillRecommendation]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "analysis_result"
    
    # class Config:
    #     validate_by_name = True
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}