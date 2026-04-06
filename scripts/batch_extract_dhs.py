"""Batch extract DHS Combined Manual sections from saved MCP Playwright JSON files.

This script processes temporary JSON files created by the MCP Playwright evaluate
tool and converts them to formatted section text files.

Usage:
    # First, use the MCP Playwright to navigate and save each page's text
    # Then run this to process all _temp_*.json files in the output dir
    python scripts/batch_extract_dhs.py
"""

import json
import re
from pathlib import Path

OUTPUT_DIR = Path("data/raw/dhs_combined_manual")

# Map of dDocName -> title for the sections we want
SECTIONS = {
    "cm_001303": "0013.03 - MFIP BASES OF ELIGIBILITY",
    "cm_001306": "0013.06 - SNAP CATEGORICAL ELIGIBILITY/INELIGIBILITY",
    "cm_001309": "0013.09 - MSA BASES OF ELIGIBILITY",
    "cm_001315": "0013.15 - GA BASES OF ELIGIBILITY",
    "cm_001318": "0013.18 - HSP BASES OF ELIGIBILITY",
    "cm_001906": "0019.06 - GROSS INCOME LIMITS",
    "cm_002009": "0020.09 - MFIP ASSISTANCE STANDARDS",
    "cm_002012": "0020.12 - SNAP ASSISTANCE STANDARDS",
    "cm_002018": "0020.18 - GA ASSISTANCE STANDARDS",
    "cm_002021": "0020.21 - MSA ASSISTANCE STANDARDS",
    "cm_002022": "0020.22 - HSP ASSISTANCE STANDARDS",
    "cm_000401": "0004.01 - EMERGENCY GENERAL ASSISTANCE (EGA)",
    "cm_000404": "0004.04 - EXPEDITED SNAP",
    "lp_cm_0019": "19 - GROSS INCOME TEST",
    "lp_cm_0020": "20 - NET INCOME LIMITS",
    "lp_cm_0022": "22 - BUDGETING AND BENEFIT DETERMINATION",
}


def process_temp_file(temp_path: Path, doc_name: str, title: str) -> None:
    raw = temp_path.read_text()
    try:
        text = json.loads(raw)
        if isinstance(text, str):
            pass  # already a string
        else:
            text = str(text)
    except json.JSONDecodeError:
        text = raw

    safe_label = doc_name.lower().replace("lp_cm_", "ch").replace("cm_", "sec")
    out_path = OUTPUT_DIR / f"section_{safe_label}.txt"

    url = (
        f"https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION"
        f"&RevisionSelectionMethod=LatestReleased&dDocName={doc_name}"
    )
    header = (
        f"SOURCE: {url}\n"
        f"SECTION: {doc_name}\n"
        f"TITLE: {title}\n"
        f"{'=' * 72}\n\n"
    )
    out_path.write_text(header + text, encoding="utf-8")
    print(f"  Saved {len(text):,} chars -> {out_path.name}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for temp_file in sorted(OUTPUT_DIR.glob("_temp_*.json")):
        # Extract doc_name from filename: _temp_cm_001303.json -> cm_001303
        stem = temp_file.stem.replace("_temp_", "")
        if stem in SECTIONS:
            print(f"Processing {stem}: {SECTIONS[stem]}")
            process_temp_file(temp_file, stem, SECTIONS[stem])
        else:
            print(f"Skipping unknown section: {stem}")


if __name__ == "__main__":
    main()
