create virtual env
python -m venv venv

install requirements.txt
pip install -r requirements.txt

# 🎓 AI Pitch Assistant for Campus Recruitment

The **AI Pitch Assistant** is a multi-agent, RAG-powered application designed to help students craft compelling elevator pitches for placement drives. It uses Google Gemini, LangGraph, MongoDB, and Streamlit to analyze resumes, optimize language, and generate recruiter-aligned intros.

---

## 🚀 Features

### 🧠 Multi-Agent Pipeline
- **Profile Insight Agent** – Extracts highlights from resume & achievements
- **Recruiter Language Optimizer Agent (RAG)** – Aligns language with hiring trends using a custom vector store
- **Elevator Pitch Generator Agent** – Crafts personalized 2-minute introductions
- **Pitch Review & Approval Agent** – Placement coordinators can review and approve final pitches

### 👥 Role-Based Access
- 👩‍🎓 **Students**: Upload resumes, generate, download, and view their pitches
- 🧑‍💼 **Placement Officers**: Review, approve, and manage student pitches

### 🗃 MongoDB Vector RAG
- Stores recruiter guides and hiring rubrics as vector chunks using Gemini embeddings
- Enables semantic retrieval for pitch optimization

### 🌐 Streamlit UI
- Simple and interactive UI for both students and placement officers
- Multi-page app with secure login and role-based navigation

---

## 📂 Folder Structure


