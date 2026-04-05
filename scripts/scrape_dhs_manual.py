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

import argparse
import logging
import re
import time
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse, urljoin

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

# DHS uses Oracle WebCenter Content. Section links use this pattern:
#   /main/idcplg?IdcService=GET_DYNAMIC_CONVERSION&...&dDocName=ID_XXXXXX
# We also accept short relative hrefs that contain IdcService= or dDocName=
SECTION_LINK_RE = re.compile(r"dDocName=(ID_\d+)", re.IGNORECASE)

# Section number patterns seen in link text, e.g. "0001", "0002.05", "9500"
SECTION_NUM_RE = re.compile(r"^\s*(\d[\d.]*)\s")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; MNBenefitsNavigator/1.0; "
        "+https://github.com/wanderduck/gemma4-good-hackathon; "
        "scraping for public-benefit research)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def build_client() -> httpx.Client:
    """Return a reusable httpx client with sensible timeouts."""
    return httpx.Client(
        headers=HEADERS,
        timeout=httpx.Timeout(connect=10.0, read=30.0, write=10.0, pool=5.0),
        follow_redirects=True,
    )


def fetch_page(client: httpx.Client, url: str) -> BeautifulSoup | None:
    """Fetch *url* and return a parsed BeautifulSoup, or None on error."""
    try:
        resp = client.get(url)
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        log.warning("HTTP %s for %s", exc.response.status_code, url)
        return None
    except httpx.RequestError as exc:
        log.warning("Request error for %s: %s", url, exc)
        return None

    return BeautifulSoup(resp.text, "html.parser")


# ---------------------------------------------------------------------------
# Link extraction
# ---------------------------------------------------------------------------


def normalise_href(href: str) -> str:
    """Return an absolute URL given a raw href from the DHS site."""
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return urljoin(MANUAL_TOC, href)


def extract_section_links(soup: BeautifulSoup) -> list[dict]:
    """Pull all section links from the TOC page.

    DHS Combined Manual TOC structure (Oracle WebCenter):
    - The main content lives inside a <div> with id/class containing
      "idcMainContent", "region1", or similar WebCenter identifiers.
    - Section entries are <a> tags whose href contains IdcService=GET_DYNAMIC_CONVERSION
      and a dDocName=ID_XXXXXX parameter.
    - Link text typically begins with a section number like "0001 Introduction".

    We collect every matching <a> across the whole page (not just the main
    content div) to be resilient to layout changes, then deduplicate by dDocName.
    """
    seen_docnames: set[str] = set()
    sections: list[dict] = []

    for a_tag in soup.find_all("a", href=True):
        href: str = a_tag["href"]
        m = SECTION_LINK_RE.search(href)
        if not m:
            continue

        doc_name = m.group(1)  # e.g. "ID_012345"
        if doc_name in seen_docnames:
            continue
        seen_docnames.add(doc_name)

        link_text = a_tag.get_text(" ", strip=True)

        # Try to derive a short section label from the link text.
        # Fall back to the dDocName numeric part.
        num_match = SECTION_NUM_RE.match(link_text)
        if num_match:
            section_label = num_match.group(1).replace(".", "_")
        else:
            # Use the numeric part of dDocName as a fallback label
            section_label = doc_name.replace("ID_", "")

        full_url = normalise_href(href)
        # Ensure the URL uses LatestReleased so we always get published content.
        if "RevisionSelectionMethod" not in full_url:
            parsed = urlparse(full_url)
            qs = parse_qs(parsed.query)
            qs.setdefault("RevisionSelectionMethod", ["LatestReleased"])
            full_url = parsed._replace(query=urlencode(qs, doseq=True)).geturl()

        sections.append(
            {
                "doc_name": doc_name,
                "label": section_label,
                "title": link_text,
                "url": full_url,
            }
        )

    return sections


# ---------------------------------------------------------------------------
# Content extraction
# ---------------------------------------------------------------------------


def extract_text(soup: BeautifulSoup, url: str) -> str:
    """Extract clean plain text from a DHS manual section page.

    DHS WebCenter pages wrap the real content in one of several containers.
    We try a priority list of selectors and fall back to <body> if needed.
    """
    # Priority order: most-specific WebCenter containers first.
    candidate_selectors = [
        {"id": re.compile(r"idcMainContent|mainContent|contentArea", re.I)},
        {"class_": re.compile(r"idcMainContent|mainContent|contentArea", re.I)},
        {"id": re.compile(r"region1|regionMain|bodyContent", re.I)},
        {"class_": re.compile(r"region1|regionMain|bodyContent", re.I)},
        "main",
        "article",
    ]

    content_tag = None
    for selector in candidate_selectors:
        if isinstance(selector, dict):
            content_tag = soup.find(True, **selector)
        else:
            content_tag = soup.find(selector)
        if content_tag:
            break

    if content_tag is None:
        # Last resort: strip the whole body.
        content_tag = soup.find("body") or soup

    # Remove boilerplate navigation / header / footer elements before
    # extracting text, so we don't pollute the content file.
    for unwanted in content_tag.find_all(
        ["nav", "header", "footer", "script", "style", "noscript"],
    ):
        unwanted.decompose()

    # Also remove common DHS nav divs by id/class patterns.
    nav_patterns = re.compile(
        r"nav|header|footer|breadcrumb|sidebar|menu|skip|print|share",
        re.I,
    )
    for tag in content_tag.find_all(True):
        tag_id = tag.get("id", "")
        tag_cls = " ".join(tag.get("class", []))
        if nav_patterns.search(tag_id) or nav_patterns.search(tag_cls):
            tag.decompose()

    # get_text with a newline separator preserves paragraph breaks.
    raw_text = content_tag.get_text("\n", strip=True)

    # Collapse runs of 3+ blank lines to 2 blank lines (keep paragraph breaks
    # but remove excessive whitespace that sometimes comes from table cells).
    cleaned = re.sub(r"\n{3,}", "\n\n", raw_text)
    return cleaned.strip()


# ---------------------------------------------------------------------------
# Main scraping loop
# ---------------------------------------------------------------------------


def scrape_section(
    client: httpx.Client,
    section: dict,
    output_dir: Path,
) -> bool:
    """Fetch one section and write its text to disk. Returns True on success."""
    # Sanitise label for use as a filename.
    safe_label = re.sub(r"[^\w.-]", "_", section["label"])
    out_path = output_dir / f"section_{safe_label}.txt"

    if out_path.exists():
        log.info("SKIP (exists) %s — %s", safe_label, section["title"][:60])
        return True

    log.info("FETCH %s — %s", safe_label, section["title"][:60])
    soup = fetch_page(client, section["url"])
    if soup is None:
        log.error("  Failed to fetch %s", section["url"])
        return False

    text = extract_text(soup, section["url"])
    if len(text) < 50:
        log.warning(
            "  Very short content (%d chars) for %s — selector may be wrong",
            len(text),
            safe_label,
        )

    # Write with a metadata header so the file is self-contained.
    header = (
        f"SOURCE: {section['url']}\n"
        f"SECTION: {section['label']}\n"
        f"TITLE: {section['title']}\n"
        f"DOC_NAME: {section['doc_name']}\n"
        f"{'=' * 72}\n\n"
    )
    out_path.write_text(header + text, encoding="utf-8")
    log.info("  Saved %d chars → %s", len(text), out_path.name)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape the MN DHS Combined Manual into plain-text files."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        metavar="N",
        help="Stop after fetching N sections (0 = no limit; useful for testing).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.5,
        metavar="SECONDS",
        help="Seconds to wait between requests (default: 1.5).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Directory for output files (default: {OUTPUT_DIR}).",
    )
    args = parser.parse_args()

    out_dir: Path = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    log.info("DHS Combined Manual scraper")
    log.info("TOC:        %s", MANUAL_TOC)
    log.info("Output dir: %s", out_dir)
    if args.limit:
        log.info("Limit:      %d sections", args.limit)

    with build_client() as client:
        # ------------------------------------------------------------------
        # Step 1: Fetch and parse the TOC page.
        # ------------------------------------------------------------------
        log.info("Fetching TOC page…")
        toc_soup = fetch_page(client, MANUAL_TOC)
        if toc_soup is None:
            log.error("Cannot fetch TOC page. Aborting.")
            raise SystemExit(1)

        sections = extract_section_links(toc_soup)
        if not sections:
            log.error(
                "No section links found on TOC page. "
                "The site structure may have changed — inspect the page HTML "
                "and update SECTION_LINK_RE or extract_section_links()."
            )
            raise SystemExit(1)

        log.info("Found %d section links.", len(sections))

        # ------------------------------------------------------------------
        # Step 2: Scrape each section.
        # ------------------------------------------------------------------
        if args.limit:
            sections = sections[: args.limit]

        success = 0
        failed = 0
        for i, section in enumerate(sections, start=1):
            log.info("[%d/%d]", i, len(sections))
            ok = scrape_section(client, section, out_dir)
            if ok:
                success += 1
            else:
                failed += 1

            # Polite delay between requests (skip delay after the last one).
            if i < len(sections):
                time.sleep(args.delay)

    log.info("Done. %d succeeded, %d failed.", success, failed)
    log.info("Files in: %s", out_dir)


if __name__ == "__main__":
    main()
