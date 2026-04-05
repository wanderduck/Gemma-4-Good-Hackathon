"""Document chunking and ingestion pipeline for the benefits knowledge base."""

import json
import hashlib
import logging
from pathlib import Path

from navigator.config import PROCESSED_DIR, PROGRAMS_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from navigator.rag.store import BenefitsStore
from navigator.rag.bm25 import BM25Index

logger = logging.getLogger(__name__)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks by word count."""
    words = text.split()
    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
        if start >= len(words):
            break

    return chunks


def _make_id(text: str, prefix: str = "") -> str:
    """Generate a deterministic ID from text content."""
    h = hashlib.md5(text.encode()).hexdigest()[:12]
    return f"{prefix}_{h}" if prefix else h


def process_program_file(path: Path) -> list[dict]:
    """Process a program JSON file into documents ready for ingestion."""
    data = json.loads(path.read_text())
    program_id = data.get("id", path.stem)
    program_name = data.get("name", program_id)

    parts = []
    if data.get("description"):
        parts.append(data["description"])
    if data.get("eligibility_summary"):
        parts.append(f"Eligibility: {data['eligibility_summary']}")
    if data.get("application_url"):
        parts.append(f"Apply at: {data['application_url']}")

    full_text = "\n\n".join(parts)
    chunks = chunk_text(full_text)

    docs = []
    for i, chunk in enumerate(chunks):
        doc_id = f"{program_id}_chunk{i}"
        docs.append({
            "id": doc_id,
            "text": chunk,
            "metadata": {
                "jurisdiction": data.get("jurisdiction", "federal"),
                "category": data.get("category", "general"),
                "program": program_name,
                "program_id": program_id,
                "source": data.get("source", ""),
                "chunk_index": i,
            },
        })
    return docs


def process_text_file(
    path: Path,
    jurisdiction: str,
    category: str,
    program: str = "",
    source: str = "",
) -> list[dict]:
    """Process a plain text or markdown file into chunked documents."""
    text = path.read_text()
    chunks = chunk_text(text)

    docs = []
    for i, chunk in enumerate(chunks):
        doc_id = _make_id(chunk, prefix=path.stem)
        docs.append({
            "id": doc_id,
            "text": chunk,
            "metadata": {
                "jurisdiction": jurisdiction,
                "category": category,
                "program": program,
                "source": source or str(path.name),
                "chunk_index": i,
            },
        })
    return docs


class IngestPipeline:
    """Orchestrates ingestion of all data sources into ChromaDB + BM25."""

    def __init__(self, store: BenefitsStore | None = None, bm25: BM25Index | None = None):
        self.store = store or BenefitsStore()
        self.bm25 = bm25 or BM25Index()
        self._total_docs = 0

    def ingest_programs_dir(self, programs_dir: Path | None = None) -> int:
        """Ingest all JSON program files from the programs directory."""
        directory = programs_dir or PROGRAMS_DIR
        count = 0
        for path in sorted(directory.glob("**/*.json")):
            docs = process_program_file(path)
            self._add_docs(docs)
            count += len(docs)
            logger.info("Ingested %s: %d chunks", path.name, len(docs))
        return count

    def ingest_text_dir(
        self,
        text_dir: Path,
        jurisdiction: str,
        category: str,
        program: str = "",
    ) -> int:
        """Ingest all text/markdown files from a directory."""
        count = 0
        for ext in ["*.txt", "*.md"]:
            for path in sorted(text_dir.glob(f"**/{ext}")):
                docs = process_text_file(path, jurisdiction, category, program)
                self._add_docs(docs)
                count += len(docs)
        return count

    def _add_docs(self, docs: list[dict]) -> None:
        """Add documents to both ChromaDB and BM25 index."""
        if not docs:
            return
        ids = [d["id"] for d in docs]
        texts = [d["text"] for d in docs]
        metadatas = [d["metadata"] for d in docs]

        self.store.add_documents(ids=ids, texts=texts, metadatas=metadatas)
        self.bm25.add_documents(ids=ids, texts=texts)
        self._total_docs += len(docs)

    @property
    def total_documents(self) -> int:
        return self._total_docs
