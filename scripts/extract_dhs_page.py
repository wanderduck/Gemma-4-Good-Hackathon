"""Helper: extract text from the current Playwright MCP page and save to a file.

Usage (called from the MCP Playwright evaluate tool):
    This script is meant to be run AFTER navigating to a DHS manual page
    via the Playwright MCP tools. It reads a JSON file with page text
    and saves it as a formatted section file.
"""

import json
import sys
from pathlib import Path


def save_section(text: str, doc_name: str, title: str, url: str, output_dir: str) -> None:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    safe_label = doc_name.lower().replace("lp_cm_", "ch").replace("cm_", "")
    out_path = out_dir / f"section_{safe_label}.txt"

    header = (
        f"SOURCE: {url}\n"
        f"SECTION: {doc_name}\n"
        f"TITLE: {title}\n"
        f"{'=' * 72}\n\n"
    )
    out_path.write_text(header + text, encoding="utf-8")
    print(f"Saved {len(text)} chars -> {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python extract_dhs_page.py <json_file> <doc_name> <title> <output_dir>")
        sys.exit(1)

    json_file, doc_name, title, output_dir = sys.argv[1:5]
    text = json.loads(Path(json_file).read_text())
    url = f"https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION&RevisionSelectionMethod=LatestReleased&dDocName={doc_name}"
    save_section(text, doc_name, title, url, output_dir)
