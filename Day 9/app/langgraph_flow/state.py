# Shared state structure for LangGraph
from typing import TypedDict, Optional, Dict, Any


class GraphState(TypedDict):
    resume_text: Optional[str]
    profile_insights: Optional[str]
    recruiter_context: Optional[str]
    optimized_pitch: Optional[str]
    final_pitch: Optional[str]
    metadata: Dict[str, Any]
