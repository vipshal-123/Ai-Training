from langgraph.graph import StateGraph, END
from backend.rag.retriever import retrieve_resources
from backend.prompt.prompt import UPSKILL_RECOMMENDATION_PROMPT
from backend.llm.tavily import search_learning_resources
from backend.llm.gemini import gemini_chat
from typing import TypedDict
from backend.utils.parsers import parse_gemini_response

class UpskillState(TypedDict):
    offer_components: dict
    acceptance_prediction: dict
    onboarding_resources: dict

def recommend_upskill(state: UpskillState) -> UpskillState:
    resources = [
        {"title": "Java Backend Developer Roadmap", "url": "https://roadmap.sh/backend"},
        {"title": "AWS Training", "url": "https://aws.amazon.com/training/"},
        {"title": "OWASP Top 10", "url": "https://owasp.org/www-project-top-ten/"}
    ]
    prompt = UPSKILL_RECOMMENDATION_PROMPT.format(
        offer=state["offer_components"],
        resources=resources
    )
    response = gemini_chat(prompt)
    parsed = parse_gemini_response(response)
    return {**state, "onboarding_resources": parsed}

def build_upskill_graph():
    builder = StateGraph(UpskillState)
    builder.add_node("recommend_upskill", recommend_upskill)
    builder.set_entry_point("recommend_upskill")
    builder.add_edge("recommend_upskill", END)
    return builder.compile()
