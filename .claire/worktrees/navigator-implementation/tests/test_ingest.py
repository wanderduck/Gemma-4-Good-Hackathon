"""Tests for the document ingestion pipeline."""

import json
import pytest
from navigator.rag.ingest import chunk_text, process_program_file, IngestPipeline


def test_chunk_text_basic():
    text = "word " * 600  # ~600 words
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    # Each chunk should be <= chunk_size words (approximately)
    for chunk in chunks:
        assert len(chunk.split()) <= 120  # some tolerance


def test_chunk_text_short():
    text = "This is a short document."
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunk_text_overlap():
    words = [f"word{i}" for i in range(200)]
    text = " ".join(words)
    chunks = chunk_text(text, chunk_size=50, overlap=10)
    # Check that chunks overlap
    assert len(chunks) > 1
    # Last words of chunk 0 should appear in chunk 1
    chunk0_words = chunks[0].split()
    chunk1_words = chunks[1].split()
    overlap_words = set(chunk0_words[-10:]) & set(chunk1_words[:15])
    assert len(overlap_words) > 0


def test_process_program_file(tmp_path):
    program = {
        "id": "snap_mn",
        "name": "SNAP",
        "category": "food",
        "jurisdiction": "state:MN",
        "description": "SNAP provides monthly food assistance. " * 20,
        "eligibility_summary": "Income below 200% FPL.",
    }
    path = tmp_path / "snap.json"
    path.write_text(json.dumps(program))

    docs = process_program_file(path)
    assert len(docs) >= 1
    assert docs[0]["metadata"]["jurisdiction"] == "state:MN"
    assert docs[0]["metadata"]["program"] == "SNAP"
