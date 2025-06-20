import json
from backend.utils.parsers import extract_text_from_pdf
from backend.llm.gemini import model
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentType(TypedDict):
    resume_text: str
    preference_alignment: dict
    
def candidate_preference_agent(state):
    resume_text = state["resume_text"]
    prompt = f"""
    You are a career guidance AI assistant. A student's resume is provided below.
    Please extract their job-related preferences in this structured JSON format:

    {{
      "preferred_location": "...",
      "interests": ["...", "..."],
      "skills": ["...", "..."],
      "expected_ctc": "...",
      "career_goals": "..."
    }}

    Resume Text:
    {resume_text}
    """

    response = model.generate_content(prompt)
    return {"preference_alignment": response.text}


def build_graph():
    builder = StateGraph(AgentType)

    builder.add_node("CandidatePreference", candidate_preference_agent)
    builder.set_entry_point("CandidatePreference")
    builder.set_finish_point("CandidatePreference")
    return builder.compile()

candidate_graph = build_graph()

def run_candidate_preference_agent(offer_path: str) -> dict:
    resume_text = extract_text_from_pdf(offer_path)

    result = candidate_graph.invoke({"resume_text": resume_text})

    json_string = result["preference_alignment"].strip().replace('```json\n', '').replace('\n```', '')
    formatted_dict = json.loads(json_string)
    
    return formatted_dict