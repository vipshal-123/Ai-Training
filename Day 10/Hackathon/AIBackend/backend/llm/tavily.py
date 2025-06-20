import os
import requests
from dotenv import load_dotenv

load_dotenv("local.env")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_learning_resources(query: str, max_results=3):
    if not TAVILY_API_KEY:
        raise ValueError("Missing TAVILY_API_KEY")

    response = requests.post(
        "https://api.tavily.com/search",
        headers={"Authorization": f"Bearer {TAVILY_API_KEY}"},
        json={
            "query": f"{query} onboarding learning path ",
            "max_results": max_results
        },
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(f"Tavily API error: {response.text}")

    data = response.json()
    return [{"title": r["title"], "url": r["url"]} for r in data.get("results", [])]
