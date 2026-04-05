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
