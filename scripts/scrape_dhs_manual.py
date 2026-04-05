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
