"""Hybrid retrieval combining ChromaDB vector search with BM25 keyword search."""

from navigator.config import BM25_WEIGHT, TOP_K_FINAL
from navigator.rag.store import BenefitsStore
from navigator.rag.bm25 import BM25Index


class HybridRetriever:
    """Combines semantic (ChromaDB) and keyword (BM25) search results.

    Score formula: (1 - alpha) * vector_score + alpha * bm25_score
    where alpha = BM25_WEIGHT (default 0.4).
    """

    def __init__(
        self,
        store: BenefitsStore,
        bm25: BM25Index,
        bm25_weight: float = BM25_WEIGHT,
    ):
        self.store = store
        self.bm25 = bm25
        self.bm25_weight = bm25_weight

    def search(
        self,
        query: str,
        top_k: int = TOP_K_FINAL,
        jurisdiction_filter: list[str] | None = None,
    ) -> list[dict]:
        """Run hybrid search and return merged, deduplicated results."""
        # Build ChromaDB where filter
        where = None
        if jurisdiction_filter:
            if len(jurisdiction_filter) == 1:
                where = {"jurisdiction": jurisdiction_filter[0]}
            else:
                where = {"$or": [{"jurisdiction": j} for j in jurisdiction_filter]}

        # Vector search
        fetch_k = top_k * 3  # over-fetch for merging
        vector_results = self.store.query(query, n_results=fetch_k, where=where)

        # BM25 search (no jurisdiction filter — we filter after)
        bm25_results = self.bm25.search(query, top_k=fetch_k)

        # Normalize scores
        vector_scores = self._normalize_vector_scores(vector_results)
        bm25_scores = self._normalize_bm25_scores(bm25_results)

        # Merge
        all_ids = set(vector_scores.keys()) | set(bm25_scores.keys())
        merged = {}
        for doc_id in all_ids:
            v_score = vector_scores.get(doc_id, 0.0)
            b_score = bm25_scores.get(doc_id, 0.0)
            merged[doc_id] = (1 - self.bm25_weight) * v_score + self.bm25_weight * b_score

        # Sort by combined score
        sorted_ids = sorted(merged, key=merged.get, reverse=True)[:top_k]

        # Build result dicts with text and metadata from vector results
        doc_map = {}
        if vector_results["ids"] and vector_results["ids"][0]:
            for i, doc_id in enumerate(vector_results["ids"][0]):
                doc_map[doc_id] = {
                    "text": vector_results["documents"][0][i],
                    "metadata": vector_results["metadatas"][0][i],
                }

        results = []
        for doc_id in sorted_ids:
            info = doc_map.get(doc_id, {"text": "", "metadata": {}})
            # Apply jurisdiction filter to BM25-only results
            if jurisdiction_filter and doc_id not in doc_map:
                continue  # BM25 result not in filtered vector results — skip
            results.append({
                "id": doc_id,
                "text": info["text"],
                "metadata": info["metadata"],
                "score": merged[doc_id],
            })

        return results

    def _normalize_vector_scores(self, results: dict) -> dict[str, float]:
        """Normalize ChromaDB distances to 0-1 similarity scores."""
        scores = {}
        if not results["ids"] or not results["ids"][0]:
            return scores
        distances = results["distances"][0] if "distances" in results else []
        for i, doc_id in enumerate(results["ids"][0]):
            dist = distances[i] if i < len(distances) else 1.0
            scores[doc_id] = max(0.0, 1.0 - dist / 2.0)
        return scores

    def _normalize_bm25_scores(self, results: list[tuple[str, float]]) -> dict[str, float]:
        """Normalize BM25 scores to 0-1 range."""
        if not results:
            return {}
        max_score = max(s for _, s in results) or 1.0
        return {doc_id: score / max_score for doc_id, score in results}
