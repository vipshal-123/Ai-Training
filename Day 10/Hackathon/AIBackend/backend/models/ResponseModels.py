from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    message: str

class CandidateResponse(BaseModel):
    id: str
    name: str
    position: str
    acceptance_probability: int
    status: str
    risk_level: str
    upload_date: str

class AnalysisResponse(BaseModel):
    offer_analysis: Dict[str, Any]
    candidate_preference: Dict[str, Any]
    acceptance_likelihood: Dict[str, Any]
    upskill_recommendations: List[Dict[str, Any]]

class DashboardStats(BaseModel):
    total_candidates: int
    avg_acceptance_rate: float
    high_confidence_count: int
    high_risk_count: int

class ProcessingStatus(BaseModel):
    status: str
    current_step: str
    progress: int
    estimated_time: str

class DocumentProcessingRequest(BaseModel):
    resume_file_id: str
    offer_file_id: str
