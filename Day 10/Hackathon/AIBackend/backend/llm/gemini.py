import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv("local.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
