
import os
import sys

INDEX_DIR  = os.path.join(os.path.dirname(__file__), "data", "faiss_index")
PAPERS_DIR = os.path.join(os.path.dirname(__file__), "data", "papers")

def ensure_index():
    index_path = os.path.join(INDEX_DIR, "papers.index")
    if os.path.exists(index_path):
        return

    print("Building FAISS index from research papers...")
    sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

    from ingest import build_index
    build_index(PAPERS_DIR, INDEX_DIR)
    print("Index built successfully ✓")

if __name__ == "__main__":
    ensure_index()
