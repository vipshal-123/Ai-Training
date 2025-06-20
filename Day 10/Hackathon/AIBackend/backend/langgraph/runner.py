from backend.agents.offerAnalyzerAgent import build_offer_analyzer_graph
from backend.agents.candidatePreferenceAgent import build_candidate_preference_graph
from backend.agents.acceptanceAgent import build_acceptance_likelihood_graph
from backend.agents.upskillAgent import build_upskill_graph
import re
import json

def parse_gemini_response(response) -> dict:
    """Safely parse Gemini LLM output into a dict."""
    text = (
        response.text if hasattr(response, "text")
        else response.content if hasattr(response, "content")
        else str(response)
    )
    try:
        cleaned = re.sub(r"```(?:json|python)?", "", text).strip("`\n ")
        if "=" in cleaned and "{" in cleaned:
            cleaned = cleaned.split("=", 1)[-1]
        return json.loads(cleaned)
    except Exception as e:
        return {"error": str(e), "raw": text}

def run_full_pipeline(offer_path, resume_path, placement_data, placement_history):
    offer_agent = build_offer_analyzer_graph()
    offer_state = offer_agent.invoke({"file_path": offer_path})
    offer_components = parse_gemini_response(offer_state["offer_components"])

    preference_agent = build_candidate_preference_graph()
    preference_state = preference_agent.invoke({
        "offer_components": offer_components,
        "resume_path": resume_path,
        "placement_data": placement_data
    })
    preference_alignment = parse_gemini_response(preference_state["preference_alignment"])

    acceptance_agent = build_acceptance_likelihood_graph()
    acceptance_state = acceptance_agent.invoke({
        "offer_components": offer_components,
        "preference_alignment": preference_alignment,
        "placement_history": placement_history
    })
    acceptance_prediction = parse_gemini_response(acceptance_state["acceptance_prediction"])

    upskill_agent = build_upskill_graph()
    upskill_state = upskill_agent.invoke({
        "offer_components": offer_components,
        "acceptance_prediction": acceptance_prediction
    })
    onboarding_resources = parse_gemini_response(upskill_state["onboarding_resources"])

    return {
        "offer_analysis": offer_components,
        "preference_alignment": preference_alignment,
        "acceptance_prediction": acceptance_prediction,
        "upskill_recommendations": onboarding_resources
    }
