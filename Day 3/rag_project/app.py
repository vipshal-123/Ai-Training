import streamlit as st
from src.loader import load_pdf_chunks
from src.embedder import get_embeddings
from src.retriever import VectorStore
from src.rag_pipeline import answer_question

st.set_page_config(page_title="RAG QA with Gemini", layout="wide")
st.title("📄 RAG Question Answering System (Gemini API)")

with st.sidebar:
    st.header("Upload Papers")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

sample_questions = [
    "What are the main components of a RAG model?",
    "What are the two sub-layers in each encoder layer of the Transformer model?",
    "Explain positional encoding in Transformers and why it is necessary.",
    "Describe the concept of multi-head attention.",
    "What is few-shot learning, and how does GPT-3 implement it?"
]

if uploaded_files:
    all_chunks = []
    for file in uploaded_files:
        with open(f"docs/{file.name}", "wb") as f:
            f.write(file.getbuffer())
        chunks = load_pdf_chunks(f"docs/{file.name}")
        all_chunks.extend(chunks)

    embeddings = get_embeddings(all_chunks)
    vector_store = VectorStore(embeddings, all_chunks)

    question = st.text_input("Ask a question about the papers")
    if st.button("Get Answer") and question:
        with st.spinner("Generating answer..."):
            answer, sources = answer_question(question, vector_store)
        st.subheader("Answer")
        st.markdown(answer)
        st.subheader("Source Info")
        st.markdown(sources)

    st.subheader("Sample Questions")
    for q in sample_questions:
        if st.button(q):
            with st.spinner("Generating answer..."):
                answer, sources = answer_question(q, vector_store)
            st.subheader("Answer")
            st.markdown(answer)
            st.subheader("Source Info")
            st.markdown(sources)
