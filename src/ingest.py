
import os
import fitz
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

CHUNK_SIZE    = 500
CHUNK_OVERLAP = 100
EMBED_MODEL   = "all-MiniLM-L6-v2"

def extract_text_from_pdf(pdf_path: str) -> str:
    doc  = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list:
    chunks = []
    start  = 0
    while start < len(text):
        end   = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 100:
            chunks.append(chunk)
        start = end - overlap
    return chunks

def build_index(papers_dir: str, index_dir: str):
    os.makedirs(index_dir, exist_ok=True)

    model  = SentenceTransformer(EMBED_MODEL)
    chunks = []
    meta   = []

    pdf_files = [f for f in os.listdir(papers_dir) if f.endswith(".pdf")]
    print(f"Processing {len(pdf_files)} papers...")

    for pdf_file in pdf_files:
        paper_name = pdf_file.replace(".pdf", "").replace("_", " ").title()
        pdf_path   = os.path.join(papers_dir, pdf_file)

        print(f"  Extracting: {paper_name}")
        text        = extract_text_from_pdf(pdf_path)
        paper_chunks = chunk_text(text)

        for chunk in paper_chunks:
            chunks.append(chunk)
            meta.append({"source": paper_name, "text": chunk})

    print(f"Total chunks: {len(chunks)}")
    print("Building embeddings...")

    embeddings = model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index     = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, os.path.join(index_dir, "papers.index"))

    with open(os.path.join(index_dir, "metadata.pkl"), "wb") as f:
        pickle.dump(meta, f)

    print(f"Index saved — {index.ntotal} vectors")
    return index, meta
