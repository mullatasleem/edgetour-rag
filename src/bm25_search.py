"""Day 10: BM25 keyword search over chunks.

Complements semantic (vector) search: BM25 rewards exact term matches, so
queries with proper nouns or Korean names (e.g. 성산일출봉) hit precisely.
Day 11 fuses both rankings with Reciprocal Rank Fusion.
"""
import re

from rank_bm25 import BM25Okapi

from chunk import chunk_documents


def _tokenize(text):
    return re.findall(r"\w+", text.lower())


class BM25Search:
    def __init__(self, chunks=None):
        self.chunks = chunks if chunks is not None else chunk_documents()
        self.bm25 = BM25Okapi([_tokenize(c.page_content) for c in self.chunks])

    def search(self, query, k=5):
        scores = self.bm25.get_scores(_tokenize(query))
        top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [(self.chunks[i], float(scores[i])) for i in top]


if __name__ == "__main__":
    s = BM25Search()
    print(f"indexed {len(s.chunks)} chunks for keyword search")
    for q in ["성산일출봉", "typhoon", "waterfall"]:
        print(f"\n--- '{q}' ---")
        for doc, score in s.search(q, k=3):
            print(f"{score:.2f} | {doc.metadata['name']} [{doc.metadata['kind']}]")
