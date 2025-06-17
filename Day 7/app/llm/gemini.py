import os
from langchain_google_genai import ( ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings)
from dotenv import load_dotenv

load_dotenv()

# Create a chat model instance
chat_model = ChatGoogleGenerativeAI( 
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  # Recommended default
    google_api_key=os.getenv("GEMINI_API_KEY")
)


def gemini_chat(prompt: str) -> str:
    """Generate a chat completion from Gemini."""
    try:
        response = chat_model.invoke(prompt)
        content = getattr(response, "content", str(response))
        return content
    except Exception as e:
        print(str(e))
        return f"Gemini Chat Error: {str(e)}"

def get_gemini_embedding(text: str) -> list:
    """Generate an embedding for text using Gemini."""
    try:
        response = embedding_model.embed_documents([text]) 
        return response[0]
    except Exception as e:
        print(f"Gemini Embedding Error: {e}")
        return []
