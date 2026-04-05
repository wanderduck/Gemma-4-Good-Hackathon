"""ChromaDB collection management for the benefits knowledge base."""

from __future__ import annotations

import chromadb
from chromadb import EmbeddingFunction, Documents, Embeddings

from navigator.config import CHROMA_DIR, CHROMA_COLLECTION
from navigator.rag.embeddings import EmbeddingModel


class _SentenceTransformerEF(EmbeddingFunction[Documents]):
    """ChromaDB EmbeddingFunction adapter for our EmbeddingModel."""

    def __init__(self, model: EmbeddingModel) -> None:
        self._model = model

    def __call__(self, input: Documents) -> Embeddings:  # noqa: A002
        return self._model.embed_batch(list(input))

    @staticmethod
    def name() -> str:
        return "sentence_transformer_ef"

    def get_config(self) -> dict:
        return {}

    @staticmethod
    def build_from_config(config: dict) -> "_SentenceTransformerEF":
        return _SentenceTransformerEF(EmbeddingModel())


class BenefitsStore:
    """ChromaDB-backed vector store for benefits program documents."""

    def __init__(
        self,
        persist_dir: str | None = None,
        collection_name: str = CHROMA_COLLECTION,
    ):
        persist = persist_dir or str(CHROMA_DIR)
        self._client = chromadb.PersistentClient(path=persist)
        self._embed_model = EmbeddingModel()
        self._ef = _SentenceTransformerEF(self._embed_model)
        self.collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=self._ef,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(
        self,
        ids: list[str],
        texts: list[str],
        metadatas: list[dict],
    ) -> None:
        """Add documents to the collection."""
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
        )

    def query(
        self,
        query_text: str,
        n_results: int = 10,
        where: dict | None = None,
    ) -> dict:
        """Query the collection by text similarity."""
        kwargs: dict = {
            "query_texts": [query_text],
            "n_results": n_results,
        }
        if where:
            kwargs["where"] = where
        return self.collection.query(**kwargs)

    def count(self) -> int:
        """Return the number of documents in the collection."""
        return self.collection.count()
