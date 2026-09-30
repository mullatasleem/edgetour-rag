"""Day 5: split documents into retrieval-friendly chunks.

Long descriptions get cut into 512-char pieces with 50 chars of overlap,
so no sentence is lost at a boundary and each chunk stays focused enough
to embed well. Short docs pass through as a single chunk.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingest import load_documents

CHUNK_SIZE = 512
CHUNK_OVERLAP = 50


def get_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def chunk_documents(docs=None):
    """Split documents into chunks, preserving metadata on each chunk."""
    if docs is None:
        docs = load_documents()
    return get_splitter().split_documents(docs)


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    long_docs = sum(1 for d in docs if len(d.page_content) > CHUNK_SIZE)
    avg_len = sum(len(c.page_content) for c in chunks) / len(chunks)
    print(f"{len(docs)} documents -> {len(chunks)} chunks")
    print(f"documents longer than {CHUNK_SIZE} chars: {long_docs}")
    print(f"average chunk length: {avg_len:.0f} chars")
    print("\n--- sample chunk ---")
    print(chunks[0].page_content[:400])
    print("metadata keys:", sorted(chunks[0].metadata.keys()))
