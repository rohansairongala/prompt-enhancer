
import os
import urllib.request
import sys

PAPERS_DIR = os.path.join(os.path.dirname(__file__), "data", "papers")
INDEX_DIR  = os.path.join(os.path.dirname(__file__), "data", "faiss_index")

PAPERS = {
    "chain_of_thought.pdf":    "https://arxiv.org/pdf/2201.11903",
    "zero_shot_reasoners.pdf": "https://arxiv.org/pdf/2205.11916",
    "self_consistency.pdf":    "https://arxiv.org/pdf/2203.11171",
    "tree_of_thoughts.pdf":    "https://arxiv.org/pdf/2305.10601",
    "react.pdf":               "https://arxiv.org/pdf/2210.03629",
    "least_to_most.pdf":       "https://arxiv.org/pdf/2205.10625"
}

def setup():
    index_path = os.path.join(INDEX_DIR, "papers.index")
    if os.path.exists(index_path):
        return

    os.makedirs(PAPERS_DIR, exist_ok=True)
    os.makedirs(INDEX_DIR,  exist_ok=True)

    print("Downloading research papers...")
    for filename, url in PAPERS.items():
        path = os.path.join(PAPERS_DIR, filename)
        if not os.path.exists(path):
            print(f"  Downloading {filename}...")
            urllib.request.urlretrieve(url, path)

    print("Building FAISS index...")
    sys.path.append(os.path.dirname(__file__))
    from src.ingest import build_index
    build_index(PAPERS_DIR, INDEX_DIR)
    print("Setup complete ✓")
