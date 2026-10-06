"""Day 9: review embedding quality + verify the Chroma index loads from disk.

Checks:
1. Saved vectors are normalized (norms ~1.0) and the right shape.
2. The persistent index opens without rebuilding and holds 744 chunks.
3. Spot-check retrieval on tourism + hazard queries.
"""
from pathlib import Path

import numpy as np

from build_index import get_store

EMB_PATH = Path(__file__).resolve().parent.parent / "data" / "embeddings" / "embeddings.npy"


def check_vector_file():
    v = np.load(EMB_PATH)
    norms = np.linalg.norm(v, axis=1)
    print(f"vectors: shape {v.shape}")
    print(f"norm min/max: {norms.min():.3f} / {norms.max():.3f} (expect ~1.0)")


def check_index():
    store = get_store()  # opens existing index, no rebuild
    n = store._collection.count()
    print(f"chroma count: {n} (expect 744)")
    for q in [
        "typhoon warning Jeju",
        "Hallasan trail closed",
        "best beach for swimming",
    ]:
        print(f"\n--- '{q}' ---")
        for doc, score in store.similarity_search_with_score(q, k=2):
            print(f"{score:.3f} | {doc.metadata['name']} [{doc.metadata['kind']}]")


if __name__ == "__main__":
    check_vector_file()
    check_index()
