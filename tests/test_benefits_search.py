"""Tests for the benefits knowledge base search tool."""

import pytest
from navigator.rag.store import BenefitsStore
from navigator.rag.bm25 import BM25Index
from navigator.rag.retrieval import HybridRetriever
from navigator.tools.benefits_search import BenefitsSearchTool


@pytest.fixture
def search_tool(tmp_path):
    store = BenefitsStore(persist_dir=str(tmp_path / "chroma"))
    bm25 = BM25Index()

    ids = ["snap", "mfip", "ma", "dw_ramsey", "eap"]
    texts = [
        "SNAP provides monthly food benefits. Eligibility: income below 200% FPL in Minnesota.",
        "MFIP provides cash and food assistance to Minnesota families with children in poverty.",
        "Medical Assistance is Minnesota's Medicaid program for low-income residents.",
        "Ramsey County Dislocated Worker Program helps recently laid-off workers find new employment.",
        "Energy Assistance Program helps pay heating bills. Income below 50% SMI.",
    ]
    metadatas = [
        {"jurisdiction": "state:MN", "category": "food", "program": "SNAP"},
        {"jurisdiction": "state:MN", "category": "cash", "program": "MFIP"},
        {"jurisdiction": "state:MN", "category": "health", "program": "MA"},
        {"jurisdiction": "county:ramsey", "category": "employment", "program": "Dislocated Worker"},
        {"jurisdiction": "state:MN", "category": "energy", "program": "EAP"},
    ]

    store.add_documents(ids=ids, texts=texts, metadatas=metadatas)
    bm25.add_documents(ids=ids, texts=texts)

    retriever = HybridRetriever(store=store, bm25=bm25)
    return BenefitsSearchTool(retriever=retriever)


def test_search_food(search_tool):
    results = search_tool.search(query="food assistance", state="MN")
    assert len(results) > 0
    programs = [r["metadata"]["program"] for r in results]
    assert "SNAP" in programs


def test_search_with_county(search_tool):
    results = search_tool.search(query="employment help", state="MN", county="Ramsey")
    programs = [r["metadata"]["program"] for r in results]
    assert "Dislocated Worker" in programs


def test_search_returns_text_and_metadata(search_tool):
    results = search_tool.search(query="health coverage", state="MN")
    assert len(results) > 0
    r = results[0]
    assert "text" in r
    assert "metadata" in r
    assert "score" in r
