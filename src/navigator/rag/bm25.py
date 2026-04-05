"""BM25 keyword search index for government program documents."""

from rank_bm25 import BM25Okapi


class BM25Index:
    """BM25 keyword index for exact-match boosting of program names."""

    def __init__(self):
        self._ids: list[str] = []
        self._corpus: list[list[str]] = []
        self._bm25: BM25Okapi | None = None

    def add_documents(self, ids: list[str], texts: list[str]) -> None:
        """Add documents to the BM25 index."""
        self._ids.extend(ids)
        tokenized = [text.lower().split() for text in texts]
        self._corpus.extend(tokenized)
        self._bm25 = BM25Okapi(self._corpus)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """Search the index. Returns list of (doc_id, score) tuples, sorted by score desc."""
        if self._bm25 is None:
            return []
        tokenized_query = query.lower().split()
        scores = self._bm25.get_scores(tokenized_query)
        scored = list(zip(self._ids, scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
