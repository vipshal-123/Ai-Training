from langgraph.graph import StateGraph, END
from backend.prompt.prompt import ACCEPTANCE_PREDICTION_PROMPT
from backend.llm.gemini import gemini_chat
from typing import TypedDict
import json
import re
from backend.utils.parsers import parse_gemini_response
from backend.prompt.prompt import ACCEPTANCE_PREDICTION_PROMPT

class AcceptanceState(TypedDict):
    offer_components: dict
    preference_alignment: dict
    placement_history: str
    acceptance_prediction: dict

def predict_acceptance(state: AcceptanceState) -> AcceptanceState:
    prompt = ACCEPTANCE_PREDICTION_PROMPT.format(
        offer=state["offer_components"],
        alignment=state["preference_alignment"],
        trends=state["placement_history"]
    )
    response = gemini_chat(prompt)
    parsed = parse_gemini_response(response)
    return {**state, "acceptance_prediction": parsed}

def build_acceptance_likelihood_graph():
    builder = StateGraph(AcceptanceState)
    builder.add_node("predict_acceptance", predict_acceptance)
    builder.set_entry_point("predict_acceptance")
    builder.add_edge("predict_acceptance", END)
    return builder.compile()
