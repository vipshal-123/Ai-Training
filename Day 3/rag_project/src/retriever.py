import faiss
import numpy as np

class VectorStore:
    def __init__(self, embeddings, chunks):
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.chunks = chunks

    def query(self, query_embedding, top_k=3):
        D, I = self.index.search(query_embedding.reshape(1, -1), top_k)
        return [(self.chunks[i], float(D[0][idx])) for idx, i in enumerate(I[0])]
