from app.llm.gemini import gemini_chat
from app.llm.prompts import ELEVATOR_PITCH_PROMPT

def generate_elevator_pitch(state: dict) -> dict:
    context = f"{state['profile_insights']}\n\n{state['recruiter_context']}"
    prompt = ELEVATOR_PITCH_PROMPT.format(context=context)
    
    optimized_pitch = gemini_chat(prompt)
    return {
        **state,
        "optimized_pitch": optimized_pitch
    }
