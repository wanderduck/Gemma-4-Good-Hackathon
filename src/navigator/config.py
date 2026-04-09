"""Configuration for the Navigator application."""

import os
from pathlib import Path

# Paths — override with NAVIGATOR_DATA_DIR env var for container deployments
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = Path(os.environ["NAVIGATOR_DATA_DIR"]) if "NAVIGATOR_DATA_DIR" in os.environ else PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CHROMA_DIR = DATA_DIR / "chroma_db"
FPL_DIR = DATA_DIR / "fpl_tables"
PROGRAMS_DIR = DATA_DIR / "programs"
TRAINING_DIR = DATA_DIR / "training"

# Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "navigator"

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
