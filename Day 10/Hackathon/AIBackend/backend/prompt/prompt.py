OFFER_EXTRACTION_PROMPT = """
Extract the following key components from the job offer text below and return it as a Python dictionary with labeled keys:
- ctc (e.g., '10 LPA')
- bonuses (if any)
- job_title
- responsibilities
- location (city or remote/onsite)
- bond_duration (if mentioned)
- benefits (healthcare, leaves, etc.)

Text:
\"\"\"
{offer_text}
\"\"\"
"""


PREFERENCE_ALIGNMENT_PROMPT = """
Compare the following job offer components with the candidate’s resume and placement data.
Return a Python dictionary with alignment scores (0-100) for each component like:
{{
    "location": 90,
    "ctc": 75,
    "role": 85,
    "bond_duration": 60,
    "benefits": 80
}}

Offer Components:
{offer}

Resume Content:
\"\"\"
{resume}
\"\"\"

Placement Data:
\"\"\"
{placement_data}
\"\"\"
"""

ACCEPTANCE_PREDICTION_PROMPT = """
Based on the following data, predict the likelihood (0 to 100) that the candidate will accept this job offer.

Input:
- Offer Components:
{offer}

- Preference Alignment Scores:
{alignment}

- Placement Trends (rejections, common reasons):
\"\"\"
{trends}
\"\"\"

Output Format:
{{
  "probability": 65,
  "reasons": [
    "Mismatch in work location preference",
    "CTC is lower than candidate's past offers"
  ]
}}
"""

UPSKILL_RECOMMENDATION_PROMPT = """
Given the following job offer details and learning resources, recommend a tailored onboarding plan.

Job Offer:
{offer}

Learning Resources:
{resources}

Output a JSON object with 3-5 prioritized learning goals and recommended links.

"""

PLACEMENT_DASHBOARD_PROMPT = """
You are a placement officer dashboard assistant.

From the given acceptance predictions and onboarding resource suggestions, generate a summary with:
1. At-risk offers (probability < 70) and reasons
2. Actionable steps per at-risk offer
3. Overview of onboarding prep status per candidate

Acceptance Predictions:
{predictions}

Onboarding Resources:
{onboarding_resources}

Output Format:
{
  "at_risk_offers": [
    {
      "candidate_id": "...",
      "probability": 60,
      "reasons": ["Relocation mismatch", "Low CTC"],
      "suggested_action": "Discuss relocation flexibility with candidate"
    },
    ...
  ],
  "onboarding_summary": [
    {
      "candidate_id": "...",
      "resources_ready": true,
      "resource_count": 3
    }
  ]
}
"""

