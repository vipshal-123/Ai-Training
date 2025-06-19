from app.llm.retriever import rag_query

def optimize_with_rag(state: dict) -> dict:
    profile_insights = state.get("profile_insights")

    # Do a RAG query against MongoDB vectorstore
    recruiter_context = rag_query(profile_insights)

    return {
        **state,
        "recruiter_context": recruiter_context
    }
