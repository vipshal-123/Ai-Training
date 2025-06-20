import json
from backend.llm.gemini import model
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentType(TypedDict):
    offer_analysis: dict
    preference_alignment: dict
    acceptance_prediction: dict
    upskill_recommendations: dict
    dashboard_summary: str
    
def placement_dashboard_agent(state: AgentType) -> AgentType:
    offer = state["offer_analysis"]
    preference = state["preference_alignment"]
    prediction = state["acceptance_prediction"]
    upskill = state["upskill_recommendations"]

    # Parse if they are still JSON strings
    for k, v in [("offer_analysis", offer), 
                 ("preference_alignment", preference), 
                 ("acceptance_prediction", prediction), 
                 ("upskill_recommendations", upskill)]:
        if isinstance(v, str):
            try:
                state[k] = json.loads(v)
            except:
                pass

    # Re-extract after parsing
    offer = state["offer_analysis"]
    preference = state["preference_alignment"]
    prediction = state["acceptance_prediction"]
    upskill = state["upskill_recommendations"]

    summary = f"""
🔍 Candidate Offer Acceptance Report

📄 OFFER DETAILS:
- Job Title: {offer.get("job_title")}
- Salary: {offer.get("salary")}
- Location: {offer.get("location")}
- Joining Date: {offer.get("joining_date")}
- Bond Terms: {offer.get("bond_terms")}

🧑‍💼 CANDIDATE PREFERENCES:
- Preferred Location: {preference.get("preferred_location")}
- Interests: {", ".join(preference.get("interests", []))}
- Skills: {", ".join(preference.get("skills", []))}
- Expected CTC: {preference.get("expected_ctc")}
- Career Goals: {preference.get("career_goals")}

📈 ACCEPTANCE PREDICTION:
- Likelihood: {prediction.get("acceptance_likelihood")}%
- Reason: {prediction.get("reasoning")}

🎯 UPSKILLING RECOMMENDATIONS:
- Skill Gap: {upskill.get("skill_gap_analysis")}
- Recommended Courses: {", ".join(upskill.get("recommended_courses", []))}
- Onboarding Resources: {", ".join(upskill.get("onboarding_resources", []))}

✅ ACTIONABLE INSIGHT:
The candidate is likely to accept the offer. Recommend initiating onboarding steps and sharing recommended courses.

"""
    return {"dashboard_summary": summary.strip()}

def build_graph():
    builder = StateGraph(AgentType)

    builder.add_node("DashboardAgent", placement_dashboard_agent)
    builder.set_entry_point("DashboardAgent")
    builder.set_finish_point("DashboardAgent")
    return builder.compile()

dashboard_graph = build_graph()

def run_dashboard_agent(offer_analysis: dict, preference_alignment: dict, acceptance_prediction: dict, upskill_recommendations: dict) -> str:
    result = dashboard_graph.invoke({
        "offer_analysis": offer_analysis, 
        "preference_alignment": preference_alignment, 
        "acceptance_prediction": acceptance_prediction, 
        "upskill_recommendations": upskill_recommendations
        })
    
    return result["dashboard_summary"]