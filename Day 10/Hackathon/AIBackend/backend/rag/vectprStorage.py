from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
from backend.rag.retriever import documents
import os
load_dotenv()


embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  # Recommended default
    google_api_key=os.getenv("GEMINI_API_KEY")
)  


vectorstore = FAISS.from_documents(documents, embedding_model)


vectorstore.save_local("rag_faiss_index")