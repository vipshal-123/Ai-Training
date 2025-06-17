def review_and_approve(state: dict) -> dict:
    # For demo, assume auto-approved. In production, connect to UI/DB
    final_pitch = f"[APPROVED] {state['optimized_pitch']}"
    return {
        **state,
        "final_pitch": final_pitch
    }
