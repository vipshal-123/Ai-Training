def transform_results_for_frontend(results: dict) -> dict:
    """Transform raw AI pipeline results into frontend-friendly mock structure"""
    
    offer = results.get("offer_analysis", {})
    preference = results.get("preference_alignment", {})
    acceptance = results.get("acceptance_prediction", {})
    upskill = results.get("upskill_recommendations", {})

    # Convert alignment scores to integers safely
    alignment_scores = []
    for val in preference.values():
        try:
            alignment_scores.append(int(val))
        except (ValueError, TypeError):
            alignment_scores.append(0)

    avg_alignment = sum(alignment_scores) // len(alignment_scores) if alignment_scores else 0

    return {
        "offerAnalysis": {
            "position": offer.get("job_title", "N/A"),
            "salary": f"₹{offer.get('ctc')}" if offer.get("ctc") else "N/A",
            "location": offer.get("location", "N/A"),
            "benefits": list(offer.get("benefits", {}).keys()) if isinstance(offer.get("benefits"), dict) else [],
            "startDate": offer.get("start_date", "TBD"),
        },
        "candidatePreference": {
            "alignmentScore": avg_alignment,
            "preferredSalary": "₹10 LPA+",
            "locationPreference": "Coimbatore / Remote",
            "keySkills": [
                "Node.js", "Python", "React", "AWS", "MongoDB", "Redis", "FastAPI"
            ]
        },
        "acceptanceLikelihood": {
            "probability": acceptance.get("probability", 0),
            "confidence": 90,
            "riskFactors": acceptance.get("reasons", [])[:2],
            "positiveFactors": ["Relevant tech stack", "No bond requirement"]
        },
        "upskillRecommendations": [
            {
                "skill": goal.get("goal", "N/A"),
                "priority": f"Priority {goal.get('priority')}",
                "resources": len(goal.get("resources", []))
            }
            for goal in upskill.get("learningGoals", [])
        ]
    }
