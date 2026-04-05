"""Tests for the embedding model wrapper."""

import pytest
from navigator.rag.embeddings import EmbeddingModel


@pytest.fixture(scope="module")
def embed_model():
    """Load embedding model once for all tests in this module."""
    return EmbeddingModel()


def test_embed_single_text(embed_model):
    vec = embed_model.embed("What is SNAP?")
    assert len(vec) == 384  # all-MiniLM-L6-v2 dimension
    assert isinstance(vec, list)
    assert all(isinstance(x, float) for x in vec)


def test_embed_batch(embed_model):
    texts = ["What is SNAP?", "How do I apply for Medicaid?"]
    vecs = embed_model.embed_batch(texts)
    assert len(vecs) == 2
    assert len(vecs[0]) == 384
    assert len(vecs[1]) == 384


def test_embed_empty_string(embed_model):
    vec = embed_model.embed("")
    assert len(vec) == 384
