"""Targeted DHS scraper: scrape specific chapter sections immediately on discovery.

Unlike scrape_dhs_manual.py (which discovers ALL sections first, then scrapes),
this script visits each chapter page and scrapes its subsections before moving
on. If the bot deterrent triggers mid-run, you keep everything scraped so far.

Usage:
    # Scrape chapters 14-18, 22-24, 26-28
    PYTHONPATH=src uv run python scripts/scrape_dhs_sections.py 14-18 22-24 26-28

    # Scrape individual chapters
    PYTHONPATH=src uv run python scripts/scrape_dhs_sections.py 14 15 22

    # With headed browser (for CAPTCHA solving)
    PYTHONPATH=src uv run python scripts/scrape_dhs_sections.py --headed 14-18 22-24 26-28

    # Slower delay to avoid bot detection
    PYTHONPATH=src uv run python scripts/scrape_dhs_sections.py --delay 5 14-18
"""

import argparse
import logging
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, Page, Browser

from navigator.config import RAW_DIR

OUTPUT_DIR = RAW_DIR / "dhs_combined_manual"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://www.dhs.state.mn.us"
SECTION_LINK_RE = re.compile(r"dDocName=((?:lp_)?cm_[\w]+)", re.IGNORECASE)
SECTION_NUM_RE = re.compile(r"^\s*(\d[\d.]*)\s")

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def _clean_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_text(page: Page) -> str:
    """Extract clean text from the current page."""
    for selector in NOISE_SELECTORS:
        try:
            page.evaluate(f"document.querySelectorAll('{selector}').forEach(el => el.remove());")
        except Exception:
            pass

    for selector in CONTENT_SELECTORS:
        try:
            el = page.query_selector(selector)
            if el:
                text = el.inner_text()
                if len(text.strip()) > 100:
                    return _clean_text(text)
        except Exception:
            continue

    try:
        return _clean_text(page.query_selector("body").inner_text())
    except Exception:
        return ""


def is_captcha(text: str) -> bool:
    """Check if page content is a bot challenge."""
    lower = text.lower()
    return "solve this captcha" in lower or "your activity and behavior" in lower or "verifying your browser" in lower


def extract_subsection_links(page: Page) -> list[dict]:
    """Extract CM subsection links from the current page."""
    links = page.evaluate("""
        () => {
            const results = [];
            document.querySelectorAll('a[href]').forEach(a => {
                const href = a.getAttribute('href') || '';
                const text = a.innerText.trim();
                if (href && text) results.push({href, text});
            });
            return results;
        }
    """)

    seen = set()
    sections = []
    for link in links:
        href = link.get("href", "")
        text = link.get("text", "")

        m = SECTION_LINK_RE.search(href)
        if not m:
            continue

        doc_name = m.group(1)
        # Skip chapter landing pages themselves — we want leaf sections
        if doc_name.lower().startswith("lp_cm_"):
            continue
        if doc_name.lower() in seen:
            continue
        seen.add(doc_name.lower())

        num_match = SECTION_NUM_RE.match(text)
        if num_match:
            label = num_match.group(1).replace(".", "_")
        else:
            label = doc_name.lower().replace("cm_", "")

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


def scrape_page(page: Page, section: dict, output_dir: Path, delay: float) -> bool:
    """Navigate to a section and save its text. Returns True on success."""
    safe_label = re.sub(r"[^\w.-]", "_", section["label"])
    out_path = output_dir / f"section_{safe_label}.txt"

    if out_path.exists() and out_path.stat().st_size > 500:
        log.info("  SKIP (exists, %d bytes) %s", out_path.stat().st_size, safe_label)
        return True

    # Delete stub files from previous failed runs
    if out_path.exists():
        out_path.unlink()

    log.info("  FETCH %s — %s", safe_label, section["title"][:60])

    try:
        page.goto(section["url"], wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
    except Exception as e:
        log.error("  Navigation failed: %s", e)
        return False

    text = extract_text(page)

    if is_captcha(text):
        log.error("  BOT CHALLENGE — stopping this chapter")
        return False

    if len(text) < 50:
        log.warning("  Very short content (%d chars), skipping save", len(text))
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


def parse_section_ranges(args: list[str]) -> list[int]:
    """Parse section arguments like '14-18', '22', '26-28' into a sorted list of ints."""
    chapters = set()
    for arg in args:
        if "-" in arg:
            parts = arg.split("-", 1)
            start, end = int(parts[0]), int(parts[1])
            chapters.update(range(start, end + 1))
        else:
            chapters.add(int(arg))
    return sorted(chapters)


def main():
    parser = argparse.ArgumentParser(
        description="Targeted DHS scraper — scrape specific chapters immediately on discovery.",
    )
    parser.add_argument(
        "chapters", nargs="*",
        help="Chapter numbers or ranges (e.g., 14-18 22-24 26-28). "
             "If omitted, prompts interactively.",
    )
    parser.add_argument("--delay", type=float, default=3.0, help="Seconds between requests (default: 3.0)")
    parser.add_argument("--headed", action="store_true", help="Show browser window")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    # Interactive prompt if no chapters specified
    if not args.chapters:
        print("Enter chapter numbers/ranges to scrape (e.g., 14-18 22-24 26-28):")
        user_input = input("> ").strip()
        if not user_input:
            print("No chapters specified. Exiting.")
            sys.exit(0)
        args.chapters = user_input.split()

    chapters = parse_section_ranges(args.chapters)
    log.info("Target chapters: %s", chapters)

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    cookie_file = OUTPUT_DIR / "_cookies.json"

    total_scraped = 0
    total_skipped = 0
    total_failed = 0
    captcha_hit = False

    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )

        if cookie_file.exists():
            import json
            cookies = json.loads(cookie_file.read_text())
            context.add_cookies(cookies)
            log.info("Loaded %d cookies from %s", len(cookies), cookie_file.name)

        page = context.new_page()

        for ch_num in chapters:
            if captcha_hit:
                log.warning("Bot deterrent active — skipping remaining chapters")
                break

            doc_name = f"lp_cm_{ch_num:04d}"
            ch_url = (
                f"{BASE_URL}/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION"
                f"&RevisionSelectionMethod=LatestReleased&dDocName={doc_name}"
            )

            log.info("=== Chapter %d (%s) ===", ch_num, doc_name)

            try:
                page.goto(ch_url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(2000)
            except Exception as e:
                log.error("Cannot load chapter %d: %s", ch_num, e)
                total_failed += 1
                continue

            # Check for bot challenge on the chapter page
            body_text = ""
            try:
                body_text = page.query_selector("body").inner_text()[:300]
            except Exception:
                pass

            if is_captcha(body_text):
                log.error("BOT CHALLENGE on chapter %d — stopping", ch_num)
                if args.headed:
                    log.info("Solve the CAPTCHA in the browser, then press Enter to continue...")
                    input("Press Enter after solving CAPTCHA> ")
                    # Retry the page
                    try:
                        page.goto(ch_url, wait_until="domcontentloaded", timeout=30000)
                        page.wait_for_timeout(2000)
                        body_text = page.query_selector("body").inner_text()[:300]
                        if is_captcha(body_text):
                            log.error("Still blocked after CAPTCHA. Stopping.")
                            captcha_hit = True
                            continue
                    except Exception:
                        captcha_hit = True
                        continue
                else:
                    captcha_hit = True
                    continue

            # Extract subsection links from this chapter page
            subsections = extract_subsection_links(page)

            if not subsections:
                # Maybe the chapter page itself IS the content (no subsections)
                log.info("No subsections found — scraping chapter page directly")
                section_info = {
                    "doc_name": doc_name,
                    "label": str(ch_num),
                    "title": f"Chapter {ch_num}",
                    "url": ch_url,
                }
                text = extract_text(page)
                if not is_captcha(text) and len(text) > 100:
                    safe_label = str(ch_num)
                    out_path = out_dir / f"section_{safe_label}.txt"
                    header = (
                        f"SOURCE: {ch_url}\n"
                        f"SECTION: {ch_num}\n"
                        f"TITLE: Chapter {ch_num}\n"
                        f"DOC_NAME: {doc_name}\n"
                        f"{'=' * 72}\n\n"
                    )
                    out_path.write_text(header + text, encoding="utf-8")
                    log.info("  Saved chapter page: %d chars", len(text))
                    total_scraped += 1
                continue

            log.info("Found %d subsections — scraping immediately", len(subsections))

            # Scrape each subsection right now, before moving to next chapter
            for i, sub in enumerate(subsections, 1):
                log.info("[%d/%d in ch.%d]", i, len(subsections), ch_num)
                ok = scrape_page(page, sub, out_dir, args.delay)
                if ok:
                    if "SKIP" not in "":  # scrape_page logs SKIP internally
                        total_scraped += 1
                else:
                    # Check if it was a CAPTCHA
                    try:
                        check = page.query_selector("body").inner_text()[:200]
                    except Exception:
                        check = ""
                    if is_captcha(check):
                        if args.headed:
                            log.info("Solve the CAPTCHA in the browser, then press Enter...")
                            input("Press Enter after solving CAPTCHA> ")
                            # Retry this specific section
                            ok = scrape_page(page, sub, out_dir, args.delay)
                            if ok:
                                total_scraped += 1
                            else:
                                total_failed += 1
                        else:
                            log.error("Bot deterrent hit at ch.%d subsection %d — stopping chapter", ch_num, i)
                            captcha_hit = True
                            total_failed += len(subsections) - i
                            break
                    else:
                        total_failed += 1

            time.sleep(args.delay)

        browser.close()

    log.info("Done. Scraped: %d, Skipped: %d, Failed: %d", total_scraped, total_skipped, total_failed)
    if captcha_hit:
        log.info("Bot deterrent interrupted the run. Rerun with remaining chapters.")
        remaining = [c for c in chapters if c >= chapters[chapters.index(ch_num)]]
        log.info("Suggested rerun: PYTHONPATH=src uv run python scripts/scrape_dhs_sections.py --headed %s",
                 " ".join(str(c) for c in remaining))


if __name__ == "__main__":
    main()
