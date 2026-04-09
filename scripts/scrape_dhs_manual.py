"""Scrape the DHS Combined Manual for cash/food eligibility rules.

Uses Playwright (headless Chromium) to bypass Radware bot protection on the
DHS site.  The httpx-based version gets CAPTCHA-blocked after the first request.

Target: https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION
        &RevisionSelectionMethod=LatestReleased&dDocName=CombinedManual

Output: data/raw/dhs_combined_manual/ (one file per section)

Key sections to scrape:
- Gross income limits, assistance standards, benefit amounts
- MFIP, SNAP, GA, HSP, MSA, RCA, Emergency programs

Usage:
    PYTHONPATH=src uv run python scripts/scrape_dhs_manual.py
    PYTHONPATH=src uv run python scripts/scrape_dhs_manual.py --limit 5
    PYTHONPATH=src uv run python scripts/scrape_dhs_manual.py --sections cm_001906,cm_001306
"""

import argparse
import logging
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, Page, Browser

from navigator.config import RAW_DIR

OUTPUT_DIR = RAW_DIR / "dhs_combined_manual"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://www.dhs.state.mn.us"
MANUAL_TOC = (
    f"{BASE_URL}/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION"
    "&RevisionSelectionMethod=LatestReleased&dDocName=CombinedManual"
)

# Section links: dDocName=cm_XXXXXX or lp_cm_XXXX (chapter landing pages)
SECTION_LINK_RE = re.compile(r"dDocName=((?:lp_)?cm_[\w]+)", re.IGNORECASE)

# Section number patterns in link text: "0001", "0002.05", etc.
SECTION_NUM_RE = re.compile(r"^\s*(\d[\d.]*)\s")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Content extraction
# ---------------------------------------------------------------------------

NOISE_SELECTORS = [
    "nav", "header", "footer", "script", "style", "noscript",
    "[class*='nav']", "[class*='menu']", "[class*='breadcrumb']",
    "[class*='sidebar']", "[class*='header']", "[class*='footer']",
    "[id*='nav']", "[id*='menu']", "[id*='breadcrumb']",
    "[id*='sidebar']", "[id*='header']", "[id*='footer']",
]

CONTENT_SELECTORS = [
    "#idcMainContent", "#mainContent", "#contentArea",
    "#region1", "#regionMain", "#bodyContent",
    "[class*='idcMainContent']", "[class*='mainContent']",
    "main", "article", "#content", ".content",
]


def extract_text_from_page(page: Page, url: str) -> str:
    """Extract clean text from the current page using Playwright's DOM API."""
    # Remove noise elements first
    for selector in NOISE_SELECTORS:
        try:
            page.evaluate(f"""
                document.querySelectorAll('{selector}').forEach(el => el.remove());
            """)
        except Exception:
            pass

    # Try content-specific selectors
    for selector in CONTENT_SELECTORS:
        try:
            el = page.query_selector(selector)
            if el:
                text = el.inner_text()
                if len(text.strip()) > 100:
                    return _clean_text(text)
        except Exception:
            continue

    # Fallback: entire body
    try:
        text = page.query_selector("body").inner_text()
        return _clean_text(text)
    except Exception:
        return ""


def _clean_text(text: str) -> str:
    """Normalize whitespace."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Link extraction from TOC
# ---------------------------------------------------------------------------


def _links_to_sections(links: list[dict]) -> list[dict]:
    """Convert raw link dicts to section dicts, filtering for CM links."""
    seen: set[str] = set()
    sections: list[dict] = []

    for link in links:
        href = link.get("href", "")
        text = link.get("text", "")

        m = SECTION_LINK_RE.search(href)
        if not m:
            continue

        doc_name = m.group(1)
        if doc_name.lower() in seen:
            continue
        seen.add(doc_name.lower())

        # Derive section label
        num_match = SECTION_NUM_RE.match(text)
        if num_match:
            label = num_match.group(1).replace(".", "_")
        else:
            label = doc_name.lower().replace("cm_", "").replace("lp_", "")

        # Build full URL
        full_url = (
            f"{BASE_URL}/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION"
            f"&RevisionSelectionMethod=LatestReleased&dDocName={doc_name}"
        )

        sections.append({
            "doc_name": doc_name,
            "label": label,
            "title": text[:120],
            "url": full_url,
        })

    return sections


def extract_section_links(page: Page) -> list[dict]:
    """Extract all CM section links from the TOC page."""
    links = page.evaluate("""
        () => {
            const results = [];
            document.querySelectorAll('a[href]').forEach(a => {
                const href = a.getAttribute('href') || '';
                const text = a.innerText.trim();
                if (href && text) {
                    results.push({href: href, text: text});
                }
            });
            return results;
        }
    """)
    return _links_to_sections(links)


def load_cached_toc() -> list[dict]:
    """Load section links from a previously cached TOC JSON file."""
    import json

    # Prefer fresh TOC from export_dhs_cookies.py
    fresh = OUTPUT_DIR / "_toc_fresh.json"
    if fresh.exists():
        links = json.loads(fresh.read_text())
        return _links_to_sections(links)

    # Fall back to old cached TOC (double-encoded)
    cached = OUTPUT_DIR / "_toc_all_links.json"
    if not cached.exists():
        return []
    raw = cached.read_text()
    links = json.loads(json.loads(raw))
    return _links_to_sections(links)


def expand_chapter_pages(page: Page, chapters: list[dict], delay: float) -> list[dict]:
    """For lp_cm_XXXX chapter pages, fetch them and extract subsection links."""
    all_sections = []
    for ch in chapters:
        if not ch["doc_name"].lower().startswith("lp_cm_"):
            all_sections.append(ch)
            continue

        log.info("Expanding chapter: %s — %s", ch["doc_name"], ch["title"][:60])
        try:
            page.goto(ch["url"], wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
        except Exception as e:
            log.warning("  Cannot load chapter page %s: %s", ch["doc_name"], e)
            # Still include the chapter page itself
            all_sections.append(ch)
            continue

        # Check for bot challenge
        body_text = ""
        try:
            body_text = page.query_selector("body").inner_text()[:200]
        except Exception:
            pass
        if "solve this captcha" in body_text.lower() or "your activity and behavior" in body_text.lower():
            log.warning("  Bot challenge on chapter page %s — skipping expansion", ch["doc_name"])
            all_sections.append(ch)
            continue

        sub_sections = extract_section_links(page)
        if sub_sections:
            log.info("  Found %d subsections in %s", len(sub_sections), ch["doc_name"])
            all_sections.extend(sub_sections)
        else:
            # No subsections found, keep the chapter page itself
            all_sections.append(ch)

        time.sleep(delay)

    return all_sections


# ---------------------------------------------------------------------------
# Scraping
# ---------------------------------------------------------------------------


def scrape_section(page: Page, section: dict, output_dir: Path, delay: float) -> bool:
    """Navigate to a section page and save its text. Returns True on success."""
    safe_label = re.sub(r"[^\w.-]", "_", section["label"])
    out_path = output_dir / f"section_{safe_label}.txt"

    if out_path.exists():
        log.info("SKIP (exists) %s — %s", safe_label, section["title"][:60])
        return True

    log.info("FETCH %s — %s", safe_label, section["title"][:60])

    try:
        page.goto(section["url"], wait_until="domcontentloaded", timeout=30000)
        # Extra wait for JS-rendered content
        page.wait_for_timeout(2000)
    except Exception as e:
        log.error("  Navigation failed for %s: %s", section["url"], e)
        return False

    text = extract_text_from_page(page, section["url"])

    if len(text) < 50:
        log.warning("  Very short content (%d chars) for %s", len(text), safe_label)

    # Check for bot challenge page
    if "your activity and behavior" in text.lower() or "solve this captcha" in text.lower():
        log.error("  Bot challenge detected for %s — try increasing delay", safe_label)
        return False

    header = (
        f"SOURCE: {section['url']}\n"
        f"SECTION: {section['label']}\n"
        f"TITLE: {section['title']}\n"
        f"DOC_NAME: {section['doc_name']}\n"
        f"{'=' * 72}\n\n"
    )
    out_path.write_text(header + text, encoding="utf-8")
    log.info("  Saved %d chars -> %s", len(text), out_path.name)

    time.sleep(delay)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape the MN DHS Combined Manual using Playwright (headless browser)."
    )
    parser.add_argument(
        "--limit", type=int, default=0, metavar="N",
        help="Stop after N sections (0 = no limit).",
    )
    parser.add_argument(
        "--delay", type=float, default=2.0, metavar="SECONDS",
        help="Seconds between requests (default: 2.0).",
    )
    parser.add_argument(
        "--sections", type=str, default="",
        help="Comma-separated dDocName values to fetch (e.g., cm_001906,cm_001306). "
             "If set, only these sections are fetched.",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=OUTPUT_DIR,
        help=f"Output directory (default: {OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--headed", action="store_true",
        help="Run with visible browser window (for debugging).",
    )
    args = parser.parse_args()

    out_dir: Path = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # Filter list if --sections is provided
    target_sections = set()
    if args.sections:
        target_sections = {s.strip().lower() for s in args.sections.split(",")}

    log.info("DHS Combined Manual scraper (Playwright)")
    log.info("TOC:        %s", MANUAL_TOC)
    log.info("Output dir: %s", out_dir)

    # Check for exported cookies from export_dhs_cookies.py
    cookie_file = OUTPUT_DIR / "_cookies.json"

    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )

        # Load cookies if available (bypasses Radware CAPTCHA)
        if cookie_file.exists():
            import json as _json
            cookies = _json.loads(cookie_file.read_text())
            context.add_cookies(cookies)
            log.info("Loaded %d cookies from %s", len(cookies), cookie_file.name)

        page = context.new_page()

        # Step 1: Load TOC (live, fresh cached, or old cached fallback)
        log.info("Loading TOC page...")
        sections = []
        try:
            page.goto(MANUAL_TOC, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)

            # Check for bot challenge
            body_text = page.query_selector("body").inner_text()[:300]
            if "solve this captcha" in body_text.lower() or "your activity and behavior" in body_text.lower():
                log.warning("Bot challenge detected on TOC page — falling back to cached TOC")
            else:
                sections = extract_section_links(page)
        except Exception as e:
            log.warning("Cannot load TOC page: %s — trying cached TOC", e)

        # Fallback to cached TOC
        if not sections:
            sections = load_cached_toc()
            if sections:
                log.info("Loaded %d sections from cached TOC", len(sections))
            else:
                log.error("No section links found (live or cached). Cannot proceed.")
                browser.close()
                raise SystemExit(1)

        # Step 2: Expand chapter landing pages into subsections
        chapters = [s for s in sections if s["doc_name"].lower().startswith("lp_cm_")]
        if chapters:
            log.info("Found %d chapter pages to expand...", len(chapters))
            sections = expand_chapter_pages(page, sections, args.delay)

        log.info("Total sections to scrape: %d", len(sections))

        # Filter by --sections if provided
        if target_sections:
            sections = [s for s in sections if s["doc_name"].lower() in target_sections]
            log.info("Filtered to %d target sections.", len(sections))

        # Apply --limit
        if args.limit:
            sections = sections[:args.limit]
            log.info("Limited to %d sections.", len(sections))

        # Step 3: Scrape each section
        success = 0
        failed = 0
        for i, section in enumerate(sections, start=1):
            log.info("[%d/%d]", i, len(sections))
            ok = scrape_section(page, section, out_dir, args.delay)
            if ok:
                success += 1
            else:
                failed += 1

        browser.close()

    log.info("Done. %d succeeded, %d failed.", success, failed)
    log.info("Files in: %s", out_dir)


if __name__ == "__main__":
    main()
