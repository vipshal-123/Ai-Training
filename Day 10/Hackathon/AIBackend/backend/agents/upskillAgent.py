import json
from backend.llm.gemini import model
from langgraph.graph import StateGraph
from typing import TypedDict
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from backend.rag.vectprStorage import vectorstore
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv
load_dotenv()


class AgentType(TypedDict):
    offer_analysis: dict
    preference_alignment: dict
    upskill_recommendations: dict
    
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)  
    
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"), temperature=0.4)

retriever = vectorstore.as_retriever(search_type="similarity", k=3)

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type="stuff"
)
    
def upskill_agent(state: AgentType) -> AgentType:
    offer = state["offer_analysis"]
    preference = state["preference_alignment"]

    if isinstance(offer, str):
        offer = json.loads(offer)
    if isinstance(preference, str):
        preference = json.loads(preference)

    job_title = offer.get("job_title", "")
    skills = ", ".join(preference.get("skills", []))
    query = f"Onboarding resources for a {job_title} with skills in {skills}"

    rag_result = rag_chain.invoke(query)
    source_docs = rag_result["source_documents"]
    print("=========", rag_result)

    sources = "\n".join([f"- {doc.page_content} (source: {doc.metadata.get('source')})" for doc in source_docs])

    prompt = f"""
    You are a career development AI assistant.
    Based on the job offer and candidate profile, and the following resources:

    {sources}

    Generate JSON like this:
    {{
      "recommended_courses": ["course 1", "course 2", ...],
      "onboarding_resources": ["resource 1", "resource 2", ...],
      "skill_gap_analysis": "Brief explanation of missing or weak skills"
    }}

    Job Offer:
    {json.dumps(offer, indent=2)}

    Candidate Profile:
    {json.dumps(preference, indent=2)}
    """

    response = model.generate_content(prompt)
    return {"upskill_recommendations": response.text}

def build_graph():
    builder = StateGraph(AgentType)

    builder.add_node("UpskillAgent", upskill_agent)
    builder.set_entry_point("UpskillAgent")
    builder.set_finish_point("UpskillAgent")
    return builder.compile()

upskill_graph = build_graph()

def run_upskill_agent(offer_analysis: dict, preference_alignment: dict) -> dict:
    
    result = upskill_graph.invoke({"offer_analysis": offer_analysis, "preference_alignment": preference_alignment})

    json_string = result["upskill_recommendations"].strip().replace('```json\n', '').replace('\n```', '')
    formatted_dict = json.loads(json_string)
    
    return formatted_dict