from langgraph.graph import StateGraph, END
from .state import GraphState

# Import agent functions
from app.agents.profile_insight import extract_profile_insights
from app.agents.recruiter_language_optimizer import optimize_with_rag
from app.agents.pitch_generator import generate_elevator_pitch
from app.agents.pitch_review import review_and_approve

def build_langgraph() -> StateGraph:
    builder = StateGraph(GraphState)

    # Add nodes (agents)
    builder.add_node("profile_insight", extract_profile_insights)
    builder.add_node("rag_optimizer", optimize_with_rag)
    builder.add_node("pitch_generator", generate_elevator_pitch)
    builder.add_node("pitch_review", review_and_approve)

    # Define flow
    builder.set_entry_point("profile_insight")
    builder.add_edge("profile_insight", "rag_optimizer")
    builder.add_edge("rag_optimizer", "pitch_generator")
    builder.add_edge("pitch_generator", "pitch_review")
    builder.add_edge("pitch_review", END)

    return builder.compile()
