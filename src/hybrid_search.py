"""Day 11: hybrid retrieval — BM25 + Chroma fused with Reciprocal Rank Fusion.

Semantic search understands meaning; BM25 nails exact terms. RRF merges the
two ranked lists without needing comparable scores: a chunk ranked highly by
both retrievers floats to the top.
"""
from build_index import get_store
from bm25_search import BM25Search

RRF_K = 60


class HybridSearch:
    def __init__(self, rrf_k=RRF_K):
        self.rrf_k = rrf_k
        self.store = get_store()      # semantic (Chroma)
        self.bm25 = BM25Search()      # keyword

    def search(self, query, top_n=5, candidate_n=20):
        sem = self.store.similarity_search_with_score(query, k=candidate_n)
        kw = self.bm25.search(query, k=candidate_n)

        fused = {}
        for rank, (doc, _) in enumerate(sem, start=1):
            key = (doc.metadata["id"], doc.page_content)
            entry = fused.setdefault(key, {"doc": doc, "score": 0.0})
            entry["score"] += 1.0 / (self.rrf_k + rank)
        for rank, (doc, _) in enumerate(kw, start=1):
            key = (doc.metadata["id"], doc.page_content)
            entry = fused.setdefault(key, {"doc": doc, "score": 0.0})
            entry["score"] += 1.0 / (self.rrf_k + rank)

        ranked = sorted(fused.values(), key=lambda x: x["score"], reverse=True)
        return [(x["doc"], x["score"]) for x in ranked[:top_n]]


if __name__ == "__main__":
    h = HybridSearch()
    for q in [
        "성산일출봉",
        "best sunrise viewpoint in Jeju",
        "is the Hallasan trail closed",
    ]:
        print(f"\n--- '{q}' ---")
        for doc, score in h.search(q, top_n=3):
            print(f"{score:.4f} | {doc.metadata['name']} [{doc.metadata['kind']}]")
