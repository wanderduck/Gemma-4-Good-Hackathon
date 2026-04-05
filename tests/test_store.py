"""Tests for the ChromaDB store."""

import pytest
from navigator.rag.store import BenefitsStore


@pytest.fixture
def store(tmp_path):
    """Create a temporary ChromaDB store for testing."""
    return BenefitsStore(persist_dir=str(tmp_path / "test_chroma"))


def test_store_init(store):
    assert store.collection is not None


def test_add_and_query(store):
    store.add_documents(
        ids=["doc1", "doc2"],
        texts=[
            "SNAP provides monthly food benefits on an EBT card.",
            "MFIP provides cash assistance to families with children.",
        ],
        metadatas=[
            {"jurisdiction": "state:MN", "category": "food", "program": "SNAP"},
            {"jurisdiction": "state:MN", "category": "cash", "program": "MFIP"},
        ],
    )
    results = store.query("food assistance", n_results=2)
    assert len(results["ids"][0]) == 2
    # SNAP should rank higher for "food assistance"
    assert "SNAP" in results["documents"][0][0]


def test_query_with_jurisdiction_filter(store):
    store.add_documents(
        ids=["fed1", "state1", "county1"],
        texts=[
            "Federal SNAP program for food assistance.",
            "Minnesota MFIP cash and food assistance.",
            "Ramsey County Dislocated Worker Program.",
        ],
        metadatas=[
            {"jurisdiction": "federal", "category": "food"},
            {"jurisdiction": "state:MN", "category": "cash"},
            {"jurisdiction": "county:ramsey", "category": "employment"},
        ],
    )
    # Filter to only state:MN
    results = store.query(
        "assistance",
        n_results=3,
        where={"jurisdiction": "state:MN"},
    )
    assert len(results["ids"][0]) == 1
    assert "MFIP" in results["documents"][0][0]


def test_query_with_multi_jurisdiction_filter(store):
    store.add_documents(
        ids=["fed1", "state1", "county1"],
        texts=[
            "Federal SNAP program.",
            "Minnesota MFIP program.",
            "Ramsey County program.",
        ],
        metadatas=[
            {"jurisdiction": "federal", "category": "food"},
            {"jurisdiction": "state:MN", "category": "cash"},
            {"jurisdiction": "county:ramsey", "category": "employment"},
        ],
    )
    # Filter to federal OR state:MN
    results = store.query(
        "program",
        n_results=3,
        where={"$or": [
            {"jurisdiction": "federal"},
            {"jurisdiction": "state:MN"},
        ]},
    )
    ids = results["ids"][0]
    assert "fed1" in ids
    assert "state1" in ids
    assert "county1" not in ids


def test_document_count(store):
    assert store.count() == 0
    store.add_documents(
        ids=["d1"],
        texts=["Test document"],
        metadatas=[{"jurisdiction": "federal", "category": "test"}],
    )
    assert store.count() == 1
