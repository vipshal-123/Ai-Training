import os
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
from app.llm.gemini import get_gemini_embedding

load_dotenv()

# MongoDB config
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB")
COLLECTION_NAME = "rag_documents"

client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def rag_query(query: str, top_k: int = 3) -> str:
    """Search MongoDB vectorstore for top_k relevant chunks."""
    query_vector = get_gemini_embedding(query)

    # Retrieve all documents and compute similarity
    docs = list(collection.find())
    scored = []

    for doc in docs:
        sim = cosine_similarity(query_vector, doc["embedding"])
        scored.append((sim, doc["text"]))

    # Sort by similarity and return top_k
    top_chunks = sorted(scored, key=lambda x: x[0], reverse=True)[:top_k]
    return "\n\n".join([chunk[1] for chunk in top_chunks])
