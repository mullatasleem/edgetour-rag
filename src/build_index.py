"""Day 8: build the Chroma vector index over the 744 chunks.

Persistent on-disk index (chroma_db/) using cosine distance over normalized
MiniLM vectors. Returns a LangChain vector store, so later steps (BM25
hybrid, RAG chain) can plug straight into it.
"""
import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

from chunk import chunk_documents

CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = "edgetour"
MODEL_NAME = "all-MiniLM-L6-v2"


class MiniLMEmbeddings(Embeddings):
    """all-MiniLM-L6-v2 with normalized vectors (cosine via dot product)."""

    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text):
        return self.model.encode([text], normalize_embeddings=True)[0].tolist()


def get_store(persist_dir=CHROMA_DIR):
    """Open the existing index (no rebuild)."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=MiniLMEmbeddings(),
        persist_directory=str(persist_dir),
        collection_metadata={"hnsw:space": "cosine"},
    )


def build_index(chunks=None, persist_dir=CHROMA_DIR):
    """Fresh build: wipe old index, embed all chunks, persist."""
    if chunks is None:
        chunks = chunk_documents()
    if persist_dir.exists():
        shutil.rmtree(persist_dir)
    store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=MiniLMEmbeddings(),
        persist_directory=str(persist_dir),
        collection_metadata={"hnsw:space": "cosine"},
    )
    store.add_documents(chunks)
    return store


if __name__ == "__main__":
    store = build_index()
    print("indexed chunks:", store._collection.count())
    print("\n--- smoke test: 'best sunrise viewpoint in Jeju' ---")
    for doc, score in store.similarity_search_with_score(
        "best sunrise viewpoint in Jeju", k=3
    ):
        # cosine distance: lower = more similar
        print(f"{score:.3f} | {doc.metadata['name']} ({doc.metadata['kind']})")
