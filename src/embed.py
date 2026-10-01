"""Day 6: embed chunks with all-MiniLM-L6-v2 (384-dim, edge-lightweight).

Each chunk becomes a 384-number vector capturing its meaning. Vectors are
normalized so similarity = dot product. Saved to data/embeddings/ for the
Chroma index (Day 8) to load.
"""
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from chunk import chunk_documents

MODEL_NAME = "all-MiniLM-L6-v2"
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "embeddings"


def embed_chunks(chunks=None, model_name=MODEL_NAME):
    if chunks is None:
        chunks = chunk_documents()
    model = SentenceTransformer(model_name)
    texts = [c.page_content for c in chunks]
    vectors = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    return chunks, np.asarray(vectors, dtype=np.float32)


def save(chunks, vectors, out_dir=OUT_DIR):
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / "embeddings.npy", vectors)
    meta = [{"page_content": c.page_content, "metadata": c.metadata} for c in chunks]
    (out_dir / "chunks_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"saved {len(chunks)} vectors (dim {vectors.shape[1]}) to {out_dir}")


if __name__ == "__main__":
    chunks, vectors = embed_chunks()
    print("vectors shape:", vectors.shape)
    # Sanity check: chunk 0 compared against all chunks — itself must win at ~1.0.
    sims = vectors @ vectors[0]
    top = np.argsort(sims)[-3:][::-1]
    print("top-3 most similar to chunk 0:", top.tolist(),
          "scores:", sims[top].round(3).tolist())
    save(chunks, vectors)
