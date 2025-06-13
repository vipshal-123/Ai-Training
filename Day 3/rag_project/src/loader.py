import fitz  # PyMuPDF
import os

def load_pdf_chunks(pdf_path, chunk_size=500, overlap=100):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    chunks = []
    for i in range(0, len(full_text), chunk_size - overlap):
        chunk = full_text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk.strip())
    return chunks
