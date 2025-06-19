# app/llm/prompts.py

# Used by Profile Insight Agent
PROFILE_INSIGHT_PROMPT = """
You are an AI assistant that extracts key achievements, strengths, and differentiators from a student's resume and project descriptions.

Resume Content:
{resume_text}

Extract and summarize:
1. Core technical skills
2. Key projects and outcomes
3. Extracurriculars and leadership roles
4. Unique strengths or differentiators

Provide your answer as a well-structured summary.
"""

# Used by Recruiter Language Optimizer Agent (with RAG results)
RECRUITER_OPTIMIZATION_PROMPT = """
You are a recruiter-focused assistant. Improve the language of this student summary by aligning it with recruiter priorities like problem-solving, impact, leadership, teamwork, and communication.

Student Summary:
{profile_insights}

Relevant recruiter expectations from hiring guides:
{rag_context}

Output an improved version of the student's pitch content that would impress campus recruiters.
"""

# Used by Elevator Pitch Generator Agent
ELEVATOR_PITCH_PROMPT = """
You are a professional resume pitch writer. Using the following optimized recruiter-facing content, write a 2-minute elevator pitch that a student can use during a placement drive introduction.

Optimized Recruiter-Aligned Summary:
{context}

Format:
- 3-4 short paragraphs
- Tone: confident, clear, enthusiastic
- Include personal motivation, relevant achievements, and career goal

Return only the pitch content.
"""

# Optional: Used for mock HR questions (not in the current agent chain)
HR_QUESTION_PROMPT = """
Based on the student's background below, generate 3 personalized HR interview questions that test both technical and behavioral aspects.

Student Profile:
{profile}

Questions should be:
1. Relevant to their projects and achievements
2. Test soft skills like leadership, problem-solving, and initiative
3. Avoid generic questions

Return as a bullet list.
"""
