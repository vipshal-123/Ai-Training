from app.llm.gemini import get_gemini_embedding
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
collection = client[os.getenv("MONGODB_DB")]["rag_documents"]

def chunk_text(text, chunk_size=400):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def load_docs_to_vector_db(filepath: str):
    with open(filepath, "r") as f:
        text = f.read()

    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = get_gemini_embedding(chunk)
        collection.insert_one({
            "text": chunk,
            "embedding": embedding
        })
