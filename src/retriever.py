
import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "all-MiniLM-L6-v2"
_model      = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model

def load_index(index_dir: str):
    index_path = os.path.join(index_dir, "papers.index")
    meta_path  = os.path.join(index_dir, "metadata.pkl")

    index = faiss.read_index(index_path)

    with open(meta_path, "rb") as f:
        meta = pickle.load(f)

    return index, meta

def retrieve(query: str, index, meta: list, top_k: int = 3) -> list:
    model      = get_model()
    query_emb  = model.encode([query]).astype("float32")
    distances, indices = index.search(query_emb, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(meta):
            results.append({
                "source"  : meta[idx]["source"],
                "text"    : meta[idx]["text"],
                "distance": float(distances[0][i])
            })
    return results

def format_context(results: list) -> str:
    context = "Relevant research findings:\n\n"
    for i, r in enumerate(results):
        context += f"[{i+1}] From '{r['source']}':\n{r['text']}\n\n"
    return context.strip()
