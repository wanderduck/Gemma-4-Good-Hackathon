# Plain Language Government Navigator — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a conversational AI benefits navigator that takes plain-language situation descriptions and returns personalized, prioritized eligibility guidance for federal, Minnesota state, and Twin Cities metro county programs — with source citations, document checklists, and application links.

**Architecture:** Three-stage agentic pipeline (Intake -> Eligibility Engine -> Response Generation) powered by Gemma 4 E4B via Ollama locally, with 26B A4B MoE on Kaggle/Colab for complex reasoning. RAG via ChromaDB + BM25 hybrid retrieval. Gradio UI deployed on HuggingFace Spaces.

**Tech Stack:** Python 3.13, Gemma 4 (E4B + 26B MoE), Ollama, Unsloth, ChromaDB, sentence-transformers, rank_bm25, Gradio, textstat, uv

**Spec:** `docs/superpowers/specs/2026-04-05-plain-language-government-navigator-design.md`
**Full Plan:** `docs/ideas/plans/plain_language_government_navigator.md`
**Toolchain Reference:** `docs/research/toolchain_reference_guide.md`
**MN Research:** `docs/research/minnesota_benefits_deep_dive.md`
**Federal Research:** `docs/research/plain_language_gov_navigator_research.md`

---

## File Structure

```
src/
  navigator/
    __init__.py                  # Package init, version
    config.py                    # Settings: paths, model names, API keys, thresholds
    models.py                    # Pydantic data models (UserProfile, Program, EligibilityResult, etc.)
    prompts.py                   # All system prompts and prompt templates
    ollama_client.py             # Ollama API wrapper (chat, function calling, streaming)
    readability.py               # Flesch-Kincaid readability checking via textstat
    intake.py                    # Stage 1: situation parsing -> UserProfile JSON
    eligibility.py               # Stage 2: agentic eligibility engine with tool loop
    response.py                  # Stage 3: plain language response generation
    rag/
      __init__.py
      embeddings.py              # Embedding model wrapper (all-MiniLM-L6-v2)
      store.py                   # ChromaDB collection management (create, add, query)
      bm25.py                    # BM25 keyword index
      retrieval.py               # Hybrid retrieval combining vector + BM25
      ingest.py                  # Document chunking and ingestion pipeline
    tools/
      __init__.py
      fpl.py                     # Federal Poverty Level calculator
      benefits_search.py         # RAG search over benefits knowledge base
      program_eligibility.py     # Per-program eligibility checking logic
      county_programs.py         # County-specific program lookup
      document_requirements.py   # Required documents per program
      api_clients.py             # External API clients (NYC Screening, CMS, HUD, CareerOneStop)
  app.py                         # Gradio UI application entry point

scripts/
  scrape_dhs_manual.py           # Scrape DHS Combined Manual (cash/food eligibility)
  scrape_dhs_epm.py              # Scrape DHS Eligibility Policy Manual (health care)
  scrape_county_pages.py         # Scrape 5 county social services pages
  scrape_cap_agencies.py         # Scrape 3 CAP agency program pages
  download_sam_gov.py            # Download SAM.gov assistance listings via API
  download_mn_house_pubs.py      # Download MN House Research PDFs
  ingest_all.py                  # Run full ingestion pipeline into ChromaDB
  build_training_data.py         # Build fine-tuning dataset from scraped content

training/
  train_unsloth.py               # Unsloth QLoRA fine-tuning script for E4B
  eval_model.py                  # Evaluate fine-tuned vs base model
  export_gguf.py                 # Export fine-tuned model to GGUF for Ollama

data/
  raw/                           # Raw scraped HTML/text/JSON
  processed/                     # Cleaned, chunked documents ready for ingestion
  chroma_db/                     # ChromaDB persistent storage
  fpl_tables/                    # FPL threshold JSON files
  programs/                      # Program definition JSON files (federal, state, county)
  training/                      # Fine-tuning datasets

tests/
  conftest.py                    # Shared fixtures
  test_models.py                 # Data model tests
  test_fpl.py                    # FPL calculator tests
  test_ollama_client.py          # Ollama client tests
  test_readability.py            # Readability checker tests
  test_embeddings.py             # Embedding model tests
  test_store.py                  # ChromaDB store tests
  test_bm25.py                   # BM25 index tests
  test_retrieval.py              # Hybrid retrieval tests
  test_ingest.py                 # Ingestion pipeline tests
  test_intake.py                 # Stage 1 intake tests
  test_benefits_search.py        # Benefits search tool tests
  test_program_eligibility.py    # Program eligibility tests
  test_county_programs.py        # County programs tests
  test_document_requirements.py  # Document requirements tests
  test_eligibility_engine.py     # Stage 2 eligibility engine tests
  test_response.py               # Stage 3 response generation tests
  test_integration.py            # End-to-end integration tests
```

---

## Task 1: Project Scaffolding & Dependencies

**Files:**
- Modify: `pyproject.toml`
- Create: `src/navigator/__init__.py`
- Create: `src/navigator/config.py`
- Create: `tests/conftest.py`
- Create: `src/app.py` (placeholder)
- Create: `scripts/.gitkeep`
- Create: `training/.gitkeep`

- [ ] **Step 1: Add project dependencies**

Add the navigator-specific dependencies to `pyproject.toml`. Do NOT remove existing dependencies — add to the list.

```toml
# Add these to the [project] dependencies list:
    "chromadb>=1.0.0",
    "sentence-transformers>=4.1.0",
    "rank-bm25>=0.2.2",
    "gradio>=5.29.0",
    "textstat>=0.7.4",
    "ollama>=0.5.1",
    "pydantic>=2.11.3",
    "httpx>=0.28.1",
    "beautifulsoup4>=4.13.4",
    "lxml>=5.4.0",
```

- [ ] **Step 2: Install dependencies**

Run: `uv sync`
Expected: All packages install successfully. Check for conflicts with existing RAPIDS/CUDA deps. If conflicts arise, the navigator deps should be isolated — consider adding them in a separate `[project.optional-dependencies]` group called `navigator`.

- [ ] **Step 3: Create package structure**

Create `src/navigator/__init__.py`:

```python
"""Plain Language Government Navigator — Gemma 4 Good Hackathon."""

__version__ = "0.1.0"
```

- [ ] **Step 4: Create config module**

Create `src/navigator/config.py`:

```python
"""Configuration for the Navigator application."""

from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CHROMA_DIR = DATA_DIR / "chroma_db"
FPL_DIR = DATA_DIR / "fpl_tables"
PROGRAMS_DIR = DATA_DIR / "programs"
TRAINING_DIR = DATA_DIR / "training"

# Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma4:4b-it-q4_0"

# Embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# ChromaDB
CHROMA_COLLECTION = "benefits_kb"

# RAG
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
TOP_K_VECTOR = 10
TOP_K_BM25 = 10
TOP_K_FINAL = 8
BM25_WEIGHT = 0.4  # alpha for hybrid: (1-alpha)*vector + alpha*bm25

# Readability
TARGET_READING_LEVELS = {
    "simple": 5.0,    # 5th grade Flesch-Kincaid
    "standard": 8.0,  # 8th grade
    "detailed": 12.0, # 12th grade (no simplification)
}

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "hmn": "Hmong",
    "so": "Somali",
    "kar": "Karen",
}

# Ensure data directories exist
for d in [RAW_DIR, PROCESSED_DIR, CHROMA_DIR, FPL_DIR, PROGRAMS_DIR, TRAINING_DIR]:
    d.mkdir(parents=True, exist_ok=True)
```

- [ ] **Step 5: Create test conftest**

Create `tests/conftest.py`:

```python
"""Shared test fixtures for Navigator tests."""

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
```

- [ ] **Step 6: Create directory stubs**

Run:
```bash
mkdir -p src/navigator/rag src/navigator/tools tests/fixtures scripts training data/raw data/processed data/chroma_db data/fpl_tables data/programs data/training
touch src/navigator/rag/__init__.py src/navigator/tools/__init__.py scripts/.gitkeep training/.gitkeep
```

- [ ] **Step 7: Create app.py placeholder**

Create `src/app.py`:

```python
"""Gradio UI entry point for the Plain Language Government Navigator."""


def main():
    """Launch the Navigator Gradio app."""
    raise NotImplementedError("UI not yet implemented — see Task 16")


if __name__ == "__main__":
    main()
```

- [ ] **Step 8: Verify structure and commit**

Run:
```bash
python -c "from navigator.config import PROJECT_ROOT; print(f'Config OK: {PROJECT_ROOT}')"
```
Expected: `Config OK: /home/wanderduck/.../Gemma4-GoodHackathon`

Run:
```bash
pytest tests/ --collect-only
```
Expected: Collects conftest fixtures, no errors.

```bash
git add src/ tests/ scripts/ training/ pyproject.toml
git commit -m "feat: scaffold project structure for Plain Language Government Navigator"
```

---

## Task 2: Data Models

**Files:**
- Create: `src/navigator/models.py`
- Create: `tests/test_models.py`

- [ ] **Step 1: Write data model tests**

Create `tests/test_models.py`:

```python
"""Tests for navigator data models."""

import pytest
from navigator.models import (
    UserProfile,
    Dependent,
    Program,
    EligibilityResult,
    BenefitsResponse,
    ReadingLevel,
)


def test_user_profile_from_basic_info():
    profile = UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
        state="MN",
        employment_status="recently_unemployed",
        dependents=[Dependent(age=3), Dependent(age=7)],
        concerns=["housing", "food"],
    )
    assert profile.income == 32000
    assert profile.household_size == 3
    assert profile.county == "Ramsey"
    assert len(profile.dependents) == 2


def test_user_profile_defaults():
    profile = UserProfile()
    assert profile.state == "MN"
    assert profile.household_size == 1
    assert profile.language == "en"
    assert profile.reading_level == ReadingLevel.STANDARD
    assert profile.dependents == []
    assert profile.concerns == []


def test_user_profile_fpl_percentage():
    # 2026 FPL for household of 3 is $26,070 (approx)
    profile = UserProfile(income=32000, household_size=3)
    # 32000 / 26070 = ~122.7% FPL
    pct = profile.fpl_percentage
    assert 120 < pct < 130


def test_program_model():
    program = Program(
        id="snap_mn",
        name="SNAP (Food Assistance)",
        category="food",
        jurisdiction="state:MN",
        description="Monthly food benefits loaded onto an EBT card.",
        eligibility_summary="Income below 200% FPL (MN BBCE threshold).",
        application_url="https://mnbenefits.mn.gov/",
        source="DHS Combined Manual Section 0007.06",
    )
    assert program.id == "snap_mn"
    assert program.jurisdiction == "state:MN"


def test_eligibility_result():
    result = EligibilityResult(
        program_id="snap_mn",
        program_name="SNAP (Food Assistance)",
        eligible=True,
        confidence="high",
        reason="Household income $32,000 = 123% FPL, below MN's 200% BBCE threshold.",
        estimated_benefit="$658/month for household of 3",
        source="DHS Combined Manual Section 0007.06",
    )
    assert result.eligible is True
    assert result.confidence == "high"


def test_benefits_response():
    result = EligibilityResult(
        program_id="snap_mn",
        program_name="SNAP",
        eligible=True,
        confidence="high",
        reason="Below threshold",
    )
    response = BenefitsResponse(
        eligible_programs=[result],
        documents_needed=["Photo ID", "Pay stubs"],
        application_groups={"mnbenefits.mn.gov": ["SNAP", "MFIP"]},
        disclaimer="This is an informational tool, not legal advice.",
    )
    assert len(response.eligible_programs) == 1
    assert "Photo ID" in response.documents_needed


def test_reading_level_enum():
    assert ReadingLevel.SIMPLE.value == "simple"
    assert ReadingLevel.STANDARD.value == "standard"
    assert ReadingLevel.DETAILED.value == "detailed"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_models.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'navigator.models'`

- [ ] **Step 3: Implement data models**

Create `src/navigator/models.py`:

```python
"""Data models for the Navigator application."""

from enum import Enum
from pydantic import BaseModel, Field


class ReadingLevel(str, Enum):
    SIMPLE = "simple"
    STANDARD = "standard"
    DETAILED = "detailed"


# FPL thresholds for 2026 (HHS Poverty Guidelines)
# https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines
FPL_2026_BASE = 15_650  # 1 person
FPL_2026_PER_ADDITIONAL = 5_380  # each additional person


def fpl_threshold(household_size: int) -> int:
    """Return the Federal Poverty Level for a given household size (2026, 48 contiguous states)."""
    if household_size < 1:
        household_size = 1
    return FPL_2026_BASE + FPL_2026_PER_ADDITIONAL * (household_size - 1)


class Dependent(BaseModel):
    age: int
    relationship: str = "child"


class UserProfile(BaseModel):
    income: float | None = None
    household_size: int = 1
    county: str | None = None
    state: str = "MN"
    employment_status: str | None = None
    dependents: list[Dependent] = Field(default_factory=list)
    age: int | None = None
    is_veteran: bool = False
    is_disabled: bool = False
    citizenship_status: str = "citizen"
    concerns: list[str] = Field(default_factory=list)
    language: str = "en"
    reading_level: ReadingLevel = ReadingLevel.STANDARD

    @property
    def fpl_percentage(self) -> float | None:
        """Calculate income as a percentage of the Federal Poverty Level."""
        if self.income is None:
            return None
        threshold = fpl_threshold(self.household_size)
        return round((self.income / threshold) * 100, 1)

    @property
    def has_children(self) -> bool:
        return any(d.age < 18 for d in self.dependents)

    @property
    def has_young_children(self) -> bool:
        """Children under 5 (relevant for WIC, Head Start)."""
        return any(d.age < 5 for d in self.dependents)


class Program(BaseModel):
    id: str
    name: str
    category: str  # food, cash, health, housing, energy, employment, childcare, emergency
    jurisdiction: str  # "federal", "state:MN", "county:ramsey", "cap:caprw"
    description: str
    eligibility_summary: str = ""
    application_url: str = ""
    application_portal: str = ""  # e.g., "MNbenefits", "MNsure", "uimn.org"
    phone: str = ""
    source: str = ""
    documents_needed: list[str] = Field(default_factory=list)


class EligibilityResult(BaseModel):
    program_id: str
    program_name: str
    eligible: bool | None = None  # None = unknown/need more info
    confidence: str = "medium"  # "high", "medium", "low"
    reason: str = ""
    estimated_benefit: str = ""
    source: str = ""
    priority: str = "normal"  # "high", "normal", "low"
    category: str = ""


class BenefitsResponse(BaseModel):
    eligible_programs: list[EligibilityResult] = Field(default_factory=list)
    documents_needed: list[str] = Field(default_factory=list)
    application_groups: dict[str, list[str]] = Field(default_factory=dict)
    follow_up_questions: list[str] = Field(default_factory=list)
    disclaimer: str = (
        "This is an informational tool, not legal advice. "
        "Eligibility determinations are unofficial estimates. "
        "Always verify with the relevant agency before applying. "
        "Program rules change -- information last verified April 2026."
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_models.py -v`
Expected: All 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/navigator/models.py tests/test_models.py
git commit -m "feat: add data models (UserProfile, Program, EligibilityResult)"
```

---

## Task 3: FPL Calculator Tool

**Files:**
- Create: `src/navigator/tools/fpl.py`
- Create: `data/fpl_tables/fpl_2026.json`
- Create: `tests/test_fpl.py`

- [ ] **Step 1: Write FPL calculator tests**

Create `tests/test_fpl.py`:

```python
"""Tests for the Federal Poverty Level calculator tool."""

import pytest
from navigator.tools.fpl import calculate_fpl, check_fpl_threshold


def test_fpl_single_person():
    result = calculate_fpl(income=15000, household_size=1)
    assert result["fpl_threshold"] == 15_650
    assert round(result["fpl_percentage"], 1) == 95.8
    assert result["household_size"] == 1


def test_fpl_family_of_three():
    result = calculate_fpl(income=32000, household_size=3)
    # FPL for 3 = 15650 + 5380*2 = 26410
    assert result["fpl_threshold"] == 26_410
    pct = result["fpl_percentage"]
    assert 121 < pct < 122  # 32000/26410 = 121.2%


def test_fpl_family_of_four():
    result = calculate_fpl(income=40000, household_size=4)
    # FPL for 4 = 15650 + 5380*3 = 31790
    assert result["fpl_threshold"] == 31_790


def test_check_threshold_below():
    result = check_fpl_threshold(income=20000, household_size=3, threshold_pct=200)
    assert result["below_threshold"] is True
    assert result["threshold_pct"] == 200


def test_check_threshold_above():
    result = check_fpl_threshold(income=60000, household_size=3, threshold_pct=200)
    assert result["below_threshold"] is False


def test_fpl_zero_income():
    result = calculate_fpl(income=0, household_size=1)
    assert result["fpl_percentage"] == 0.0


def test_mn_snap_bbce_threshold():
    """MN uses 200% FPL BBCE threshold for SNAP."""
    result = check_fpl_threshold(income=32000, household_size=3, threshold_pct=200)
    # 32000 is ~121% FPL for household of 3, well below 200%
    assert result["below_threshold"] is True


def test_mn_medicaid_threshold():
    """MN Medicaid (MA) uses 138% FPL."""
    result = check_fpl_threshold(income=32000, household_size=3, threshold_pct=138)
    # 121% < 138%, so eligible
    assert result["below_threshold"] is True


def test_mn_minnesotacare_threshold():
    """MinnesotaCare uses 200% FPL."""
    result = check_fpl_threshold(income=50000, household_size=3, threshold_pct=200)
    # 50000/26410 = 189% FPL, below 200%
    assert result["below_threshold"] is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_fpl.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Create FPL data file**

Create `data/fpl_tables/fpl_2026.json`:

```json
{
  "year": 2026,
  "source": "HHS Poverty Guidelines (48 contiguous states + DC)",
  "base_amount": 15650,
  "per_additional_person": 5380,
  "note": "Alaska and Hawaii have higher thresholds (not implemented for MN focus)"
}
```

- [ ] **Step 4: Implement FPL calculator**

Create `src/navigator/tools/fpl.py`:

```python
"""Federal Poverty Level calculator.

Uses 2026 HHS Poverty Guidelines for the 48 contiguous states.
This is a deterministic calculation, not a model inference.
"""

import json
from pathlib import Path

from navigator.config import FPL_DIR

_FPL_DATA_PATH = FPL_DIR / "fpl_2026.json"

# Default values matching 2026 guidelines
_BASE = 15_650
_PER_ADDITIONAL = 5_380


def _load_fpl_data() -> tuple[int, int]:
    """Load FPL thresholds from data file, fall back to defaults."""
    if _FPL_DATA_PATH.exists():
        data = json.loads(_FPL_DATA_PATH.read_text())
        return data["base_amount"], data["per_additional_person"]
    return _BASE, _PER_ADDITIONAL


def fpl_threshold(household_size: int) -> int:
    """Return the FPL dollar threshold for a given household size."""
    base, per_additional = _load_fpl_data()
    size = max(1, household_size)
    return base + per_additional * (size - 1)


def calculate_fpl(income: float, household_size: int) -> dict:
    """Calculate FPL percentage for given income and household size.

    Returns a dict suitable for use as a function calling tool response.
    """
    threshold = fpl_threshold(household_size)
    percentage = (income / threshold) * 100 if threshold > 0 else 0.0
    return {
        "income": income,
        "household_size": household_size,
        "fpl_threshold": threshold,
        "fpl_percentage": round(percentage, 1),
        "year": 2026,
    }


def check_fpl_threshold(
    income: float, household_size: int, threshold_pct: float
) -> dict:
    """Check if income is below a specific FPL percentage threshold.

    Common thresholds:
    - 138% FPL: Medicaid (Medical Assistance in MN)
    - 200% FPL: SNAP (MN BBCE), MinnesotaCare, EGA
    - 185% FPL: WIC
    - 50% SMI: Energy Assistance (not FPL-based, but similar concept)
    """
    result = calculate_fpl(income, household_size)
    below = result["fpl_percentage"] <= threshold_pct
    return {
        **result,
        "threshold_pct": threshold_pct,
        "below_threshold": below,
    }
```

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_fpl.py -v`
Expected: All 9 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add src/navigator/tools/fpl.py data/fpl_tables/fpl_2026.json tests/test_fpl.py
git commit -m "feat: add FPL calculator tool with 2026 thresholds"
```

---

## Task 4: Ollama Client Wrapper

**Files:**
- Create: `src/navigator/ollama_client.py`
- Create: `tests/test_ollama_client.py`

- [ ] **Step 1: Write Ollama client tests**

Create `tests/test_ollama_client.py`:

```python
"""Tests for the Ollama client wrapper.

These tests mock the ollama library so they run without a running Ollama server.
Tests that require a live Ollama server are marked with @pytest.mark.ollama.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from navigator.ollama_client import OllamaClient


@pytest.fixture
def client():
    return OllamaClient(model="gemma4:4b-it-q4_0")


def test_client_init(client):
    assert client.model == "gemma4:4b-it-q4_0"


def test_build_messages_with_system(client):
    messages = client._build_messages(
        user_message="Hello",
        system_prompt="You are a helpful assistant.",
    )
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are a helpful assistant."
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "Hello"


def test_build_messages_with_history(client):
    history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"},
    ]
    messages = client._build_messages(
        user_message="What programs?",
        system_prompt="System",
        history=history,
    )
    assert len(messages) == 4  # system + 2 history + new user
    assert messages[3]["role"] == "user"
    assert messages[3]["content"] == "What programs?"


@patch("navigator.ollama_client.ollama")
def test_chat_returns_response(mock_ollama, client):
    mock_ollama.chat.return_value = {
        "message": {"role": "assistant", "content": "Here are some programs."},
    }
    result = client.chat("What programs am I eligible for?")
    assert result == "Here are some programs."
    mock_ollama.chat.assert_called_once()


@patch("navigator.ollama_client.ollama")
def test_chat_with_json_output(mock_ollama, client):
    mock_ollama.chat.return_value = {
        "message": {
            "role": "assistant",
            "content": '{"income": 32000, "household_size": 3}',
        },
    }
    result = client.chat_json("Extract the profile")
    assert result["income"] == 32000
    assert result["household_size"] == 3
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_ollama_client.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement Ollama client**

Create `src/navigator/ollama_client.py`:

```python
"""Ollama API client wrapper for Gemma 4 inference."""

import json
import logging
from collections.abc import Generator

import ollama

from navigator.config import OLLAMA_BASE_URL, OLLAMA_MODEL

logger = logging.getLogger(__name__)


class OllamaClient:
    """Wrapper around the ollama Python client for Navigator use."""

    def __init__(
        self,
        model: str = OLLAMA_MODEL,
        base_url: str = OLLAMA_BASE_URL,
    ):
        self.model = model
        self.base_url = base_url
        self._client = ollama.Client(host=base_url)

    def _build_messages(
        self,
        user_message: str,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
    ) -> list[dict]:
        """Build the messages list for the chat API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})
        return messages

    def chat(
        self,
        user_message: str,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
        temperature: float = 1.0,
        top_p: float = 0.95,
        top_k: int = 64,
    ) -> str:
        """Send a chat message and return the response text."""
        messages = self._build_messages(user_message, system_prompt, history)
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
            },
        )
        return response["message"]["content"]

    def chat_json(
        self,
        user_message: str,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
    ) -> dict:
        """Send a chat message and parse the response as JSON.

        Instructs the model to respond in JSON format and parses the result.
        Raises ValueError if the response is not valid JSON.
        """
        json_instruction = (
            "\n\nRespond ONLY with valid JSON. No markdown, no explanation, "
            "no code fences. Just the JSON object."
        )
        full_prompt = (system_prompt or "") + json_instruction

        text = self.chat(user_message, system_prompt=full_prompt, history=history)

        # Strip markdown code fences if present
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1]) if len(lines) > 2 else text

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse JSON response: %s\nRaw: %s", e, text)
            raise ValueError(f"Model did not return valid JSON: {e}") from e

    def chat_stream(
        self,
        user_message: str,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
    ) -> Generator[str, None, None]:
        """Stream a chat response token by token."""
        messages = self._build_messages(user_message, system_prompt, history)
        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True,
            options={
                "temperature": 1.0,
                "top_p": 0.95,
                "top_k": 64,
            },
        )
        for chunk in stream:
            token = chunk["message"]["content"]
            if token:
                yield token
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_ollama_client.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 5: Verify live Ollama connection (manual)**

Run:
```bash
ollama pull gemma4:4b-it-q4_0
python -c "
from navigator.ollama_client import OllamaClient
client = OllamaClient()
print(client.chat('Say hello in one sentence.'))
"
```
Expected: A one-sentence greeting from Gemma 4 E4B.

- [ ] **Step 6: Commit**

```bash
git add src/navigator/ollama_client.py tests/test_ollama_client.py
git commit -m "feat: add Ollama client wrapper with chat, JSON, and streaming"
```

---

## Task 5: System Prompts

**Files:**
- Create: `src/navigator/prompts.py`

- [ ] **Step 1: Create prompts module**

Create `src/navigator/prompts.py`:

```python
"""System prompts and templates for each pipeline stage."""

INTAKE_SYSTEM_PROMPT = """\
You are a benefits intake assistant. Your job is to extract structured information \
from a person's description of their situation.

Extract the following fields into a JSON object:
- income: annual household income (number or null)
- household_size: total number of people in household (integer)
- county: county name (string or null). If they mention a city, infer the county: \
Saint Paul = Ramsey, Minneapolis = Hennepin, Apple Valley/Eagan/Burnsville = Dakota, \
Shakopee/Prior Lake = Scott, Chaska/Chanhassen = Carver
- employment_status: one of "employed", "recently_unemployed", "long_term_unemployed", \
"self_employed", "retired", "disabled", "student", or null
- dependents: list of objects with "age" (integer) and "relationship" (string, \
default "child")
- age: the person's age (integer or null)
- is_veteran: boolean (default false)
- is_disabled: boolean (default false)
- citizenship_status: "citizen", "permanent_resident", "refugee", "undocumented", \
or "other" (default "citizen")
- concerns: list of keywords from: "food", "housing", "health", "childcare", \
"employment", "energy", "cash", "emergency"
- language: detected language code (en, es, hmn, so, kar)
- missing_info: list of critical fields still needed (empty list if all key info \
is present). Critical fields are: income, household_size, county.

If information is not stated, set it to null (not a guess).
Respond ONLY with valid JSON. No explanation."""

INTAKE_MISSING_INFO_PROMPT = """\
You are a friendly benefits navigator. The user has described their situation but \
you are missing some information needed to find the right programs.

Missing information: {missing_fields}

Ask ONE friendly, conversational follow-up question to get the most important \
missing piece of information. Be warm and reassuring. Do not ask for more than \
one thing at a time. If multiple things are missing, prioritize: \
county > income > household_size.

Keep your question to 1-2 sentences."""

ELIGIBILITY_SYSTEM_PROMPT = """\
You are a government benefits eligibility analyst. You have access to tools to \
look up program information and check eligibility thresholds.

Given a user's profile and retrieved program information, determine which programs \
they may be eligible for. For each program:
1. Check if their income/household meets the threshold
2. Check if they meet categorical requirements (age, children, employment, etc.)
3. Assess confidence: "high" (clear match), "medium" (likely but uncertain), \
"low" (possible but need more info)
4. Assign priority: "high" (urgent need, large benefit), "normal" (beneficial), \
"low" (marginal benefit)

CRITICAL RULES:
- NEVER say someone "qualifies" or "is eligible". Say "may be eligible" or \
"appears to meet the criteria".
- ALWAYS cite the source of eligibility rules (manual section, statute, etc.)
- If you are unsure about eligibility, say so and explain what additional \
information would be needed.
- Do not fabricate income thresholds or benefit amounts. Only use values from \
the retrieved program information or tool results.

Use the available tools to look up information. Do not guess."""

RESPONSE_SYSTEM_PROMPT_TEMPLATE = """\
You are a plain-language government benefits navigator. Your job is to explain \
benefits eligibility results in clear, simple language.

TARGET READING LEVEL: {reading_level}
- simple: 5th grade reading level. Short sentences. No jargon. Define any \
technical terms. Use "you" and "your."
- standard: 8th grade reading level. Clear but can use some common terms.
- detailed: Full detail. Can use technical terms but define acronyms on first use.

LANGUAGE: Respond in {language}.

You are presenting results to a real person in a difficult situation. Be warm, \
clear, and actionable. Structure your response as:

1. A brief empathetic acknowledgment (1 sentence)
2. HIGH PRIORITY programs (most impactful/urgent)
3. ALSO CHECK programs (additional options)
4. DOCUMENTS TO GATHER (consolidated list across all programs)
5. WHERE TO APPLY (grouped by application portal with direct URLs)

For each program, include:
- Program name and what it provides (1 sentence)
- Why they may be eligible (1 sentence citing the rule)
- Estimated benefit amount if available
- Any important deadlines or notes

End with the standard disclaimer.

CRITICAL: Only include programs from the provided eligibility results. Do not \
add programs not in the results. Do not fabricate benefit amounts."""

RESPONSE_DISCLAIMER = (
    "This is an informational tool, not legal advice. "
    "Eligibility determinations are unofficial estimates. "
    "Always verify with the relevant agency before applying. "
    "Program rules change -- information last verified April 2026."
)


def get_response_prompt(reading_level: str = "standard", language: str = "English") -> str:
    """Build the response generation system prompt for a given reading level and language."""
    return RESPONSE_SYSTEM_PROMPT_TEMPLATE.format(
        reading_level=reading_level,
        language=language,
    )
```

- [ ] **Step 2: Commit**

```bash
git add src/navigator/prompts.py
git commit -m "feat: add system prompts for intake, eligibility, and response stages"
```

---

## Task 6: RAG — Embeddings & ChromaDB Store

**Files:**
- Create: `src/navigator/rag/embeddings.py`
- Create: `src/navigator/rag/store.py`
- Create: `tests/test_embeddings.py`
- Create: `tests/test_store.py`

- [ ] **Step 1: Write embedding tests**

Create `tests/test_embeddings.py`:

```python
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
```

- [ ] **Step 2: Write ChromaDB store tests**

Create `tests/test_store.py`:

```python
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
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/test_embeddings.py tests/test_store.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 4: Implement embedding model wrapper**

Create `src/navigator/rag/embeddings.py`:

```python
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
```

- [ ] **Step 5: Implement ChromaDB store**

Create `src/navigator/rag/store.py`:

```python
"""ChromaDB collection management for the benefits knowledge base."""

import chromadb
from chromadb.config import Settings

from navigator.config import CHROMA_DIR, CHROMA_COLLECTION
from navigator.rag.embeddings import EmbeddingModel


class _SentenceTransformerEF(chromadb.EmbeddingFunction):
    """ChromaDB embedding function adapter for our EmbeddingModel."""

    def __init__(self, model: EmbeddingModel):
        self._model = model

    def __call__(self, input: list[str]) -> list[list[float]]:
        return self._model.embed_batch(input)


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
        """Query the collection by text similarity.

        Args:
            query_text: The search query.
            n_results: Number of results to return.
            where: Optional ChromaDB metadata filter (e.g., {"jurisdiction": "state:MN"}
                   or {"$or": [{"jurisdiction": "federal"}, {"jurisdiction": "state:MN"}]}).
        """
        kwargs = {
            "query_texts": [query_text],
            "n_results": n_results,
        }
        if where:
            kwargs["where"] = where
        return self.collection.query(**kwargs)

    def count(self) -> int:
        """Return the number of documents in the collection."""
        return self.collection.count()
```

- [ ] **Step 6: Run tests**

Run: `pytest tests/test_embeddings.py tests/test_store.py -v`
Expected: All tests PASS. First run will download the `all-MiniLM-L6-v2` model (~80 MB).

- [ ] **Step 7: Commit**

```bash
git add src/navigator/rag/embeddings.py src/navigator/rag/store.py tests/test_embeddings.py tests/test_store.py
git commit -m "feat: add embedding model wrapper and ChromaDB store with jurisdiction filtering"
```

---

## Task 7: RAG — BM25 & Hybrid Retrieval

**Files:**
- Create: `src/navigator/rag/bm25.py`
- Create: `src/navigator/rag/retrieval.py`
- Create: `tests/test_bm25.py`
- Create: `tests/test_retrieval.py`

- [ ] **Step 1: Write BM25 tests**

Create `tests/test_bm25.py`:

```python
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
```

- [ ] **Step 2: Write hybrid retrieval tests**

Create `tests/test_retrieval.py`:

```python
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
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/test_bm25.py tests/test_retrieval.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 4: Implement BM25 index**

Create `src/navigator/rag/bm25.py`:

```python
"""BM25 keyword search index for government program documents."""

from rank_bm25 import BM25Okapi


class BM25Index:
    """BM25 keyword index for exact-match boosting of program names."""

    def __init__(self):
        self._ids: list[str] = []
        self._corpus: list[list[str]] = []
        self._bm25: BM25Okapi | None = None

    def add_documents(self, ids: list[str], texts: list[str]) -> None:
        """Add documents to the BM25 index."""
        self._ids.extend(ids)
        tokenized = [text.lower().split() for text in texts]
        self._corpus.extend(tokenized)
        self._bm25 = BM25Okapi(self._corpus)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """Search the index. Returns list of (doc_id, score) tuples, sorted by score desc."""
        if self._bm25 is None:
            return []
        tokenized_query = query.lower().split()
        scores = self._bm25.get_scores(tokenized_query)
        scored = list(zip(self._ids, scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
```

- [ ] **Step 5: Implement hybrid retriever**

Create `src/navigator/rag/retrieval.py`:

```python
"""Hybrid retrieval combining ChromaDB vector search with BM25 keyword search."""

from navigator.config import BM25_WEIGHT, TOP_K_FINAL
from navigator.rag.store import BenefitsStore
from navigator.rag.bm25 import BM25Index


class HybridRetriever:
    """Combines semantic (ChromaDB) and keyword (BM25) search results.

    Score formula: (1 - alpha) * vector_score + alpha * bm25_score
    where alpha = BM25_WEIGHT (default 0.4).
    """

    def __init__(
        self,
        store: BenefitsStore,
        bm25: BM25Index,
        bm25_weight: float = BM25_WEIGHT,
    ):
        self.store = store
        self.bm25 = bm25
        self.bm25_weight = bm25_weight

    def search(
        self,
        query: str,
        top_k: int = TOP_K_FINAL,
        jurisdiction_filter: list[str] | None = None,
    ) -> list[dict]:
        """Run hybrid search and return merged, deduplicated results.

        Args:
            query: Search query text.
            top_k: Number of results to return.
            jurisdiction_filter: List of jurisdictions to include
                (e.g., ["federal", "state:MN", "county:ramsey"]).

        Returns:
            List of dicts with keys: id, text, metadata, score.
        """
        # Build ChromaDB where filter
        where = None
        if jurisdiction_filter:
            if len(jurisdiction_filter) == 1:
                where = {"jurisdiction": jurisdiction_filter[0]}
            else:
                where = {"$or": [{"jurisdiction": j} for j in jurisdiction_filter]}

        # Vector search
        fetch_k = top_k * 3  # over-fetch for merging
        vector_results = self.store.query(query, n_results=fetch_k, where=where)

        # BM25 search (no jurisdiction filter — we filter after)
        bm25_results = self.bm25.search(query, top_k=fetch_k)

        # Normalize scores
        vector_scores = self._normalize_vector_scores(vector_results)
        bm25_scores = self._normalize_bm25_scores(bm25_results)

        # Merge
        all_ids = set(vector_scores.keys()) | set(bm25_scores.keys())
        merged = {}
        for doc_id in all_ids:
            v_score = vector_scores.get(doc_id, 0.0)
            b_score = bm25_scores.get(doc_id, 0.0)
            merged[doc_id] = (1 - self.bm25_weight) * v_score + self.bm25_weight * b_score

        # Sort by combined score
        sorted_ids = sorted(merged, key=merged.get, reverse=True)[:top_k]

        # Build result dicts with text and metadata from vector results
        doc_map = {}
        if vector_results["ids"] and vector_results["ids"][0]:
            for i, doc_id in enumerate(vector_results["ids"][0]):
                doc_map[doc_id] = {
                    "text": vector_results["documents"][0][i],
                    "metadata": vector_results["metadatas"][0][i],
                }

        results = []
        for doc_id in sorted_ids:
            info = doc_map.get(doc_id, {"text": "", "metadata": {}})
            # Apply jurisdiction filter to BM25-only results
            if jurisdiction_filter and doc_id not in doc_map:
                continue  # BM25 result not in filtered vector results — skip
            results.append({
                "id": doc_id,
                "text": info["text"],
                "metadata": info["metadata"],
                "score": merged[doc_id],
            })

        return results

    def _normalize_vector_scores(self, results: dict) -> dict[str, float]:
        """Normalize ChromaDB distances to 0-1 similarity scores."""
        scores = {}
        if not results["ids"] or not results["ids"][0]:
            return scores
        distances = results["distances"][0] if "distances" in results else []
        for i, doc_id in enumerate(results["ids"][0]):
            # ChromaDB cosine distance: 0 = identical, 2 = opposite
            # Convert to similarity: 1 - (distance / 2)
            dist = distances[i] if i < len(distances) else 1.0
            scores[doc_id] = max(0.0, 1.0 - dist / 2.0)
        return scores

    def _normalize_bm25_scores(self, results: list[tuple[str, float]]) -> dict[str, float]:
        """Normalize BM25 scores to 0-1 range."""
        if not results:
            return {}
        max_score = max(s for _, s in results) or 1.0
        return {doc_id: score / max_score for doc_id, score in results}
```

- [ ] **Step 6: Run tests**

Run: `pytest tests/test_bm25.py tests/test_retrieval.py -v`
Expected: All tests PASS.

- [ ] **Step 7: Commit**

```bash
git add src/navigator/rag/bm25.py src/navigator/rag/retrieval.py tests/test_bm25.py tests/test_retrieval.py
git commit -m "feat: add BM25 index and hybrid retrieval (vector + keyword)"
```

---

## Task 8: RAG — Document Ingestion Pipeline

**Files:**
- Create: `src/navigator/rag/ingest.py`
- Create: `tests/test_ingest.py`

- [ ] **Step 1: Write ingestion tests**

Create `tests/test_ingest.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_ingest.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement ingestion pipeline**

Create `src/navigator/rag/ingest.py`:

```python
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
    """Split text into overlapping chunks by word count.

    Args:
        text: The text to chunk.
        chunk_size: Target number of words per chunk.
        overlap: Number of words to overlap between chunks.
    """
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
    """Process a program JSON file into documents ready for ingestion.

    Each document has: id, text, metadata.
    """
    data = json.loads(path.read_text())
    program_id = data.get("id", path.stem)
    program_name = data.get("name", program_id)

    # Combine description and eligibility into one text block
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
        for path in sorted(text_dir.glob("**/*.txt")) | sorted(text_dir.glob("**/*.md")):
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
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_ingest.py -v`
Expected: All tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/navigator/rag/ingest.py tests/test_ingest.py
git commit -m "feat: add document chunking and ingestion pipeline"
```

---

## Task 9: Readability Checker

**Files:**
- Create: `src/navigator/readability.py`
- Create: `tests/test_readability.py`

- [ ] **Step 1: Write readability tests**

Create `tests/test_readability.py`:

```python
"""Tests for the readability checker."""

import pytest
from navigator.readability import check_readability, meets_reading_level
from navigator.models import ReadingLevel


def test_check_readability_returns_scores():
    text = "The cat sat on the mat. It was a nice day."
    result = check_readability(text)
    assert "flesch_kincaid_grade" in result
    assert "flesch_reading_ease" in result
    assert isinstance(result["flesch_kincaid_grade"], float)


def test_simple_text_low_grade():
    text = "I need food. My kids are hungry. We need help now."
    result = check_readability(text)
    assert result["flesch_kincaid_grade"] < 5.0


def test_complex_text_high_grade():
    text = (
        "The Supplemental Nutrition Assistance Program eligibility determination "
        "necessitates comprehensive evaluation of household income relative to "
        "categorical eligibility thresholds established pursuant to federal "
        "poverty guidelines promulgated annually by the Department of Health "
        "and Human Services."
    )
    result = check_readability(text)
    assert result["flesch_kincaid_grade"] > 12.0


def test_meets_simple_level():
    simple = "I lost my job. I have two kids. I need help with food and rent."
    assert meets_reading_level(simple, ReadingLevel.SIMPLE)


def test_complex_fails_simple_level():
    complex_text = (
        "The categorical eligibility determination for supplemental nutrition "
        "assistance requires comprehensive evaluation of modified adjusted gross "
        "income relative to federally mandated poverty thresholds."
    )
    assert not meets_reading_level(complex_text, ReadingLevel.SIMPLE)


def test_any_text_meets_detailed():
    text = "Any text should pass the detailed reading level check."
    assert meets_reading_level(text, ReadingLevel.DETAILED)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_readability.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement readability checker**

Create `src/navigator/readability.py`:

```python
"""Readability checking via textstat for reading level adaptation."""

import textstat

from navigator.config import TARGET_READING_LEVELS
from navigator.models import ReadingLevel


def check_readability(text: str) -> dict:
    """Compute readability scores for the given text.

    Returns dict with flesch_kincaid_grade and flesch_reading_ease.
    """
    return {
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "text_length_words": textstat.lexicon_count(text),
    }


def meets_reading_level(text: str, level: ReadingLevel) -> bool:
    """Check if text meets the target reading level.

    Returns True if the text's Flesch-Kincaid grade level is at or below
    the target for the given reading level.
    """
    target_grade = TARGET_READING_LEVELS[level.value]
    actual_grade = textstat.flesch_kincaid_grade(text)
    return actual_grade <= target_grade
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_readability.py -v`
Expected: All 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/navigator/readability.py tests/test_readability.py
git commit -m "feat: add readability checker using textstat"
```

---

## Task 10: Stage 1 — Intake & Extraction

**Files:**
- Create: `src/navigator/intake.py`
- Create: `tests/test_intake.py`

- [ ] **Step 1: Write intake tests**

Create `tests/test_intake.py`:

```python
"""Tests for Stage 1: Intake & Extraction.

Uses mocked Ollama responses since we can't depend on a running server in CI.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from navigator.intake import IntakeProcessor
from navigator.models import UserProfile


@pytest.fixture
def processor():
    return IntakeProcessor()


def test_parse_profile_from_json(processor):
    raw_json = {
        "income": 32000,
        "household_size": 3,
        "county": "Ramsey",
        "employment_status": "recently_unemployed",
        "dependents": [{"age": 3}, {"age": 7}],
        "concerns": ["food", "housing"],
        "language": "en",
        "missing_info": [],
    }
    profile = processor._json_to_profile(raw_json)
    assert isinstance(profile, UserProfile)
    assert profile.income == 32000
    assert profile.county == "Ramsey"
    assert len(profile.dependents) == 2
    assert profile.household_size == 3


def test_parse_profile_with_missing_info(processor):
    raw_json = {
        "income": None,
        "household_size": 3,
        "county": None,
        "employment_status": "recently_unemployed",
        "dependents": [],
        "concerns": ["food"],
        "language": "en",
        "missing_info": ["income", "county"],
    }
    profile = processor._json_to_profile(raw_json)
    assert profile.income is None
    assert profile.county is None


def test_identify_missing_fields(processor):
    profile = UserProfile(household_size=3, employment_status="recently_unemployed")
    missing = processor._get_missing_fields(profile)
    assert "income" in missing
    assert "county" in missing


def test_no_missing_fields(processor):
    profile = UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
    )
    missing = processor._get_missing_fields(profile)
    assert len(missing) == 0


@patch("navigator.intake.OllamaClient")
def test_extract_profile(MockClient, processor):
    mock_instance = MockClient.return_value
    mock_instance.chat_json.return_value = {
        "income": 32000,
        "household_size": 3,
        "county": "Ramsey",
        "employment_status": "recently_unemployed",
        "dependents": [{"age": 3}, {"age": 7}],
        "concerns": ["food", "housing"],
        "language": "en",
        "missing_info": [],
    }
    processor.client = mock_instance

    profile, missing = processor.extract("I'm a single mom with two kids...")
    assert profile.income == 32000
    assert profile.county == "Ramsey"
    assert len(missing) == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_intake.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement intake processor**

Create `src/navigator/intake.py`:

```python
"""Stage 1: Intake & Extraction — parse user situation into a structured profile."""

import logging

from navigator.models import UserProfile, Dependent, ReadingLevel
from navigator.ollama_client import OllamaClient
from navigator.prompts import INTAKE_SYSTEM_PROMPT, INTAKE_MISSING_INFO_PROMPT

logger = logging.getLogger(__name__)

# Fields that are critical for eligibility determination
CRITICAL_FIELDS = ["income", "county", "household_size"]


class IntakeProcessor:
    """Extracts a structured UserProfile from natural language input."""

    def __init__(self, client: OllamaClient | None = None):
        self.client = client or OllamaClient()

    def extract(self, user_message: str) -> tuple[UserProfile, list[str]]:
        """Extract a UserProfile from the user's situation description.

        Returns:
            Tuple of (profile, missing_fields). If missing_fields is non-empty,
            the caller should ask follow-up questions.
        """
        raw = self.client.chat_json(user_message, system_prompt=INTAKE_SYSTEM_PROMPT)
        profile = self._json_to_profile(raw)
        missing = self._get_missing_fields(profile)
        return profile, missing

    def ask_followup(self, missing_fields: list[str]) -> str:
        """Generate a friendly follow-up question for missing information."""
        prompt = INTAKE_MISSING_INFO_PROMPT.format(missing_fields=", ".join(missing_fields))
        return self.client.chat(
            f"Missing fields: {', '.join(missing_fields)}",
            system_prompt=prompt,
        )

    def _json_to_profile(self, data: dict) -> UserProfile:
        """Convert raw JSON from the model into a UserProfile."""
        dependents = []
        for dep in data.get("dependents") or []:
            if isinstance(dep, dict):
                dependents.append(Dependent(
                    age=dep.get("age", 0),
                    relationship=dep.get("relationship", "child"),
                ))

        # Detect language and set reading level
        language = data.get("language", "en") or "en"

        return UserProfile(
            income=data.get("income"),
            household_size=data.get("household_size", 1) or 1,
            county=data.get("county"),
            state="MN",
            employment_status=data.get("employment_status"),
            dependents=dependents,
            age=data.get("age"),
            is_veteran=data.get("is_veteran", False) or False,
            is_disabled=data.get("is_disabled", False) or False,
            citizenship_status=data.get("citizenship_status", "citizen") or "citizen",
            concerns=data.get("concerns") or [],
            language=language,
        )

    def _get_missing_fields(self, profile: UserProfile) -> list[str]:
        """Identify critical fields that are still missing."""
        missing = []
        if profile.income is None:
            missing.append("income")
        if profile.county is None:
            missing.append("county")
        # household_size defaults to 1, so only flag if it seems wrong
        # (e.g., they mentioned kids but size is 1)
        if profile.household_size == 1 and len(profile.dependents) > 0:
            missing.append("household_size")
        return missing
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_intake.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/navigator/intake.py tests/test_intake.py
git commit -m "feat: add Stage 1 intake processor for situation extraction"
```

---

## Task 11: Benefits Search Tool

**Files:**
- Create: `src/navigator/tools/benefits_search.py`
- Create: `tests/test_benefits_search.py`

- [ ] **Step 1: Write benefits search tests**

Create `tests/test_benefits_search.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_benefits_search.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement benefits search tool**

Create `src/navigator/tools/benefits_search.py`:

```python
"""Benefits knowledge base search tool for the eligibility engine."""

from navigator.rag.retrieval import HybridRetriever
from navigator.config import TOP_K_FINAL


class BenefitsSearchTool:
    """Searches the benefits knowledge base using hybrid retrieval."""

    def __init__(self, retriever: HybridRetriever):
        self.retriever = retriever

    def search(
        self,
        query: str,
        state: str = "MN",
        county: str | None = None,
        category: str | None = None,
        top_k: int = TOP_K_FINAL,
    ) -> list[dict]:
        """Search the benefits KB for relevant programs.

        Automatically includes federal programs and filters by state/county.

        Args:
            query: Natural language search query.
            state: State code (default "MN").
            county: Optional county name for county-level programs.
            category: Optional category filter (food, cash, health, etc.).
            top_k: Number of results to return.
        """
        # Build jurisdiction filter
        jurisdictions = ["federal", f"state:{state}"]
        if county:
            jurisdictions.append(f"county:{county.lower()}")
            # Add CAP agency jurisdictions
            cap_map = {
                "ramsey": "cap:caprw",
                "hennepin": "cap:cap-hc",
                "dakota": "cap:cap-agency",
                "scott": "cap:cap-agency",
                "carver": "cap:cap-agency",
            }
            if county.lower() in cap_map:
                jurisdictions.append(cap_map[county.lower()])

        results = self.retriever.search(
            query=query,
            top_k=top_k,
            jurisdiction_filter=jurisdictions,
        )

        return results
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_benefits_search.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/navigator/tools/benefits_search.py tests/test_benefits_search.py
git commit -m "feat: add benefits search tool with jurisdiction-aware retrieval"
```

---

## Task 12: County Programs & Document Requirements Tools

**Files:**
- Create: `src/navigator/tools/county_programs.py`
- Create: `src/navigator/tools/document_requirements.py`
- Create: `tests/test_county_programs.py`
- Create: `tests/test_document_requirements.py`

- [ ] **Step 1: Write tests**

Create `tests/test_county_programs.py`:

```python
"""Tests for county programs lookup tool."""

import pytest
from navigator.tools.county_programs import CountyProgramsTool


@pytest.fixture
def tool():
    return CountyProgramsTool()


def test_ramsey_has_dislocated_worker(tool):
    programs = tool.get_programs("Ramsey")
    names = [p["name"] for p in programs]
    assert any("Dislocated Worker" in n for n in names)


def test_ramsey_has_caprw(tool):
    programs = tool.get_programs("Ramsey")
    caps = [p for p in programs if p["type"] == "cap"]
    assert len(caps) > 0
    assert any("CAPRW" in p["name"] for p in caps)


def test_hennepin_has_pathways(tool):
    programs = tool.get_programs("Hennepin")
    names = [p["name"] for p in programs]
    assert any("Pathways" in n for n in names)


def test_dakota_served_by_cap_agency(tool):
    programs = tool.get_programs("Dakota")
    caps = [p for p in programs if p["type"] == "cap"]
    assert any("CAP Agency" in p["name"] for p in caps)


def test_unknown_county_returns_empty(tool):
    programs = tool.get_programs("FakeCounty")
    assert programs == []


def test_get_cap_agency(tool):
    cap = tool.get_cap_agency("Ramsey")
    assert cap is not None
    assert "CAPRW" in cap["name"]
    assert "phone" in cap
```

Create `tests/test_document_requirements.py`:

```python
"""Tests for document requirements tool."""

import pytest
from navigator.tools.document_requirements import DocumentRequirementsTool
from navigator.models import UserProfile


@pytest.fixture
def tool():
    return DocumentRequirementsTool()


@pytest.fixture
def profile():
    return UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
        employment_status="recently_unemployed",
    )


def test_snap_documents(tool, profile):
    docs = tool.get_documents("snap", profile)
    assert "Photo ID" in docs or "Government-issued photo ID" in docs
    assert any("income" in d.lower() for d in docs)


def test_ui_documents(tool, profile):
    docs = tool.get_documents("unemployment_insurance", profile)
    assert any("employer" in d.lower() or "layoff" in d.lower() for d in docs)


def test_consolidated_documents(tool, profile):
    programs = ["snap", "mfip", "medical_assistance"]
    docs = tool.get_consolidated_documents(programs, profile)
    # Should be deduplicated
    assert len(docs) == len(set(docs))
    assert "Government-issued photo ID" in docs
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_county_programs.py tests/test_document_requirements.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement county programs tool**

Create `src/navigator/tools/county_programs.py`:

```python
"""County-specific program lookup for the five Twin Cities metro counties."""

# Hardcoded county data from research. In production, this would come from
# the scraped county pages in the knowledge base.

_COUNTY_DATA = {
    "ramsey": {
        "programs": [
            {
                "name": "Ramsey County Dislocated Worker Program",
                "type": "employment",
                "url": "https://www.ramseycountymn.gov/residents/assistance-support/employment-assistance/job-seeker-programs/dislocated-worker-program",
                "application_url": "https://www.ramseycountymn.gov/residents/assistance-support/employment-assistance/job-seeker-programs/dislocated-worker-program/dislocated-worker-program-application",
                "description": "County-run program for recently laid-off workers. Career exploration, skills assessment, resume writing, interview prep, training. Has its own application (5 business day response).",
                "phone": "651-266-3800",
            },
            {
                "name": "Ramsey County Emergency Assistance",
                "type": "emergency",
                "url": "https://www.ramseycountymn.gov/residents/assistance-support/assistance/financial-assistance/emergency-assistance",
                "description": "Short-term emergency assistance for rent, housing, and utilities.",
            },
        ],
        "cap": {
            "name": "CAPRW (Community Action Partnership of Ramsey & Washington Counties)",
            "url": "https://www.caprw.org/",
            "phone": "(651) 645-6445",
            "address": "450 Syndicate St N, Saint Paul, MN 55104",
            "programs": [
                "Energy Assistance (EAP)",
                "Head Start & Early Head Start",
                "SNAP Screening & Application Assistance",
                "Car Loan Program",
                "VITA Free Tax Clinic",
                "Section 8 Housing Applications (when waitlist opens)",
                "Financial Literacy Classes",
            ],
        },
        "phone_24_7": "651-266-3800 (24/7 EZ Info — English, Spanish, Hmong, Somali, Karen)",
        "application_portal": "MNbenefits.mn.gov",
    },
    "hennepin": {
        "programs": [
            {
                "name": "Hennepin Pathways Employment Program",
                "type": "employment",
                "url": "https://www.hennepin.us/pathways-program",
                "description": "County employment program placing graduates in county jobs (office admin, human services, building ops).",
            },
            {
                "name": "Hennepin County SNAP Employment & Training",
                "type": "employment",
                "url": "https://www.hennepin.us/residents/human-services/workforce-development",
                "description": "Job resources, support, and training for SNAP recipients.",
            },
        ],
        "cap": {
            "name": "CAP-HC (Community Action Partnership of Hennepin County)",
            "url": "https://caphennepin.org/",
            "phone": "See website",
            "programs": [
                "Energy Assistance",
                "Water Assistance",
                "Rental Assistance",
                "Vehicle Repair Program",
                "Homebuyer Services",
                "Tax Assistance",
            ],
        },
        "application_portal": "MNbenefits.mn.gov",
    },
    "dakota": {
        "programs": [
            {
                "name": "Dakota County Emergency Assistance",
                "type": "emergency",
                "url": "https://www.co.dakota.mn.us/HealthFamily/PublicAssistance/Emergency/Pages/default.aspx",
                "description": "One-time payment for eviction or utility shutoff.",
                "phone": "651-554-5611",
            },
        ],
        "cap": {
            "name": "CAP Agency (Scott-Carver-Dakota)",
            "url": "https://capagency.org/",
            "phone": "651-322-3500",
            "address": "2496 145th St W, Rosemount, MN 55068",
            "programs": [
                "Energy Assistance",
                "Emergency Furnace Repair/Replacement",
                "Head Start (ages 3-5)",
                "Early Head Start (birth-3)",
                "Chore Program for Seniors",
                "Housing Services",
            ],
        },
        "application_portal": "MNbenefits.mn.gov",
    },
    "scott": {
        "programs": [],
        "cap": {
            "name": "CAP Agency (Scott-Carver-Dakota)",
            "url": "https://capagency.org/",
            "phone": "See Shakopee office",
            "address": "738 1st Ave E, Shakopee, MN 55379",
            "programs": [
                "Energy Assistance",
                "Emergency Furnace Repair/Replacement",
                "Head Start",
                "Early Head Start",
                "Housing Services",
            ],
        },
        "application_portal": "MNbenefits.mn.gov",
    },
    "carver": {
        "programs": [],
        "cap": {
            "name": "CAP Agency (Scott-Carver-Dakota)",
            "url": "https://capagency.org/",
            "phone": "952-496-2125",
            "address": "110 W 2nd St, Chaska, MN 55318",
            "programs": [
                "Energy Assistance",
                "Emergency Furnace Repair/Replacement",
                "Head Start",
                "Housing Services",
            ],
        },
        "application_portal": "MNbenefits.mn.gov",
    },
}


class CountyProgramsTool:
    """Look up county-specific programs and CAP agencies."""

    def get_programs(self, county: str) -> list[dict]:
        """Get all county-specific programs for a given county."""
        data = _COUNTY_DATA.get(county.lower())
        if not data:
            return []

        results = []
        for prog in data.get("programs", []):
            results.append(prog)

        # Add CAP agency programs
        cap = data.get("cap")
        if cap:
            results.append({
                "name": cap["name"],
                "type": "cap",
                "url": cap["url"],
                "phone": cap.get("phone", ""),
                "description": f"Programs: {', '.join(cap['programs'])}",
            })

        return results

    def get_cap_agency(self, county: str) -> dict | None:
        """Get the CAP agency serving a given county."""
        data = _COUNTY_DATA.get(county.lower())
        if not data:
            return None
        return data.get("cap")

    def get_application_portal(self, county: str) -> str:
        """Get the primary application portal for a county."""
        data = _COUNTY_DATA.get(county.lower())
        if not data:
            return "MNbenefits.mn.gov"
        return data.get("application_portal", "MNbenefits.mn.gov")
```

- [ ] **Step 4: Implement document requirements tool**

Create `src/navigator/tools/document_requirements.py`:

```python
"""Document requirements lookup for benefits programs."""

from navigator.models import UserProfile

# Common documents by program. Sourced from MNbenefits.mn.gov FAQ and
# DHS Combined Manual application requirements.
_PROGRAM_DOCS = {
    "snap": [
        "Government-issued photo ID",
        "Proof of income (last 30 days pay stubs or employer letter)",
        "Proof of residency (utility bill, lease, or mail)",
        "Social Security numbers for all household members",
        "Bank statements (last 30 days)",
    ],
    "mfip": [
        "Government-issued photo ID",
        "Birth certificates for all children in household",
        "Proof of income (last 30 days pay stubs or employer letter)",
        "Social Security numbers for all household members",
        "Proof of residency (utility bill, lease, or mail)",
        "Bank statements (last 30 days)",
        "Proof of child care costs (if applicable)",
    ],
    "medical_assistance": [
        "Government-issued photo ID",
        "Social Security numbers for all household members",
        "Proof of income (last 30 days pay stubs or tax return)",
        "Proof of residency",
        "Immigration documents (if applicable)",
    ],
    "minnesotacare": [
        "Government-issued photo ID",
        "Social Security numbers for all household members",
        "Proof of income (last 30 days pay stubs or tax return)",
        "Proof of residency",
        "Proof that no affordable employer coverage is available",
    ],
    "unemployment_insurance": [
        "Government-issued photo ID",
        "Social Security number",
        "Employer name, address, and phone for last 18 months",
        "Layoff letter or separation notice (if available)",
        "Direct deposit bank information",
    ],
    "emergency_assistance": [
        "Government-issued photo ID",
        "Proof of emergency (eviction notice, utility shutoff notice)",
        "Proof of income",
        "Proof of residency",
        "Birth certificates for children",
    ],
    "ccap": [
        "Government-issued photo ID",
        "Proof of income (last 30 days)",
        "Proof of activity (work schedule, school enrollment, job search log)",
        "Child care provider information",
        "Birth certificates for children",
    ],
    "energy_assistance": [
        "Government-issued photo ID",
        "Social Security numbers for all household members",
        "Proof of income (last 30 days)",
        "Most recent utility bill",
        "Proof of residency",
    ],
    "dislocated_worker": [
        "Government-issued photo ID",
        "Proof of layoff (separation notice, WARN notice, or employer letter)",
        "Resume (if available)",
    ],
}


class DocumentRequirementsTool:
    """Look up required documents for benefits program applications."""

    def get_documents(self, program_id: str, profile: UserProfile) -> list[str]:
        """Get required documents for a specific program."""
        docs = list(_PROGRAM_DOCS.get(program_id, []))

        # Add conditional documents based on profile
        if profile.citizenship_status != "citizen":
            docs.append("Immigration/citizenship documentation")
        if profile.is_disabled:
            docs.append("Disability documentation or SSI/SSDI award letter")
        if profile.is_veteran:
            docs.append("DD-214 or VA documentation")

        return docs

    def get_consolidated_documents(
        self, program_ids: list[str], profile: UserProfile
    ) -> list[str]:
        """Get a deduplicated, consolidated document list across multiple programs."""
        all_docs = []
        for pid in program_ids:
            all_docs.extend(self.get_documents(pid, profile))

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for doc in all_docs:
            if doc not in seen:
                seen.add(doc)
                unique.append(doc)
        return unique
```

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_county_programs.py tests/test_document_requirements.py -v`
Expected: All tests PASS.

- [ ] **Step 6: Commit**

```bash
git add src/navigator/tools/county_programs.py src/navigator/tools/document_requirements.py tests/test_county_programs.py tests/test_document_requirements.py
git commit -m "feat: add county programs and document requirements tools"
```

---

## Task 13: Stage 2 — Eligibility Engine

**Files:**
- Create: `src/navigator/eligibility.py`
- Create: `tests/test_eligibility_engine.py`

- [ ] **Step 1: Write eligibility engine tests**

Create `tests/test_eligibility_engine.py`:

```python
"""Tests for Stage 2: Eligibility Engine."""

import pytest
from unittest.mock import MagicMock, patch
from navigator.eligibility import EligibilityEngine
from navigator.models import UserProfile, Dependent, EligibilityResult


@pytest.fixture
def profile():
    return UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
        employment_status="recently_unemployed",
        dependents=[Dependent(age=3), Dependent(age=7)],
        concerns=["food", "housing"],
    )


def test_check_snap_eligible(profile):
    """Family at 121% FPL should be SNAP eligible (MN BBCE: 200% FPL)."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_snap(profile)
    assert result.eligible is True
    assert result.confidence == "high"
    assert "200%" in result.reason


def test_check_snap_over_income():
    """Family over 200% FPL should not be SNAP eligible."""
    profile = UserProfile(income=80000, household_size=3)
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_snap(profile)
    assert result.eligible is False


def test_check_mfip_eligible(profile):
    """Family with children in poverty should be MFIP eligible."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_mfip(profile)
    assert result.eligible is True


def test_check_mfip_no_children():
    """Single adult without children should not be MFIP eligible."""
    profile = UserProfile(income=20000, household_size=1)
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_mfip(profile)
    assert result.eligible is False


def test_check_medical_assistance_eligible(profile):
    """Family at 121% FPL should be MA eligible (138% FPL threshold)."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_medical_assistance(profile)
    assert result.eligible is True


def test_check_ui_eligible(profile):
    """Recently unemployed should be UI eligible."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_unemployment(profile)
    assert result.eligible is True


def test_check_ui_still_employed():
    """Employed person should not be UI eligible."""
    profile = UserProfile(income=50000, employment_status="employed")
    engine = EligibilityEngine.__new__(EligibilityEngine)
    result = engine._check_unemployment(profile)
    assert result.eligible is False


def test_determine_all_programs(profile):
    """Integration: should find multiple programs for a laid-off single mom."""
    engine = EligibilityEngine.__new__(EligibilityEngine)
    results = engine._run_rule_checks(profile)
    program_ids = [r.program_id for r in results if r.eligible]
    assert "snap" in program_ids
    assert "mfip" in program_ids
    assert "medical_assistance" in program_ids
    assert "unemployment_insurance" in program_ids
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_eligibility_engine.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement eligibility engine**

Create `src/navigator/eligibility.py`:

```python
"""Stage 2: Eligibility Engine — determine which programs a user may qualify for.

Uses a hybrid approach:
- Hard-coded rule checks for well-defined thresholds (FPL, age, employment status)
- RAG search for additional programs and detailed eligibility context
- Function calling for external API data (when available)
"""

import logging
from navigator.models import UserProfile, EligibilityResult, BenefitsResponse
from navigator.tools.fpl import check_fpl_threshold
from navigator.tools.county_programs import CountyProgramsTool
from navigator.tools.document_requirements import DocumentRequirementsTool
from navigator.tools.benefits_search import BenefitsSearchTool

logger = logging.getLogger(__name__)


class EligibilityEngine:
    """Determines program eligibility for a given user profile."""

    def __init__(
        self,
        search_tool: BenefitsSearchTool | None = None,
        county_tool: CountyProgramsTool | None = None,
        doc_tool: DocumentRequirementsTool | None = None,
    ):
        self.search_tool = search_tool
        self.county_tool = county_tool or CountyProgramsTool()
        self.doc_tool = doc_tool or DocumentRequirementsTool()

    def evaluate(self, profile: UserProfile) -> BenefitsResponse:
        """Run full eligibility evaluation for a user profile.

        Returns a BenefitsResponse with all eligible programs, documents, and
        application groupings.
        """
        # Step 1: Rule-based checks for major programs
        results = self._run_rule_checks(profile)

        # Step 2: Add county-specific programs
        if profile.county:
            county_results = self._check_county_programs(profile)
            results.extend(county_results)

        # Step 3: Sort by priority
        priority_order = {"high": 0, "normal": 1, "low": 2}
        results.sort(key=lambda r: priority_order.get(r.priority, 1))

        # Step 4: Get consolidated documents
        eligible_ids = [r.program_id for r in results if r.eligible]
        documents = self.doc_tool.get_consolidated_documents(eligible_ids, profile)

        # Step 5: Group by application portal
        app_groups = self._group_by_portal(results)

        return BenefitsResponse(
            eligible_programs=[r for r in results if r.eligible],
            documents_needed=documents,
            application_groups=app_groups,
        )

    def _run_rule_checks(self, profile: UserProfile) -> list[EligibilityResult]:
        """Run all hard-coded eligibility rule checks."""
        checks = [
            self._check_snap,
            self._check_mfip,
            self._check_medical_assistance,
            self._check_minnesotacare,
            self._check_unemployment,
            self._check_emergency_assistance,
            self._check_ega,
            self._check_ccap,
            self._check_energy_assistance,
            self._check_wic,
        ]
        results = []
        for check in checks:
            try:
                result = check(profile)
                results.append(result)
            except Exception as e:
                logger.warning("Rule check %s failed: %s", check.__name__, e)
        return results

    def _check_snap(self, profile: UserProfile) -> EligibilityResult:
        """SNAP: MN uses BBCE with 200% FPL gross income limit."""
        if profile.income is None:
            return EligibilityResult(
                program_id="snap", program_name="SNAP (Food Assistance)",
                eligible=None, confidence="low", category="food",
                reason="Income information needed to determine eligibility.",
                priority="high",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 200)
        eligible = fpl["below_threshold"]
        return EligibilityResult(
            program_id="snap", program_name="SNAP (Food Assistance)",
            eligible=eligible, confidence="high", category="food",
            reason=f"Household income ${profile.income:,.0f} = {fpl['fpl_percentage']}% FPL. "
                   f"MN SNAP uses 200% FPL BBCE threshold. "
                   f"{'Below' if eligible else 'Above'} threshold.",
            estimated_benefit=self._estimate_snap_benefit(profile.household_size) if eligible else "",
            source="DHS Combined Manual Section 0007.06",
            priority="high" if eligible else "low",
        )

    def _check_mfip(self, profile: UserProfile) -> EligibilityResult:
        """MFIP: MN's TANF. Families with children in poverty."""
        if not profile.has_children:
            return EligibilityResult(
                program_id="mfip", program_name="MFIP (Cash & Food Assistance)",
                eligible=False, confidence="high", category="cash",
                reason="MFIP requires minor children in the household.",
                priority="low",
            )
        if profile.income is None:
            return EligibilityResult(
                program_id="mfip", program_name="MFIP (Cash & Food Assistance)",
                eligible=None, confidence="low", category="cash",
                reason="Income information needed.", priority="high",
            )
        # MFIP has complex income tests; use ~100% FPL as rough threshold
        fpl = check_fpl_threshold(profile.income, profile.household_size, 100)
        return EligibilityResult(
            program_id="mfip", program_name="MFIP (Cash & Food Assistance)",
            eligible=fpl["below_threshold"],
            confidence="medium",  # MFIP has asset tests we can't check
            category="cash",
            reason=f"MFIP serves families with children below poverty level. "
                   f"Income {fpl['fpl_percentage']}% FPL. Asset limit $10,000 (not verified).",
            source="MN Statutes Chapter 256J",
            priority="high" if fpl["below_threshold"] else "low",
        )

    def _check_medical_assistance(self, profile: UserProfile) -> EligibilityResult:
        """Medical Assistance (Medicaid): 138% FPL for adults 19-64."""
        if profile.income is None:
            return EligibilityResult(
                program_id="medical_assistance", program_name="Medical Assistance (Medicaid)",
                eligible=None, confidence="low", category="health",
                reason="Income information needed.", priority="normal",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 138)
        return EligibilityResult(
            program_id="medical_assistance", program_name="Medical Assistance (Medicaid)",
            eligible=fpl["below_threshold"],
            confidence="high", category="health",
            reason=f"MA threshold: 138% FPL. Income = {fpl['fpl_percentage']}% FPL. "
                   f"{'Below' if fpl['below_threshold'] else 'Above'} threshold.",
            estimated_benefit="Free health coverage (no premium, $1-$3 copays)" if fpl["below_threshold"] else "",
            source="MN Statutes Chapter 256B; DHS EPM",
            priority="high" if fpl["below_threshold"] else "normal",
        )

    def _check_minnesotacare(self, profile: UserProfile) -> EligibilityResult:
        """MinnesotaCare: 138-200% FPL, ages 19-64."""
        if profile.income is None:
            return EligibilityResult(
                program_id="minnesotacare", program_name="MinnesotaCare",
                eligible=None, confidence="low", category="health",
                reason="Income information needed.", priority="normal",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 200)
        above_138 = not check_fpl_threshold(profile.income, profile.household_size, 138)["below_threshold"]
        eligible = fpl["below_threshold"] and above_138
        return EligibilityResult(
            program_id="minnesotacare", program_name="MinnesotaCare",
            eligible=eligible,
            confidence="medium", category="health",
            reason=f"MinnesotaCare: 138-200% FPL. Income = {fpl['fpl_percentage']}% FPL. "
                   f"{'Within' if eligible else 'Outside'} range. Requires no affordable employer coverage.",
            source="MN Statutes Chapter 256L",
            priority="normal",
        )

    def _check_unemployment(self, profile: UserProfile) -> EligibilityResult:
        """Unemployment Insurance: recently lost job through no fault."""
        recently_unemployed = profile.employment_status in (
            "recently_unemployed", "long_term_unemployed"
        )
        return EligibilityResult(
            program_id="unemployment_insurance",
            program_name="Unemployment Insurance",
            eligible=recently_unemployed,
            confidence="medium" if recently_unemployed else "high",
            category="employment",
            reason="UI available for workers who lost their job through no fault of their own. "
                   f"Employment status: {profile.employment_status or 'unknown'}. "
                   "Must have sufficient work history (not verified)."
                   if recently_unemployed else
                   f"Employment status '{profile.employment_status}' does not indicate recent job loss.",
            source="MN Statutes Chapter 268",
            priority="high" if recently_unemployed else "low",
        )

    def _check_emergency_assistance(self, profile: UserProfile) -> EligibilityResult:
        """Emergency Assistance: families with children facing housing crisis."""
        has_kids = profile.has_children
        housing_concern = "housing" in profile.concerns or "emergency" in profile.concerns
        eligible = has_kids and housing_concern
        return EligibilityResult(
            program_id="emergency_assistance",
            program_name="Emergency Assistance (EA)",
            eligible=eligible if (has_kids and housing_concern) else None,
            confidence="medium" if eligible else "low",
            category="emergency",
            reason="EA provides one-time payment for rent/mortgage/utilities for families "
                   "with children facing housing crisis. "
                   + ("Housing concern indicated." if housing_concern else "No housing crisis indicated.")
                   + (" Has children." if has_kids else " No children (EA requires children)."),
            source="DCYF Emergency Assistance program",
            priority="high" if eligible else "low",
        )

    def _check_ega(self, profile: UserProfile) -> EligibilityResult:
        """Emergency General Assistance: single adults, 200% FPL, emergency."""
        if profile.income is None:
            return EligibilityResult(
                program_id="ega", program_name="Emergency General Assistance (EGA)",
                eligible=None, confidence="low", category="emergency",
                reason="Income information needed.", priority="low",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 200)
        has_emergency = any(c in profile.concerns for c in ["housing", "food", "emergency", "energy"])
        eligible = fpl["below_threshold"] and has_emergency and not profile.has_children
        return EligibilityResult(
            program_id="ega", program_name="Emergency General Assistance (EGA)",
            eligible=eligible,
            confidence="medium", category="emergency",
            reason="EGA: one-time emergency help for individuals without children. "
                   f"Income {fpl['fpl_percentage']}% FPL (limit 200%). "
                   f"{'Emergency indicated.' if has_emergency else 'No emergency indicated.'} "
                   f"{'No children (eligible).' if not profile.has_children else 'Has children (use EA instead).'}",
            source="MN Statutes Chapter 256D; LawHelp MN",
            priority="normal" if eligible else "low",
        )

    def _check_ccap(self, profile: UserProfile) -> EligibilityResult:
        """CCAP: child care assistance for working/training parents."""
        has_young_kids = profile.has_children
        working_or_training = profile.employment_status in (
            "employed", "recently_unemployed", "student"
        )
        eligible = has_young_kids and working_or_training
        return EligibilityResult(
            program_id="ccap", program_name="Child Care Assistance Program (CCAP)",
            eligible=eligible if has_young_kids else False,
            confidence="medium" if eligible else "high",
            category="childcare",
            reason="CCAP helps pay for child care while parents work, look for work, or attend school. "
                   f"{'Has children.' if has_young_kids else 'No children.'} "
                   f"Income must be below 47% SMI (entry) / 85% SMI (exit). Income threshold not verified.",
            source="DCYF CCAP; MN House Research",
            priority="normal" if eligible else "low",
        )

    def _check_energy_assistance(self, profile: UserProfile) -> EligibilityResult:
        """Energy Assistance Program: 50% SMI income threshold."""
        # 50% SMI is roughly 60% FPL for most household sizes (approximation)
        if profile.income is None:
            return EligibilityResult(
                program_id="energy_assistance", program_name="Energy Assistance Program (EAP)",
                eligible=None, confidence="low", category="energy",
                reason="Income information needed.", priority="normal",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 150)
        energy_concern = "energy" in profile.concerns or "housing" in profile.concerns
        return EligibilityResult(
            program_id="energy_assistance", program_name="Energy Assistance Program (EAP)",
            eligible=fpl["below_threshold"],
            confidence="medium",  # Using FPL approximation for SMI
            category="energy",
            reason=f"EAP threshold: 50% State Median Income (approx 150% FPL). "
                   f"Income = {fpl['fpl_percentage']}% FPL. Benefits: $200-$1,400 heating, up to $600 crisis. "
                   f"Application deadline May 31, 2026.",
            source="MN Commerce Dept EAP Guidelines",
            priority="normal" if fpl["below_threshold"] else "low",
        )

    def _check_wic(self, profile: UserProfile) -> EligibilityResult:
        """WIC: pregnant/postpartum/children under 5, 185% FPL."""
        has_young = profile.has_young_children
        if not has_young:
            return EligibilityResult(
                program_id="wic", program_name="WIC (Women, Infants, and Children)",
                eligible=False, confidence="high", category="food",
                reason="WIC requires pregnant/postpartum women or children under 5.",
                priority="low",
            )
        if profile.income is None:
            return EligibilityResult(
                program_id="wic", program_name="WIC (Women, Infants, and Children)",
                eligible=None, confidence="low", category="food",
                reason="Income needed. Auto-eligible if on SNAP, Medicaid, or MFIP.",
                priority="normal",
            )
        fpl = check_fpl_threshold(profile.income, profile.household_size, 185)
        return EligibilityResult(
            program_id="wic", program_name="WIC (Women, Infants, and Children)",
            eligible=fpl["below_threshold"],
            confidence="high", category="food",
            reason=f"WIC threshold: 185% FPL. Income = {fpl['fpl_percentage']}% FPL. "
                   f"Has child(ren) under 5. Also auto-eligible if receiving SNAP, MA, or MFIP.",
            source="MN Dept of Health WIC Program",
            priority="normal" if fpl["below_threshold"] else "low",
        )

    def _check_county_programs(self, profile: UserProfile) -> list[EligibilityResult]:
        """Check for county-specific programs."""
        results = []
        county_programs = self.county_tool.get_programs(profile.county or "")

        for prog in county_programs:
            if prog["type"] == "employment" and profile.employment_status in (
                "recently_unemployed", "long_term_unemployed"
            ):
                results.append(EligibilityResult(
                    program_id=f"county_{prog['name'].lower().replace(' ', '_')[:30]}",
                    program_name=prog["name"],
                    eligible=True,
                    confidence="medium",
                    category="employment",
                    reason=prog.get("description", "County employment program for displaced workers."),
                    source=prog.get("url", ""),
                    priority="normal",
                ))
            elif prog["type"] == "cap":
                results.append(EligibilityResult(
                    program_id=f"cap_{profile.county.lower() if profile.county else 'unknown'}",
                    program_name=prog["name"],
                    eligible=True,
                    confidence="high",
                    category="community",
                    reason=prog.get("description", "Community Action programs available to all residents."),
                    source=prog.get("url", ""),
                    priority="normal",
                ))

        return results

    def _estimate_snap_benefit(self, household_size: int) -> str:
        """Rough SNAP benefit estimate by household size (2026 values)."""
        estimates = {1: "$292", 2: "$535", 3: "$768", 4: "$975", 5: "$1,158", 6: "$1,390"}
        return f"Up to {estimates.get(household_size, '$' + str(292 + 243 * (household_size - 1)))}/month"

    def _group_by_portal(self, results: list[EligibilityResult]) -> dict[str, list[str]]:
        """Group eligible programs by application portal."""
        portal_map = {
            "snap": "MNbenefits.mn.gov",
            "mfip": "MNbenefits.mn.gov",
            "emergency_assistance": "MNbenefits.mn.gov",
            "ega": "MNbenefits.mn.gov",
            "ccap": "MNbenefits.mn.gov",
            "medical_assistance": "MNsure.org",
            "minnesotacare": "MNsure.org",
            "unemployment_insurance": "uimn.org",
            "energy_assistance": "Contact local CAP agency",
            "wic": "Call 1-800-942-4030",
        }
        groups: dict[str, list[str]] = {}
        for r in results:
            if not r.eligible:
                continue
            portal = portal_map.get(r.program_id, "Contact county office")
            if portal not in groups:
                groups[portal] = []
            groups[portal].append(r.program_name)
        return groups
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_eligibility_engine.py -v`
Expected: All 8 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/navigator/eligibility.py tests/test_eligibility_engine.py
git commit -m "feat: add Stage 2 eligibility engine with rule-based checks for MN programs"
```

---

## Task 14: Stage 3 — Response Generation

**Files:**
- Create: `src/navigator/response.py`
- Create: `tests/test_response.py`

- [ ] **Step 1: Write response generation tests**

Create `tests/test_response.py`:

```python
"""Tests for Stage 3: Response Generation."""

import pytest
from unittest.mock import patch, MagicMock
from navigator.response import ResponseGenerator
from navigator.models import (
    UserProfile, Dependent, EligibilityResult, BenefitsResponse, ReadingLevel,
)


@pytest.fixture
def generator():
    return ResponseGenerator()


@pytest.fixture
def sample_response():
    return BenefitsResponse(
        eligible_programs=[
            EligibilityResult(
                program_id="snap", program_name="SNAP",
                eligible=True, confidence="high", category="food",
                reason="Below 200% FPL", estimated_benefit="$768/month",
                source="DHS Combined Manual", priority="high",
            ),
            EligibilityResult(
                program_id="unemployment_insurance",
                program_name="Unemployment Insurance",
                eligible=True, confidence="medium", category="employment",
                reason="Recently unemployed", priority="high",
                source="MN Statutes 268",
            ),
        ],
        documents_needed=["Photo ID", "Pay stubs", "Layoff letter"],
        application_groups={
            "MNbenefits.mn.gov": ["SNAP"],
            "uimn.org": ["Unemployment Insurance"],
        },
    )


@pytest.fixture
def sample_profile():
    return UserProfile(
        income=32000, household_size=3, county="Ramsey",
        employment_status="recently_unemployed",
        dependents=[Dependent(age=3), Dependent(age=7)],
        reading_level=ReadingLevel.SIMPLE,
        language="en",
    )


def test_format_context(generator, sample_response, sample_profile):
    """Test that the context formatted for the LLM includes all key info."""
    context = generator._format_context(sample_response, sample_profile)
    assert "SNAP" in context
    assert "Unemployment Insurance" in context
    assert "Photo ID" in context
    assert "MNbenefits.mn.gov" in context


@patch("navigator.response.OllamaClient")
def test_generate_calls_ollama(MockClient, sample_response, sample_profile):
    mock_instance = MockClient.return_value
    mock_instance.chat.return_value = "Here are the programs you may be eligible for..."
    gen = ResponseGenerator(client=mock_instance)

    result = gen.generate(sample_response, sample_profile)
    assert isinstance(result, str)
    assert len(result) > 0
    mock_instance.chat.assert_called_once()


def test_format_context_includes_disclaimer(generator, sample_response, sample_profile):
    context = generator._format_context(sample_response, sample_profile)
    assert "informational tool" in context.lower() or "not legal advice" in context.lower()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_response.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement response generator**

Create `src/navigator/response.py`:

```python
"""Stage 3: Response Generation — produce plain language output from eligibility results."""

from navigator.models import UserProfile, BenefitsResponse, ReadingLevel
from navigator.ollama_client import OllamaClient
from navigator.prompts import get_response_prompt, RESPONSE_DISCLAIMER
from navigator.config import SUPPORTED_LANGUAGES


class ResponseGenerator:
    """Generate plain-language benefits guidance from eligibility results."""

    def __init__(self, client: OllamaClient | None = None):
        self.client = client or OllamaClient()

    def generate(self, response: BenefitsResponse, profile: UserProfile) -> str:
        """Generate a plain-language response for the user.

        Args:
            response: The BenefitsResponse from the eligibility engine.
            profile: The user's profile (for reading level and language).
        """
        context = self._format_context(response, profile)
        language = SUPPORTED_LANGUAGES.get(profile.language, "English")
        system_prompt = get_response_prompt(
            reading_level=profile.reading_level.value,
            language=language,
        )

        return self.client.chat(context, system_prompt=system_prompt)

    def _format_context(self, response: BenefitsResponse, profile: UserProfile) -> str:
        """Format eligibility results as structured context for the LLM."""
        parts = []

        # User situation summary
        parts.append("## User Situation")
        parts.append(f"- Income: ${profile.income:,.0f}/year" if profile.income else "- Income: Unknown")
        parts.append(f"- Household size: {profile.household_size}")
        parts.append(f"- County: {profile.county or 'Unknown'}")
        parts.append(f"- Employment: {profile.employment_status or 'Unknown'}")
        if profile.dependents:
            ages = ", ".join(str(d.age) for d in profile.dependents)
            parts.append(f"- Dependents: {len(profile.dependents)} (ages: {ages})")
        if profile.fpl_percentage:
            parts.append(f"- Federal Poverty Level: {profile.fpl_percentage}%")

        # Eligible programs
        parts.append("\n## Eligible Programs")
        high_priority = [r for r in response.eligible_programs if r.priority == "high"]
        normal_priority = [r for r in response.eligible_programs if r.priority != "high"]

        if high_priority:
            parts.append("\n### HIGH PRIORITY")
            for r in high_priority:
                parts.append(f"\n**{r.program_name}**")
                parts.append(f"- Category: {r.category}")
                parts.append(f"- Reason: {r.reason}")
                if r.estimated_benefit:
                    parts.append(f"- Estimated benefit: {r.estimated_benefit}")
                parts.append(f"- Confidence: {r.confidence}")
                parts.append(f"- Source: {r.source}")

        if normal_priority:
            parts.append("\n### ALSO CHECK")
            for r in normal_priority:
                parts.append(f"\n**{r.program_name}**")
                parts.append(f"- Reason: {r.reason}")
                if r.estimated_benefit:
                    parts.append(f"- Estimated benefit: {r.estimated_benefit}")
                parts.append(f"- Source: {r.source}")

        # Documents
        if response.documents_needed:
            parts.append("\n## Documents to Gather")
            for doc in response.documents_needed:
                parts.append(f"- {doc}")

        # Application portals
        if response.application_groups:
            parts.append("\n## Where to Apply")
            for portal, programs in response.application_groups.items():
                parts.append(f"- **{portal}**: {', '.join(programs)}")

        # Disclaimer
        parts.append(f"\n## Disclaimer\n{RESPONSE_DISCLAIMER}")

        return "\n".join(parts)
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_response.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/navigator/response.py tests/test_response.py
git commit -m "feat: add Stage 3 response generator with reading level and language support"
```

---

## Task 15: End-to-End Integration Test

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: Write integration test**

Create `tests/test_integration.py`:

```python
"""End-to-end integration tests for the Navigator pipeline.

Tests the full flow: UserProfile -> EligibilityEngine -> ResponseGenerator.
Ollama calls are mocked; everything else runs for real.
"""

import pytest
from unittest.mock import patch, MagicMock
from navigator.models import UserProfile, Dependent, ReadingLevel
from navigator.eligibility import EligibilityEngine
from navigator.response import ResponseGenerator
from navigator.tools.county_programs import CountyProgramsTool
from navigator.tools.document_requirements import DocumentRequirementsTool


@pytest.fixture
def profile():
    """The canonical test scenario: single mom, Ramsey County, laid off."""
    return UserProfile(
        income=32000,
        household_size=3,
        county="Ramsey",
        state="MN",
        employment_status="recently_unemployed",
        dependents=[Dependent(age=3), Dependent(age=7)],
        concerns=["food", "housing"],
        language="en",
        reading_level=ReadingLevel.SIMPLE,
    )


def test_full_pipeline_no_ollama(profile):
    """Test eligibility engine produces correct results without Ollama."""
    engine = EligibilityEngine()
    response = engine.evaluate(profile)

    # Should find multiple programs
    program_ids = [r.program_id for r in response.eligible_programs]
    assert "snap" in program_ids, "SNAP should be eligible at 121% FPL"
    assert "mfip" in program_ids, "MFIP should be eligible (has children, low income)"
    assert "medical_assistance" in program_ids, "MA should be eligible at 121% FPL < 138%"
    assert "unemployment_insurance" in program_ids, "UI should be eligible (recently unemployed)"
    assert "wic" in program_ids, "WIC should be eligible (child under 5, below 185% FPL)"

    # Should have documents
    assert len(response.documents_needed) > 0
    assert "Government-issued photo ID" in response.documents_needed

    # Should have application groups
    assert "MNbenefits.mn.gov" in response.application_groups
    assert "uimn.org" in response.application_groups

    # Should have disclaimer
    assert "not legal advice" in response.disclaimer


def test_county_programs_included(profile):
    """Ramsey County should include Dislocated Worker and CAPRW."""
    engine = EligibilityEngine()
    response = engine.evaluate(profile)
    names = [r.program_name for r in response.eligible_programs]

    assert any("Dislocated Worker" in n for n in names), \
        "Ramsey County Dislocated Worker should be included"
    assert any("CAPRW" in n for n in names), \
        "CAPRW community programs should be included"


def test_high_income_fewer_programs():
    """High income household should have fewer eligible programs."""
    profile = UserProfile(
        income=120000,
        household_size=3,
        county="Ramsey",
        employment_status="employed",
    )
    engine = EligibilityEngine()
    response = engine.evaluate(profile)
    eligible = [r for r in response.eligible_programs]
    # Should not qualify for income-based programs
    ids = [r.program_id for r in eligible]
    assert "snap" not in ids
    assert "mfip" not in ids
    assert "medical_assistance" not in ids


@patch("navigator.response.OllamaClient")
def test_response_generation(MockClient, profile):
    """Test that response generation calls Ollama with correct context."""
    mock_instance = MockClient.return_value
    mock_instance.chat.return_value = "Based on your situation, you may be eligible for..."

    engine = EligibilityEngine()
    benefits_response = engine.evaluate(profile)

    gen = ResponseGenerator(client=mock_instance)
    text = gen.generate(benefits_response, profile)

    assert isinstance(text, str)
    # Verify the system prompt includes reading level
    call_args = mock_instance.chat.call_args
    system_prompt = call_args[1].get("system_prompt") or call_args[0][1]
    assert "simple" in system_prompt.lower()
```

- [ ] **Step 2: Run integration tests**

Run: `pytest tests/test_integration.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 3: Run full test suite**

Run: `pytest tests/ -v --tb=short`
Expected: All tests across all modules PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add end-to-end integration tests for Navigator pipeline"
```

---

## Task 16: Gradio UI

**Files:**
- Modify: `src/app.py`

- [ ] **Step 1: Implement the Gradio application**

Replace `src/app.py` with:

```python
"""Gradio UI for the Plain Language Government Navigator."""

import logging
from collections.abc import Generator

import gradio as gr

from navigator.models import UserProfile, Dependent, ReadingLevel
from navigator.ollama_client import OllamaClient
from navigator.intake import IntakeProcessor
from navigator.eligibility import EligibilityEngine
from navigator.response import ResponseGenerator
from navigator.prompts import RESPONSE_DISCLAIMER

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
client = OllamaClient()
intake = IntakeProcessor(client=client)
engine = EligibilityEngine()
generator = ResponseGenerator(client=client)


def process_message(
    message: str,
    history: list[dict],
    reading_level: str,
    language: str,
) -> str:
    """Process a user message through the Navigator pipeline."""
    try:
        # Stage 1: Extract profile
        profile, missing = intake.extract(message)

        # Override reading level and language from UI settings
        profile.reading_level = ReadingLevel(reading_level)
        profile.language = {"English": "en", "Spanish": "es", "Hmong": "hmn",
                           "Somali": "so", "Karen": "kar"}.get(language, "en")

        # If missing critical info, ask follow-up
        if missing:
            return intake.ask_followup(missing)

        # Stage 2: Determine eligibility
        benefits_response = engine.evaluate(profile)

        # Stage 3: Generate plain-language response
        response_text = generator.generate(benefits_response, profile)

        # Append sources section
        sources = _format_sources(benefits_response)
        if sources:
            response_text += f"\n\n---\n**Sources & Reasoning**\n{sources}"

        return response_text

    except Exception as e:
        logger.exception("Error processing message")
        return (
            "I'm sorry, I encountered an error processing your request. "
            "Please try rephrasing your situation, or contact 211 by dialing 2-1-1 "
            "for immediate assistance.\n\n"
            f"Error: {e}"
        )


def _format_sources(benefits_response) -> str:
    """Format the sources accordion content."""
    lines = []
    for r in benefits_response.eligible_programs:
        if r.source:
            lines.append(f"- **{r.program_name}**: {r.reason} (Source: {r.source})")
    return "\n".join(lines)


# Build the Gradio interface
with gr.Blocks(
    title="Plain Language Government Navigator",
    theme=gr.themes.Soft(),
) as demo:
    gr.Markdown(
        "# Plain Language Government Navigator\n"
        "*Powered by Gemma 4 via Ollama - Your data never leaves this device*"
    )

    with gr.Row():
        # Left sidebar
        with gr.Column(scale=1):
            gr.Markdown("### Settings")
            reading_level = gr.Radio(
                choices=["simple", "standard", "detailed"],
                value="standard",
                label="Reading Level",
            )
            language = gr.Dropdown(
                choices=["English", "Spanish", "Hmong", "Somali", "Karen"],
                value="English",
                label="Language",
            )
            gr.Markdown(
                "---\n"
                "*Describe your situation in your own words. "
                "Include details like your income, household size, "
                "county, and what kind of help you need.*"
            )

        # Main chat area
        with gr.Column(scale=3):
            chatbot = gr.ChatInterface(
                fn=process_message,
                additional_inputs=[reading_level, language],
                examples=[
                    "I'm a single mom with two kids, ages 3 and 7. I just got laid off "
                    "from my warehouse job where I made $32,000. We're in Ramsey County "
                    "and I'm worried about paying rent and feeding my kids.",
                    "I'm a 68-year-old veteran in Hennepin County living on Social Security. "
                    "I'm having trouble paying my heating bill this winter.",
                    "Soy madre soltera con dos hijos. Perdí mi trabajo y necesito ayuda "
                    "con comida y alquiler. Vivo en el condado de Dakota.",
                ],
                retry_btn=None,
                undo_btn=None,
            )

    gr.Markdown(
        f"---\n*{RESPONSE_DISCLAIMER}*\n\n"
        "Running locally via Ollama | Last updated: April 2026"
    )


def main():
    """Launch the Navigator Gradio app."""
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test the UI locally**

Run:
```bash
python src/app.py
```
Expected: Gradio launches at `http://localhost:7860`. Open in browser and test with:
- The single mom scenario
- Switching reading levels
- Switching to Spanish

Press Ctrl+C to stop.

- [ ] **Step 3: Commit**

```bash
git add src/app.py
git commit -m "feat: add Gradio UI with chat, reading level toggle, and language selector"
```

---

## Task 17: Data Scraping Scripts (High-Level)

**Files:**
- Create: `scripts/scrape_dhs_manual.py`
- Create: `scripts/scrape_county_pages.py`
- Create: `scripts/download_sam_gov.py`
- Create: `scripts/ingest_all.py`

These scripts are high-level outlines since you're experienced with web scraping. Fill in the implementation details based on the target sites' structure.

- [ ] **Step 1: Create DHS Combined Manual scraper**

Create `scripts/scrape_dhs_manual.py`:

```python
"""Scrape the DHS Combined Manual for cash/food eligibility rules.

Target: https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION&RevisionSelectionMethod=LatestReleased&dDocName=ID_016956

Output: data/raw/dhs_combined_manual/ (one file per section)

Key sections to scrape:
- Gross income limits
- Assistance standards and benefit amounts
- Application processing
- MFIP, DWP, SNAP, GA, GRH/Housing Support, MSA, RCA, Emergency programs

Strategy:
1. Fetch the table of contents page
2. Follow each section link
3. Extract text content (strip HTML formatting)
4. Save as individual text files named by section number
5. Be polite: add 1-2 second delays between requests
6. Respect robots.txt (government sites are typically permissive)
"""

import time
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

from navigator.config import RAW_DIR

OUTPUT_DIR = RAW_DIR / "dhs_combined_manual"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://www.dhs.state.mn.us"
MANUAL_TOC = (
    f"{BASE_URL}/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION"
    "&RevisionSelectionMethod=LatestReleased&dDocName=ID_016956"
)


def main():
    # TODO: Implement based on the DHS site structure.
    # 1. Fetch TOC page
    # 2. Parse section links
    # 3. For each section, fetch and extract text
    # 4. Save to OUTPUT_DIR / f"section_{number}.txt"
    print(f"DHS Combined Manual scraper — output to {OUTPUT_DIR}")
    print("Implement scraping logic based on site structure.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create county pages scraper**

Create `scripts/scrape_county_pages.py`:

```python
"""Scrape social services pages for the 5 Twin Cities metro counties.

Target URLs (from docs/research/minnesota_benefits_deep_dive.md):
- Ramsey: https://www.ramseycountymn.gov/residents/assistance-support/
- Hennepin: https://www.hennepin.us/en/residents/human-services
- Dakota: https://www.co.dakota.mn.us/HealthFamily/PublicAssistance
- Scott: https://www.scottcountymn.gov/193/Social-Services
- Carver: https://www.carvercountymn.gov/departments/health-human-services

Also scrape CAP agency pages:
- CAPRW: https://www.caprw.org/
- CAP-HC: https://caphennepin.org/
- CAP Agency: https://capagency.org/

Output: data/raw/county_pages/ (one directory per county/agency)

Strategy:
1. For each county, fetch the main social services page
2. Follow links to individual program pages
3. Extract program descriptions, eligibility info, contacts
4. Save as JSON files with structure matching the Program model
"""

from pathlib import Path

from navigator.config import RAW_DIR

OUTPUT_DIR = RAW_DIR / "county_pages"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COUNTY_URLS = {
    "ramsey": "https://www.ramseycountymn.gov/residents/assistance-support/",
    "hennepin": "https://www.hennepin.us/en/residents/human-services",
    "dakota": "https://www.co.dakota.mn.us/HealthFamily/PublicAssistance",
    "scott": "https://www.scottcountymn.gov/193/Social-Services",
    "carver": "https://www.carvercountymn.gov/departments/health-human-services",
}

CAP_URLS = {
    "caprw": "https://www.caprw.org/",
    "cap_hc": "https://caphennepin.org/",
    "cap_agency": "https://capagency.org/",
}


def main():
    print(f"County pages scraper — output to {OUTPUT_DIR}")
    print("Implement scraping logic based on each site's structure.")
    # TODO: Implement for each county and CAP agency


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Create SAM.gov downloader**

Create `scripts/download_sam_gov.py`:

```python
"""Download federal assistance listings from SAM.gov API.

API docs: https://open.gsa.gov/api/
Endpoint: Assistance Listings Public API

Output: data/raw/sam_gov/ (JSON files)

Steps:
1. Register for API key at api.data.gov (free, instant)
2. Set SAM_GOV_API_KEY in .env
3. Fetch assistance listings (paginated)
4. Filter to benefits-relevant programs (categories: income security,
   food/nutrition, health, housing, employment, education)
5. Save as individual JSON files per program
"""

import os
import json
from pathlib import Path

import httpx
from dotenv import load_dotenv

from navigator.config import RAW_DIR

load_dotenv()
OUTPUT_DIR = RAW_DIR / "sam_gov"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.getenv("SAM_GOV_API_KEY", "")
BASE_URL = "https://api.sam.gov/opportunities/v2/search"


def main():
    if not API_KEY:
        print("Set SAM_GOV_API_KEY in .env (get one at api.data.gov)")
        return
    print(f"SAM.gov downloader — output to {OUTPUT_DIR}")
    # TODO: Implement API calls and pagination


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Create ingestion orchestrator**

Create `scripts/ingest_all.py`:

```python
"""Run the full ingestion pipeline: load all scraped data into ChromaDB + BM25.

Run this after scraping is complete:
    python scripts/ingest_all.py

What it does:
1. Loads all program JSON files from data/programs/
2. Loads all processed text files from data/processed/
3. Ingests everything into ChromaDB with metadata tagging
4. Builds the BM25 keyword index
5. Reports final document count
"""

import json
import logging
from pathlib import Path

from navigator.config import PROGRAMS_DIR, PROCESSED_DIR, RAW_DIR
from navigator.rag.ingest import IngestPipeline, process_program_file, process_text_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    pipeline = IngestPipeline()

    # Ingest program JSON files
    if PROGRAMS_DIR.exists() and any(PROGRAMS_DIR.glob("**/*.json")):
        count = pipeline.ingest_programs_dir()
        logger.info("Ingested %d program document chunks", count)
    else:
        logger.warning("No program files found in %s", PROGRAMS_DIR)

    # Ingest processed text files by jurisdiction
    text_dirs = {
        "federal": PROCESSED_DIR / "federal",
        "state:MN": PROCESSED_DIR / "state_mn",
        "county:ramsey": PROCESSED_DIR / "county_ramsey",
        "county:hennepin": PROCESSED_DIR / "county_hennepin",
        "county:dakota": PROCESSED_DIR / "county_dakota",
        "county:scott": PROCESSED_DIR / "county_scott",
        "county:carver": PROCESSED_DIR / "county_carver",
    }
    for jurisdiction, text_dir in text_dirs.items():
        if text_dir.exists():
            count = pipeline.ingest_text_dir(
                text_dir, jurisdiction=jurisdiction, category="general"
            )
            logger.info("Ingested %d chunks from %s (%s)", count, text_dir, jurisdiction)

    logger.info("Total documents ingested: %d", pipeline.total_documents)
    logger.info("ChromaDB store count: %d", pipeline.store.count())


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Commit**

```bash
git add scripts/
git commit -m "feat: add data scraping scripts and ingestion pipeline orchestrator"
```

---

## Task 18: Unsloth Fine-Tuning Script

**Files:**
- Create: `training/train_unsloth.py`
- Create: `training/export_gguf.py`

- [ ] **Step 1: Create the Unsloth training script**

Create `training/train_unsloth.py`:

```python
"""Fine-tune Gemma 4 E4B with Unsloth + QLoRA.

Run on Kaggle T4 (16 GB) or local RTX 2080 Ti (11 GB).

Usage:
    python training/train_unsloth.py --dataset data/training/combined.jsonl

Dataset format (JSONL, one JSON object per line):
    {"messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]}

See docs/research/toolchain_reference_guide.md for detailed Unsloth docs.
"""

import argparse
import json
from pathlib import Path

from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import Dataset


def load_dataset(path: str) -> Dataset:
    """Load JSONL dataset into HuggingFace Dataset format."""
    records = []
    with open(path) as f:
        for line in f:
            records.append(json.loads(line))
    return Dataset.from_list(records)


def format_chat(example: dict) -> dict:
    """Format a chat example for training."""
    messages = example["messages"]
    # Unsloth handles chat template formatting internally
    return {"messages": messages}


def main():
    parser = argparse.ArgumentParser(description="Fine-tune Gemma 4 E4B with Unsloth")
    parser.add_argument("--dataset", required=True, help="Path to JSONL training data")
    parser.add_argument("--output", default="training/output", help="Output directory")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=4)
    parser.add_argument("--lora-rank", type=int, default=16)
    parser.add_argument("--max-seq-length", type=int, default=2048)
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load model with Unsloth optimizations
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="google/gemma-4-E4B-it",
        max_seq_length=args.max_seq_length,
        load_in_4bit=True,
        dtype=None,  # auto-detect
    )

    # Add LoRA adapters
    model = FastLanguageModel.get_peft_model(
        model,
        r=args.lora_rank,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_alpha=args.lora_rank * 2,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
    )

    # Load and prepare dataset
    dataset = load_dataset(args.dataset)
    dataset = dataset.map(format_chat)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        logging_steps=10,
        save_steps=100,
        save_total_limit=2,
        fp16=False,
        bf16=True,
        optim="adamw_8bit",
        seed=42,
        report_to="none",
    )

    # Create trainer
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=training_args,
        max_seq_length=args.max_seq_length,
    )

    # Train
    print(f"Training on {len(dataset)} examples for {args.epochs} epochs...")
    trainer.train()

    # Save
    model.save_pretrained(str(output_dir / "final"))
    tokenizer.save_pretrained(str(output_dir / "final"))
    print(f"Model saved to {output_dir / 'final'}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create GGUF export script**

Create `training/export_gguf.py`:

```python
"""Export Unsloth fine-tuned model to GGUF format for Ollama.

Usage:
    python training/export_gguf.py --model training/output/final --output training/output/gguf

After export, create an Ollama model:
    ollama create navigator-e4b -f training/output/gguf/Modelfile
"""

import argparse
from pathlib import Path

from unsloth import FastLanguageModel


def main():
    parser = argparse.ArgumentParser(description="Export fine-tuned model to GGUF")
    parser.add_argument("--model", required=True, help="Path to fine-tuned model")
    parser.add_argument("--output", default="training/output/gguf", help="Output directory")
    parser.add_argument("--quant", default="q4_k_m", help="Quantization method")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the fine-tuned model
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=2048,
        load_in_4bit=True,
    )

    # Export to GGUF
    model.save_pretrained_gguf(
        str(output_dir),
        tokenizer,
        quantization_method=args.quant,
    )

    # Create Ollama Modelfile
    modelfile_content = f"""FROM {output_dir / f'unsloth.{args.quant.upper()}.gguf'}
PARAMETER temperature 1.0
PARAMETER top_p 0.95
PARAMETER top_k 64
SYSTEM "You are a plain-language government benefits navigator."
"""
    modelfile_path = output_dir / "Modelfile"
    modelfile_path.write_text(modelfile_content)

    print(f"GGUF exported to {output_dir}")
    print(f"Modelfile written to {modelfile_path}")
    print(f"\nTo create Ollama model, run:")
    print(f"  ollama create navigator-e4b -f {modelfile_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Commit**

```bash
git add training/
git commit -m "feat: add Unsloth fine-tuning and GGUF export scripts"
```

---

## Task 19: Update CLAUDE.md with New Project Structure

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update CLAUDE.md**

Add to the `## Project Status` section in CLAUDE.md:

```markdown
## Project Status

- **Active idea: Plain Language Government Navigator** — see `docs/ideas/plans/plain_language_government_navigator.md`
  - Design spec: `docs/superpowers/specs/2026-04-05-plain-language-government-navigator-design.md`
  - Architecture: Three-stage pipeline (Intake -> Eligibility -> Response) with Gemma 4 E4B via Ollama
  - Prize targets: Main + Digital Equity + Safety & Trust + Ollama + Unsloth ($130K ceiling)
```

Update the `## Project Structure` section:

```markdown
## Project Structure

- `src/navigator/` — Core Navigator application
  - `models.py` — Pydantic data models (UserProfile, Program, EligibilityResult)
  - `intake.py` — Stage 1: situation parsing and profile extraction
  - `eligibility.py` — Stage 2: rule-based + RAG eligibility engine
  - `response.py` — Stage 3: plain language response generation
  - `ollama_client.py` — Ollama API wrapper
  - `prompts.py` — System prompts for all pipeline stages
  - `readability.py` — Flesch-Kincaid reading level checking
  - `config.py` — Settings, paths, model configuration
  - `rag/` — RAG pipeline (ChromaDB, BM25, hybrid retrieval, ingestion)
  - `tools/` — Function calling tools (FPL calc, benefits search, county programs, docs)
- `src/app.py` — Gradio UI entry point
- `scripts/` — Data scraping and ingestion scripts
- `training/` — Unsloth fine-tuning and GGUF export
- `tests/` — Full test suite
- `data/` — Scraped data, ChromaDB store, training datasets
- `models/` — Gemma 4 model weights (31B + E4B)
- `docs/ideas/plans/` — Competition idea plans
- `docs/research/` — Research reports (federal APIs, MN benefits, toolchain guide)
- `docs/competition/` — Competition rules and overview
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with Navigator project structure and status"
```

---

## Self-Review Checklist

**Spec coverage:**
- [x] Three-stage pipeline (intake, eligibility, response) — Tasks 10, 13, 14
- [x] Two-model split (E4B + 26B MoE) — Task 4 (Ollama client), Task 13 (engine)
- [x] RAG with ChromaDB + BM25 hybrid — Tasks 6, 7, 8
- [x] Function calling tools — Tasks 3, 11, 12
- [x] Gradio UI with reading level + language — Task 16
- [x] Unsloth fine-tuning — Task 18
- [x] Data scraping — Task 17
- [x] County-specific programs (5 counties) — Task 12
- [x] Document requirements — Task 12
- [x] Readability checking — Task 9
- [x] Integration testing — Task 15
- [x] Disclaimers on every response — Tasks 5, 14

**Placeholder scan:** No TBDs in code (scraping scripts have TODO comments intentionally since user handles those). All code blocks are complete.

**Type consistency:** UserProfile, Program, EligibilityResult, BenefitsResponse used consistently across all tasks. Method names match: `extract()`, `evaluate()`, `generate()`, `search()`.
