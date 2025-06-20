from langgraph.graph import StateGraph, END
from backend.prompt.prompt import PLACEMENT_DASHBOARD_PROMPT
from backend.llm.gemini import gemini_chat
from typing import TypedDict, List, Dict
import re
import json

class DashboardAgentState(TypedDict):
    acceptance_predictions: List[Dict]
    onboarding_resources: Dict[str, List[Dict]] 
    dashboard_summary: Dict
    
def parse_gemini_response(response) -> dict:
    """Safely parse Gemini LLM output into a dict."""
    # Extract string content from AIMessage or string
    text = (
        response.text if hasattr(response, "text")
        else response.content if hasattr(response, "content")
        else str(response)
    )
    
    try:
        # Remove triple backticks and language labels
        cleaned = re.sub(r"```(?:json|python)?", "", text).strip("`\n ")
        # If it's a full assignment like job_offer_details = {...}, extract the {...}
        if "=" in cleaned and "{" in cleaned:
            cleaned = cleaned.split("=", 1)[-1]
        return json.loads(cleaned)
    except Exception as e:
        return {"error": str(e), "raw": text}
    
def generate_dashboard(state: DashboardAgentState) -> DashboardAgentState:
    prompt = PLACEMENT_DASHBOARD_PROMPT.format(
        predictions=state["acceptance_predictions"],
        onboarding_resources=state["onboarding_resources"]
    )

    response = gemini_chat(prompt)

    try:
        dashboard_data = parse_gemini_response(response)
    except Exception as e:
        dashboard_data = {"error": str(e)}

    return {**state, "dashboard_summary": dashboard_data}

def build_dashboard_agent_graph():
    builder = StateGraph(DashboardAgentState)
    builder.add_node("generate_dashboard", generate_dashboard)
    builder.set_entry_point("generate_dashboard")
    builder.add_edge("generate_dashboard", END)
    return builder.compile()
