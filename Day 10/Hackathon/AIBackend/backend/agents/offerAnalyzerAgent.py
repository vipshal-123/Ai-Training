import json
from backend.utils.parsers import extract_text_from_pdf
from backend.llm.gemini import model
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentType(TypedDict):
    offer_text: str
    offer_analysis: dict

def offer_analyzer_agent(state: AgentType) -> AgentType:
    offer_text = state["offer_text"]
    prompt = f"""
    You are an HR assistant. Extract structured information from the following job offer letter:

    Text:
    {offer_text}

    Return in JSON format with fields:
    - job_title
    - salary
    - location
    - joining_date
    - bond_terms
    """
    response = model.generate_content(prompt)
    
    return {"offer_analysis": response.text}

def build_graph():
    builder = StateGraph(AgentType)


    builder.add_node("OfferAnalyzer", offer_analyzer_agent)
    builder.set_entry_point("OfferAnalyzer")
    builder.set_finish_point("OfferAnalyzer")
    return builder.compile()


offer_graph = build_graph()

def run_offer_analyze_agent(offer_path: str) -> dict:
    offer_text = extract_text_from_pdf(offer_path)

    result = offer_graph.invoke({"offer_text": offer_text})

    json_string = result["offer_analysis"].strip().replace('```json\n', '').replace('\n```', '')
    formatted_dict = json.loads(json_string)
    
    return formatted_dict

