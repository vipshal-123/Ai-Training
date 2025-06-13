import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_answer(context, question):
    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer:"""
    response = model.generate_content(prompt)
    return response.text.strip()
