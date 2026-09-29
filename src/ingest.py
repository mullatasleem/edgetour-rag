"""Day 4: ingest both datasets into LangChain Document objects.

Reads data/tourism_jeju.json and data/civic_hazards.json and converts each
record into a Document: searchable text (page_content) + structured facts
(metadata). Downstream code (chunking, embeddings, retrieval) imports
load_documents() from here.
"""
import json
from pathlib import Path

from langchain_core.documents import Document

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_tourism_docs():
    records = json.loads((DATA_DIR / "tourism_jeju.json").read_text(encoding="utf-8"))
    docs = []
    for r in records:
        header = r["name"]
        if r.get("name_ko"):
            header += f" ({r['name_ko']})"
        page_content = (
            f"{header}\n"
            f"Category: {r.get('category', '')}\n"
            f"{r.get('description', '')}"
        ).strip()
        metadata = {
            "id": r["id"],
            "kind": "tourism",
            "name": r["name"],
            "name_ko": r.get("name_ko") or "",
            "category": r.get("category") or "",
            "subcategory": r.get("subcategory") or "",
            "latitude": r.get("latitude"),
            "longitude": r.get("longitude"),
            "source": r.get("source") or "",
        }
        # Chroma (later) rejects None metadata values, so drop them.
        metadata = {k: v for k, v in metadata.items() if v is not None}
        docs.append(Document(page_content=page_content, metadata=metadata))
    return docs


def load_hazard_docs():
    records = json.loads((DATA_DIR / "civic_hazards.json").read_text(encoding="utf-8"))
    docs = []
    for r in records:
        page_content = (
            f"{r['title']} [{r['urgency'].upper()}]\n"
            f"Location: {r['location']}\n"
            f"{r['description']}"
        ).strip()
        docs.append(Document(
            page_content=page_content,
            metadata={
                "id": r["id"],
                "kind": "hazard",
                "name": r["title"],
                "hazard": r["hazard"],
                "location": r["location"],
                "urgency": r["urgency"],
                "category": r["category"],
                "source": r.get("source") or "",
            },
        ))
    return docs


def load_documents():
    """All documents: 729 tourism + 10 hazards."""
    return load_tourism_docs() + load_hazard_docs()


if __name__ == "__main__":
    docs = load_documents()
    tourism = [d for d in docs if d.metadata["kind"] == "tourism"]
    hazards = [d for d in docs if d.metadata["kind"] == "hazard"]
    print(f"Loaded {len(docs)} documents ({len(tourism)} tourism + {len(hazards)} hazards)")
    print("\n--- sample tourism doc ---")
    print(tourism[0].page_content[:300])
    print("metadata:", tourism[0].metadata)
    print("\n--- sample hazard doc ---")
    print(hazards[0].page_content)
    print("metadata:", hazards[0].metadata)
