import json
from backend.llm.gemini import model
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentType(TypedDict):
    offer_analysis: dict
    preference_alignment: dict
    acceptance_prediction: dict
    
def acceptance_likelihood_agent(state: AgentType) -> AgentType:
    offer = state["offer_analysis"]
    preference = state["preference_alignment"]

    if isinstance(offer, str):
        offer = json.loads(offer)
    if isinstance(preference, str):
        preference = json.loads(preference)

    prompt = f"""
    You are an AI placement counselor.
    Based on the offer details and the candidate's preferences, predict the likelihood that the student will accept the job.

    Offer Details:
    {json.dumps(offer, indent=2)}

    Candidate Preferences:
    {json.dumps(preference, indent=2)}

    Respond in the following format:
    {{
      "acceptance_likelihood": <percentage from 0 to 100>,
      "confidence": <percentage from 0 to 100>,
      "reasoning": "short explanation of why the student is likely/unlikely to accept"
    }}
    """

    response = model.generate_content(prompt)
    return {"acceptance_prediction": response.text}

def build_graph():
    builder = StateGraph(AgentType)


    builder.add_node("AcceptanceLikelihood", acceptance_likelihood_agent)
    builder.set_entry_point("AcceptanceLikelihood")
    builder.set_finish_point("AcceptanceLikelihood")
    return builder.compile()

acceptance_graph = build_graph()

def run_acceptance_agent(offer_analysis: dict, preference_alignment: dict) -> dict:
    
    result = acceptance_graph.invoke({"offer_analysis": offer_analysis, "preference_alignment": preference_alignment})

    json_string = result["acceptance_prediction"].strip().replace('```json\n', '').replace('\n```', '')
    formatted_dict = json.loads(json_string)
    
    return formatted_dict