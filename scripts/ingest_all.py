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
