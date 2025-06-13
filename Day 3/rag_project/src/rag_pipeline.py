from .embedder import model as embed_model
from .retriever import VectorStore
from .generator import generate_answer
from .loader import load_pdf_chunks

def answer_question(question, vector_store):
    query_embedding = embed_model.encode([question])[0]
    results = vector_store.query(query_embedding)
    context = "\n---\n".join(chunk for chunk, _ in results)
    sources = "\n".join(f"[{i+1}] Score: {score:.2f}" for i, (_, score) in enumerate(results))
    answer = generate_answer(context, question)
    return answer, sources
