# backend/rag/retriever.py

import json

# Load dummy resource DB
with open("backend/rag/resource_db.json") as f:
    RESOURCE_DB = json.load(f)

def retrieve_resources(role: str, company: str, tools: str) -> list:
    keywords = f"{role} {company} {tools}".lower()
    
    resource_pool = RESOURCE_DB  # Your DB or JSON
    
    matches = []
    for item in resource_pool:
        if any(tag in keywords for tag in item.get("tags", [])):
            matches.append(item)
    
    return matches

