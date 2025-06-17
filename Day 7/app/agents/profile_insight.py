def extract_profile_insights(state: dict) -> dict:
    resume_text = state.get("resume_text")

    # Call Gemini or extract key info from resume_text
    profile_insights = f"Parsed strengths and highlights from resume: {resume_text[:100]}..."

    return {
        **state,
        "profile_insights": profile_insights
    }
