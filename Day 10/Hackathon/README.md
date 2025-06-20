📊 Offer Acceptance Predictor & Pre-Onboarding Enabler
An Agentic AI System that predicts the likelihood of a student accepting a job offer and prepares personalized onboarding resources — empowering placement officers with actionable insights.

🚀 Objective
To streamline campus placement decisions with intelligent agent workflows that:

Analyze job offers

Match student preferences

Predict acceptance likelihood

Recommend upskilling content

Generate dashboard summaries for placement teams

🧠 Agentic AI Workflow
1️⃣ Offer Analyzer Agent
Parses uploaded offer letters to extract:

🧾 CTC, bonuses

💼 Role details

📍 Location

📄 Other conditions (bond, benefits)

✅ Input: Offer letter (PDF/DOCX)
✅ Output: Structured JSON

2️⃣ Candidate Preference Agent
Aligns offer against student’s:

🎓 Resume (skills, projects)

📋 Placement preferences (location, salary, role)

🧠 Past decision patterns

✅ Input: Resume + Offer JSON + Placement Data
✅ Output: Alignment scores

3️⃣ Acceptance Likelihood Agent
Predicts:

🔢 Likelihood (0–100%) of offer acceptance

🟢 Positive factors

🔴 Risk factors

✅ Input: Offer JSON + Preferences + History
✅ Output: JSON with probability and reasons

4️⃣ Upskill Agent
Recommends:

📚 Learning paths (Java, AWS, etc.)

🧑‍🤝‍🧑 Soft skills (communication, teamwork)

🔒 Secure coding practices

✅ Input: Offer + Prediction
✅ Output: Structured onboarding resources
⚠️ Uses fallback defaults (no RAG)

![alt text](<Untitled Diagram.drawio (1).png>)
