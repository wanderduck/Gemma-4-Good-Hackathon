"""Embedding model wrapper using sentence-transformers."""

from sentence_transformers import SentenceTransformer

from navigator.config import EMBEDDING_MODEL, EMBEDDING_DIM


class EmbeddingModel:
    """Wrapper for the all-MiniLM-L6-v2 sentence embedding model.

    Runs on CPU. Produces 384-dimensional vectors.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self._model = SentenceTransformer(model_name, device="cpu")

    def embed(self, text: str) -> list[float]:
        """Embed a single text string. Returns a list of floats."""
        vec = self._model.encode(text, convert_to_numpy=True)
        return vec.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. Returns a list of float lists."""
        vecs = self._model.encode(texts, convert_to_numpy=True, batch_size=32)
        return [v.tolist() for v in vecs]
