"""Tests for hybrid retrieval (vector + BM25)."""

import pytest
from navigator.rag.store import BenefitsStore
from navigator.rag.bm25 import BM25Index
from navigator.rag.retrieval import HybridRetriever


@pytest.fixture
def retriever(tmp_path):
    store = BenefitsStore(persist_dir=str(tmp_path / "chroma"))
    bm25 = BM25Index()

    ids = ["d1", "d2", "d3"]
    texts = [
        "SNAP provides monthly food benefits on an EBT card. Eligibility: income below 200% FPL.",
        "Medical Assistance is Minnesota's Medicaid program. Free health coverage.",
        "Ramsey County Dislocated Worker Program for recently laid-off workers.",
    ]
    metadatas = [
        {"jurisdiction": "state:MN", "category": "food", "program": "SNAP"},
        {"jurisdiction": "state:MN", "category": "health", "program": "MA"},
        {"jurisdiction": "county:ramsey", "category": "employment", "program": "DW"},
    ]

    store.add_documents(ids=ids, texts=texts, metadatas=metadatas)
    bm25.add_documents(ids=ids, texts=texts)

    return HybridRetriever(store=store, bm25=bm25)


def test_hybrid_search_returns_results(retriever):
    results = retriever.search("food assistance SNAP", top_k=3)
    assert len(results) > 0
    assert all("id" in r and "text" in r and "score" in r for r in results)


def test_hybrid_search_snap_ranks_high(retriever):
    results = retriever.search("food benefits EBT", top_k=3)
    assert results[0]["id"] == "d1"


def test_hybrid_search_with_jurisdiction(retriever):
    results = retriever.search(
        "program",
        top_k=3,
        jurisdiction_filter=["state:MN"],
    )
    ids = [r["id"] for r in results]
    assert "d3" not in ids  # county:ramsey excluded


def test_hybrid_search_multi_jurisdiction(retriever):
    results = retriever.search(
        "program",
        top_k=3,
        jurisdiction_filter=["state:MN", "county:ramsey"],
    )
    ids = [r["id"] for r in results]
    assert "d3" in ids  # county:ramsey included
