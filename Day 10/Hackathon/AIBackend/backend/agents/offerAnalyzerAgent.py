from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from backend.utils.parsers import parse_offer_file
from backend.prompt.prompt import OFFER_EXTRACTION_PROMPT
from backend.llm.gemini import gemini_chat
from typing import TypedDict
import re
import json
from backend.utils.parsers import parse_gemini_response

class OfferState(TypedDict):
    file_path: str
    offer_components: dict

def extract_offer_text(state: OfferState) -> OfferState:
    raw_text = parse_offer_file(state["file_path"])
    response = gemini_chat(OFFER_EXTRACTION_PROMPT.format(offer_text=raw_text))
    parsed = parse_gemini_response(response)
    return {**state, "offer_components": parsed}

def build_offer_analyzer_graph():
    builder = StateGraph(OfferState)
    builder.add_node("extract_text", extract_offer_text)
    builder.set_entry_point("extract_text")
    builder.add_edge("extract_text", END)
    return builder.compile()