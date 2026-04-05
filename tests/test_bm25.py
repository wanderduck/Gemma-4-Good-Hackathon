"""Tests for BM25 keyword search."""

import pytest
from navigator.rag.bm25 import BM25Index


@pytest.fixture
def index():
    idx = BM25Index()
    idx.add_documents(
        ids=["d1", "d2", "d3"],
        texts=[
            "SNAP provides monthly food benefits on an EBT card",
            "MFIP provides cash assistance to Minnesota families with children",
            "Ramsey County Dislocated Worker Program helps laid-off workers",
        ],
    )
    return idx


def test_search_keyword_match(index):
    results = index.search("SNAP food", top_k=2)
    assert results[0][0] == "d1"  # SNAP doc should be first


def test_search_returns_scores(index):
    results = index.search("SNAP", top_k=1)
    doc_id, score = results[0]
    assert doc_id == "d1"
    assert score > 0


def test_search_top_k(index):
    results = index.search("assistance", top_k=2)
    assert len(results) == 2


def test_empty_query(index):
    results = index.search("", top_k=3)
    assert len(results) == 3  # BM25 returns all with zero scores
