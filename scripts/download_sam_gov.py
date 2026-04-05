"""Download federal assistance listings from SAM.gov API.

API docs: https://open.gsa.gov/api/assistance-listings-api/
Endpoint: https://api.sam.gov/assistance-listings/v1/search

Output: data/raw/sam_gov/<cfda_number>.json

API key: register at https://sam.gov/profile/details (free, instant)
         set SAM_GOV_API_KEY in .env

Assumptions (from open.gsa.gov docs, verified April 2026):
  - Pagination via `pageNumber` (1-based) and `pageSize` query params
  - Total record count in response root as `totalRecords`
  - Each listing nested under `assistanceListings` array in response
  - CFDA number in `programNumber` field (e.g., "93.714")
  - Program title in `programTitle`
  - Agency in `organizationId` + `agencyName` (top-level org name)
  - `assistanceTypes` is a list of type codes; we don't filter on these —
    we filter on `functionalCodes` / `missionSubCategories` instead
  - Rate limit: ~10 req/min for public key tier; we sleep 6 s between pages
  - `status=Active` returns only active listings (inactive are historical)

Usage:
    PYTHONPATH=src uv run python scripts/download_sam_gov.py
    PYTHONPATH=src uv run python scripts/download_sam_gov.py --limit 50
    PYTHONPATH=src uv run python scripts/download_sam_gov.py --category health
    PYTHONPATH=src uv run python scripts/download_sam_gov.py --category income --limit 20
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

from navigator.config import RAW_DIR

load_dotenv()

OUTPUT_DIR = RAW_DIR / "sam_gov"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.getenv("SAM_GOV_API_KEY", "")
BASE_URL = "https://api.sam.gov/assistance-listings/v1/search"

# Default page size (API max appears to be 100)
PAGE_SIZE = 100

# Seconds to sleep between paginated requests (conservative for public key tier)
REQUEST_DELAY = 6.0

# Seconds to wait before retrying after a rate-limit (429) response
RATE_LIMIT_BACKOFF = 60.0

# Maximum retries per page before giving up
MAX_RETRIES = 3

# ---------------------------------------------------------------------------
# Category configuration
# ---------------------------------------------------------------------------
# Maps our internal category names to SAM.gov `functionalCodes` values.
# These functional/subject-area codes are listed in the CFDA taxonomy.
# Common codes (from SAM.gov CFDA documentation):
#   10 - Agriculture
#   13 - Business and Commerce
#   14 - Community Development
#   15 - Consumer Protection
#   16 - Crime  (Law enforcement)
#   17 - Employment, Labor and Training
#   20 - Transportation
#   93 - Health
#   84 - Education
#   14.xxx - Housing (HUD prefix)
#   10.xxx - USDA/Food programs
# The API also exposes `functionalCodes` as a multi-value filter param.
# Since the exact taxonomy for functional codes is extensive, we use
# keyword matching on programTitle + description as a secondary filter.
# For direct API filtering we target the CFDA two-digit prefix ranges.
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "income": [
        "income", "cash assistance", "tanf", "supplemental security",
        "ssi", "welfare", "poverty", "financial assistance",
        "emergency assistance", "hardship",
    ],
    "food": [
        "food", "nutrition", "snap", "wic", "hunger", "meal",
        "commodity", "school lunch", "breakfast program", "pantry",
        "feeding", "dietary",
    ],
    "health": [
        "health", "medical", "medicaid", "medicare", "mental health",
        "substance abuse", "behavioral health", "clinic", "hospital",
        "dental", "vision", "insurance", "chip", "vaccine", "immunization",
        "maternal", "prenatal", "disability", "rehabilitation",
    ],
    "housing": [
        "housing", "shelter", "rent", "homeless", "voucher",
        "section 8", "affordable housing", "mortgage", "utility",
        "heat", "energy", "low income housing",
    ],
    "employment": [
        "employment", "job", "workforce", "training", "apprenticeship",
        "unemployment", "vocational", "labor", "worker", "reemployment",
        "wage", "career",
    ],
    "education": [
        "education", "school", "college", "university", "student",
        "scholarship", "grant", "head start", "early childhood",
        "literacy", "adult education", "pell", "loan forgiveness",
        "childcare", "child care",
    ],
}

ALL_CATEGORIES = list(CATEGORY_KEYWORDS.keys())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _matches_category(listing: dict, category: str) -> bool:
    """Return True if the listing text matches any keyword for the category."""
    keywords = CATEGORY_KEYWORDS[category]
    title = (listing.get("programTitle") or "").lower()
    desc = (listing.get("objectives") or "").lower()
    text = f"{title} {desc}"
    return any(kw in text for kw in keywords)


def _matches_any_target_category(listing: dict, categories: list[str]) -> bool:
    return any(_matches_category(listing, cat) for cat in categories)


def _infer_category(listing: dict) -> str:
    """Best-effort primary category label for a listing."""
    for cat in ALL_CATEGORIES:
        if _matches_category(listing, cat):
            return cat
    return "other"


def _extract_eligibility(listing: dict) -> str:
    """Pull eligibility text from the nested applicant/beneficiary structure."""
    parts: list[str] = []

    # Direct eligibility field
    elig = listing.get("eligibility") or {}
    if isinstance(elig, dict):
        for key in ("applicant", "beneficiary", "credentials", "documentation"):
            val = elig.get(key)
            if val and isinstance(val, str):
                parts.append(val.strip())

    # Also check top-level eligibility prose fields that SAM uses
    for field in ("eligibilityRequirements", "applicantEligibility", "beneficiaryEligibility"):
        val = listing.get(field)
        if val and isinstance(val, str) and val.strip():
            parts.append(val.strip())

    return " ".join(parts) if parts else ""


def _extract_application_url(listing: dict) -> str:
    """Extract the best application URL from the listing."""
    # SAM.gov links the listing itself; programs may also have their own URL
    cfda = listing.get("programNumber", "")
    if cfda:
        # Canonical SAM.gov listing page URL
        return f"https://sam.gov/fal/{cfda}/view"
    return ""


def _transform_listing(raw: dict) -> dict:
    """Transform a raw SAM.gov listing into our Program-compatible format."""
    cfda = raw.get("programNumber", "").strip()
    title = raw.get("programTitle", "").strip()
    description = (raw.get("objectives") or raw.get("description") or "").strip()
    agency = (
        raw.get("agencyName")
        or raw.get("organizationName")
        or raw.get("department")
        or ""
    ).strip()

    return {
        # Program model fields
        "id": f"sam_gov_{cfda.replace('.', '_')}",
        "cfda_number": cfda,
        "name": title,
        "title": title,
        "category": _infer_category(raw),
        "jurisdiction": "federal",
        "description": description,
        "eligibility_summary": _extract_eligibility(raw),
        "application_url": _extract_application_url(raw),
        "source": "SAM.gov Assistance Listings",
        "agency": agency,
        # Preserve full raw data for ingestion / debugging
        "_raw": raw,
    }


def _listing_path(cfda_number: str) -> Path:
    safe = cfda_number.replace(".", "_").replace("/", "_")
    return OUTPUT_DIR / f"{safe}.json"


# ---------------------------------------------------------------------------
# API fetching
# ---------------------------------------------------------------------------

def fetch_page(
    client: httpx.Client,
    page_number: int,
    page_size: int,
    extra_params: dict | None = None,
) -> dict:
    """Fetch one page of results from the Assistance Listings API.

    Raises httpx.HTTPStatusError for non-retried errors.
    Returns the parsed JSON response dict.
    """
    params: dict = {
        "api_key": API_KEY,
        "pageNumber": page_number,
        "pageSize": page_size,
        "status": "Active",
    }
    if extra_params:
        params.update(extra_params)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.get(BASE_URL, params=params, timeout=30.0)

            if response.status_code == 429:
                wait = RATE_LIMIT_BACKOFF * attempt
                print(
                    f"  [rate limit] 429 received — waiting {wait:.0f}s "
                    f"(attempt {attempt}/{MAX_RETRIES})"
                )
                time.sleep(wait)
                continue

            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException as exc:
            print(f"  [timeout] attempt {attempt}/{MAX_RETRIES}: {exc}")
            if attempt < MAX_RETRIES:
                time.sleep(REQUEST_DELAY * attempt)
            else:
                raise

        except httpx.HTTPStatusError as exc:
            print(f"  [http error] {exc.response.status_code}: {exc}")
            raise

    raise RuntimeError(f"Failed to fetch page {page_number} after {MAX_RETRIES} attempts")


def download_listings(
    categories: list[str],
    limit: int | None,
    resume: bool = True,
) -> tuple[int, int]:
    """Download assistance listings, filter by category, save to disk.

    Returns (saved_count, skipped_count).
    """
    saved = 0
    skipped = 0
    seen = 0

    with httpx.Client() as client:
        page_number = 1
        total_records: int | None = None

        while True:
            print(f"Fetching page {page_number} (page_size={PAGE_SIZE}) ...", end=" ", flush=True)

            try:
                data = fetch_page(client, page_number, PAGE_SIZE)
            except Exception as exc:
                print(f"\n[error] Failed on page {page_number}: {exc}")
                break

            # SAM.gov wraps results in `assistanceListings`
            listings: list[dict] = data.get("assistanceListings", [])

            if total_records is None:
                total_records = data.get("totalRecords", 0)
                print(f"total={total_records}", end=" ")

            print(f"got {len(listings)} listings")

            if not listings:
                print("  No more listings — done.")
                break

            for listing in listings:
                seen += 1
                if limit is not None and (saved + skipped) >= limit:
                    break

                cfda = listing.get("programNumber", "").strip()
                if not cfda:
                    continue

                dest = _listing_path(cfda)

                # Resume: skip already-downloaded files
                if resume and dest.exists():
                    skipped += 1
                    continue

                # Category filter
                if not _matches_any_target_category(listing, categories):
                    continue

                transformed = _transform_listing(listing)
                dest.write_text(json.dumps(transformed, indent=2, default=str))
                saved += 1

                if saved % 25 == 0:
                    print(f"  ... saved {saved} files so far")

            # Check stop conditions
            if limit is not None and (saved + skipped) >= limit:
                print(f"  Reached --limit {limit} — stopping.")
                break

            if total_records is not None and seen >= total_records:
                print("  All records fetched.")
                break

            page_number += 1
            time.sleep(REQUEST_DELAY)

    return saved, skipped


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download SAM.gov federal assistance listings.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Categories: {', '.join(ALL_CATEGORIES)}

Examples:
  PYTHONPATH=src uv run python scripts/download_sam_gov.py
  PYTHONPATH=src uv run python scripts/download_sam_gov.py --limit 100
  PYTHONPATH=src uv run python scripts/download_sam_gov.py --category health --limit 50
  PYTHONPATH=src uv run python scripts/download_sam_gov.py --no-resume
        """,
    )
    parser.add_argument(
        "--category",
        choices=ALL_CATEGORIES,
        default=None,
        help="Filter to a single category (default: all target categories)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Stop after saving/skipping this many total programs",
    )
    parser.add_argument(
        "--no-resume",
        dest="resume",
        action="store_false",
        default=True,
        help="Re-download files that already exist (default: skip existing)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Directory to write JSON files (default: {OUTPUT_DIR})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not API_KEY:
        print(
            "ERROR: SAM_GOV_API_KEY is not set.\n"
            "  1. Register for a free public API key at: https://sam.gov/profile/details\n"
            "  2. Add  SAM_GOV_API_KEY=<your-key>  to your .env file\n"
            "  3. Run again."
        )
        sys.exit(1)

    # Override output directory if user passed --output-dir
    global OUTPUT_DIR
    OUTPUT_DIR = args.output_dir
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    categories = [args.category] if args.category else ALL_CATEGORIES

    print("=" * 60)
    print("SAM.gov Assistance Listings Downloader")
    print(f"  Endpoint : {BASE_URL}")
    print(f"  Output   : {OUTPUT_DIR}")
    print(f"  Category : {args.category or 'all (' + ', '.join(ALL_CATEGORIES) + ')'}")
    print(f"  Limit    : {args.limit or 'none'}")
    print(f"  Resume   : {args.resume}")
    print("=" * 60)

    saved, skipped = download_listings(
        categories=categories,
        limit=args.limit,
        resume=args.resume,
    )

    print()
    print("=" * 60)
    print(f"Done. Saved: {saved}  Skipped (already existed): {skipped}")
    print(f"Files in {OUTPUT_DIR}: {len(list(OUTPUT_DIR.glob('*.json')))}")
    print("=" * 60)


if __name__ == "__main__":
    main()
