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

    # Ingest DHS Combined Manual sections (raw scraped text)
    dhs_dir = RAW_DIR / "dhs_combined_manual"
    if dhs_dir.exists():
        count = pipeline.ingest_text_dir(
            dhs_dir, jurisdiction="state:MN", category="eligibility",
            program="dhs_combined_manual",
        )
        logger.info("Ingested %d DHS manual chunks from %s", count, dhs_dir)

    # Ingest county program JSON files
    county_dir = RAW_DIR / "county_pages"
    if county_dir.exists():
        for county_path in sorted(county_dir.iterdir()):
            programs_file = county_path / "programs.json"
            if not programs_file.exists():
                continue
            county_name = county_path.name
            programs = json.loads(programs_file.read_text())
            count = 0
            for prog in programs:
                text_parts = []
                if prog.get("name"):
                    text_parts.append(prog["name"])
                if prog.get("description"):
                    text_parts.append(prog["description"])
                if prog.get("eligibility"):
                    text_parts.append(f"Eligibility: {prog['eligibility']}")
                if prog.get("contact"):
                    text_parts.append(f"Contact: {prog['contact']}")
                if prog.get("url"):
                    text_parts.append(f"More info: {prog['url']}")
                full_text = "\n\n".join(text_parts)
                from navigator.rag.ingest import chunk_text, _make_id
                chunks = chunk_text(full_text)
                docs = []
                for i, chunk in enumerate(chunks):
                    doc_id = _make_id(chunk, prefix=f"{county_name}_{prog.get('name', 'unknown')}")
                    docs.append({
                        "id": doc_id,
                        "text": chunk,
                        "metadata": {
                            "jurisdiction": f"county:{county_name}",
                            "category": prog.get("type", "general"),
                            "program": prog.get("name", ""),
                            "source": prog.get("url", county_name),
                            "chunk_index": i,
                        },
                    })
                pipeline._add_docs(docs)
                count += len(docs)
            logger.info("Ingested %d county program chunks from %s", count, county_name)

    # Ingest SAM.gov federal assistance listings
    sam_dir = RAW_DIR / "sam_gov"
    if sam_dir.exists() and any(sam_dir.glob("*.json")):
        from navigator.rag.ingest import chunk_text, _make_id
        count = 0
        for sam_file in sorted(sam_dir.glob("*.json")):
            listing = json.loads(sam_file.read_text())
            text_parts = []
            if listing.get("name"):
                text_parts.append(listing["name"])
            if listing.get("description"):
                text_parts.append(listing["description"])
            if listing.get("eligibility_summary"):
                text_parts.append(f"Eligibility: {listing['eligibility_summary']}")
            if listing.get("agency"):
                text_parts.append(f"Agency: {listing['agency']}")
            if listing.get("application_url"):
                text_parts.append(f"More info: {listing['application_url']}")
            full_text = "\n\n".join(text_parts)
            chunks = chunk_text(full_text)
            docs = []
            for i, chunk in enumerate(chunks):
                doc_id = _make_id(chunk, prefix=f"sam_{listing.get('cfda_number', sam_file.stem)}")
                docs.append({
                    "id": doc_id,
                    "text": chunk,
                    "metadata": {
                        "jurisdiction": "federal",
                        "category": listing.get("category", "general"),
                        "program": listing.get("name", ""),
                        "source": listing.get("application_url", "SAM.gov"),
                        "cfda_number": listing.get("cfda_number", ""),
                        "chunk_index": i,
                    },
                })
            pipeline._add_docs(docs)
            count += len(docs)
        logger.info("Ingested %d SAM.gov federal listing chunks", count)

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
