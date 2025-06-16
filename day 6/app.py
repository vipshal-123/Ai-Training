import streamlit as st
from dotenv import load_dotenv
import os
from utils import extract_text_from_pdf
from rag_pipeline import generate_outputs

load_dotenv()

st.set_page_config(page_title="AI Elevator Pitch Generator", layout="centered")
st.title("🚀 AI Elevator Pitch Generator")

role = st.selectbox("Who are you?", ["Student", "Placement Officer"])

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_file = st.file_uploader("Upload Job Description (PDF or TXT)", type=["pdf", "txt"])

if st.button("Generate Pitch") and resume_file and jd_file:
    with st.spinner("Processing..."):
        resume_text = extract_text_from_pdf(resume_file)
        jd_text = extract_text_from_pdf(jd_file) if jd_file.name.endswith(".pdf") else jd_file.read().decode("utf-8")

        pitch, keywords, questions = generate_outputs(resume_text, jd_text)

    st.subheader("🗣️ Elevator Pitch")
    st.write(pitch)

    st.subheader("🧠 Recruiter Keywords")
    st.write(", ".join(keywords))

    st.subheader("❓ Mock HR Questions")
    for q in questions:
        st.markdown(f"- {q}")

    if role == "Placement Officer":
        approved = st.radio("Do you approve this pitch?", ["Pending", "Approved", "Rejected"])
        st.success(f"Status: {approved}")