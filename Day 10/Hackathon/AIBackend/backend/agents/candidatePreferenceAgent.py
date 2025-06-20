from langgraph.graph import StateGraph, END
from backend.utils.parsers import parse_offer_file, parse_resume_file
from backend.prompt.prompt import PREFERENCE_ALIGNMENT_PROMPT
from backend.llm.gemini import gemini_chat
from typing import TypedDict
from backend.utils.parsers import parse_gemini_response

class PreferenceState(TypedDict):
    offer_components: dict
    resume_path: str
    placement_data: str
    preference_alignment: dict

def extract_resume_text(state: PreferenceState) -> PreferenceState:
    resume_text = parse_resume_file(state["resume_path"])
    prompt = PREFERENCE_ALIGNMENT_PROMPT.format(
        offer=state["offer_components"],
        resume=resume_text,
        placement_data=state["placement_data"]
    )
    response = gemini_chat(prompt)
    parsed = parse_gemini_response(response)
    return {**state, "preference_alignment": parsed}

def build_candidate_preference_graph():
    builder = StateGraph(PreferenceState)
    builder.add_node("extract_resume", extract_resume_text)
    builder.set_entry_point("extract_resume")
    builder.add_edge("extract_resume", END)
    return builder.compile()
