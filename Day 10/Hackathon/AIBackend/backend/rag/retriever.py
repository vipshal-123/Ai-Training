import json
from langchain_core.documents import Document

with open("backend/rag/rag_onboarding_resources.json", "r") as f:
    raw_resources = json.load(f)
    
documents = [
    Document(
        page_content=f"{item['title']}. {item['description']}",
        metadata={
            "id": item["id"],
            "tags": item["tags"],
            "link": item["link"],
            "source": item["source"]
        }
    )
    for item in raw_resources
]

