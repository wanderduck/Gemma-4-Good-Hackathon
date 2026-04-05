"""Shared test fixtures for Navigator tests."""

import os
# Must be set before chromadb is imported anywhere — protobuf 4.x + older
# generated _pb2 files require the pure-Python implementation.
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

import pytest
from pathlib import Path

TEST_DIR = Path(__file__).parent
FIXTURES_DIR = TEST_DIR / "fixtures"


@pytest.fixture
def sample_user_input():
    """A typical user situation description."""
    return (
        "I'm a single mom with two kids, ages 3 and 7. "
        "I just got laid off from my warehouse job where I made $32,000. "
        "We're in Ramsey County and I'm worried about paying rent and feeding my kids."
    )


@pytest.fixture
def sample_user_input_spanish():
    """Same situation in Spanish."""
    return (
        "Soy madre soltera con dos hijos de 3 y 7 anos. "
        "Me acaban de despedir de mi trabajo en un almacen donde ganaba $32,000. "
        "Vivimos en el condado de Ramsey y me preocupa pagar el alquiler y alimentar a mis hijos."
    )
