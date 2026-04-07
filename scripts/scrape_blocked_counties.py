"""Scrape bot-blocked county sites using Playwright headless browser.

Targets Carver County and CAP-HC which return 403 to httpx/requests.

Usage:
    PYTHONPATH=src uv run python scripts/scrape_blocked_counties.py
    PYTHONPATH=src uv run python scripts/scrape_blocked_counties.py --county carver
"""

import argparse
import json
import logging
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright, Page

from navigator.config import RAW_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

OUTPUT_DIR = RAW_DIR / "county_pages"

TARGETS = {
    "carver": {
        "root": "https://www.carvercountymn.gov/departments/health-human-services",
        "service_pages": [
            "https://www.carvercountymn.gov/departments/health-human-services/financial-assistance",
            "https://www.carvercountymn.gov/departments/health-human-services/child-family-services",
            "https://www.carvercountymn.gov/departments/health-human-services/mental-health",
            "https://www.carvercountymn.gov/departments/health-human-services/public-health",
        ],
    },
    "cap_hc": {
        "root": "https://caphennepin.org/",
        "service_pages": [
            "https://caphennepin.org/services/",
            "https://caphennepin.org/energy-assistance/",
            "https://caphennepin.org/housing/",
            "https://caphennepin.org/food/",
        ],
    },
}

SERVICE_KEYWORDS = re.compile(
    r"(assist|benefit|cash|food|hous|eligib|program|service|snap|mfip|"
    r"emergency|energy|childcare|child.care|health|medical|mental|dental|"
    r"shelter|rent|utility|employ|job|refugee|senior|disab|veteran|"
    r"family|youth|crisis|support|wic|heat|nutrition)",
    re.IGNORECASE,
)

SKIP_PATTERNS = re.compile(
    r"(mailto:|tel:|javascript:|#|\.pdf$|\.doc|login|logout|search|"
    r"sitemap|privacy|terms|twitter|facebook|linkedin|youtube|instagram)",
    re.IGNORECASE,
)


def extract_page_data(page: Page, url: str, source: str) -> dict | None:
    """Extract program data from a loaded page."""
    title = page.title() or ""
    # Get main content text
    try:
        main_el = page.query_selector("main") or page.query_selector('[role="main"]') or page.query_selector("#content") or page.query_selector(".content")
        if main_el:
            text = main_el.inner_text()
        else:
            text = page.query_selector("body").inner_text()
    except Exception:
        text = page.inner_text("body")

    # Clean text
    text = re.sub(r"[\u200b\u00ad\ufeff]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    if len(text) < 100:
        log.debug("Skipping %s — too little text", url)
        return None

    # Extract contact info
    phones = re.findall(r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}", text)
    phones = list(dict.fromkeys(p.strip() for p in phones if len(re.sub(r"\D", "", p)) >= 10))[:5]
    emails = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    contact_parts = []
    if phones:
        contact_parts.append("Phone: " + ", ".join(phones))
    if emails:
        contact_parts.append("Email: " + ", ".join(list(dict.fromkeys(emails))[:3]))

    # Extract eligibility
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    elig_kw = re.compile(r"(eligib|qualif|requir|income limit|household|must be|who can|criteria)", re.IGNORECASE)
    eligibility = " | ".join(p for p in paragraphs if elig_kw.search(p))[:1000]

    # Classify type
    combined = (title + " " + text[:500]).lower()
    prog_type = "general_services"
    type_map = [
        (r"food|snap|nutrition|meal", "food_assistance"),
        (r"cash|mfip|tanf|ga\b|general assist", "cash_assistance"),
        (r"hous|rent|shelter|homeless", "housing"),
        (r"energy|heat|utility|liheap", "energy_utilities"),
        (r"child.?care|day.?care", "childcare"),
        (r"health|medical|medicaid|dental", "healthcare"),
        (r"mental|behavioral|counsel|therapy", "mental_health"),
        (r"employ|job|work|train|career", "employment"),
        (r"senior|elder|aging", "senior_services"),
        (r"disab|disability", "disability_services"),
        (r"veteran", "veteran_services"),
        (r"refugee|immigrant", "refugee_immigrant"),
        (r"emergency|crisis", "emergency_services"),
    ]
    for pattern, label in type_map:
        if re.search(pattern, combined):
            prog_type = label
            break

    return {
        "name": title or url,
        "description": text[:3000],
        "eligibility": eligibility,
        "contact": "; ".join(contact_parts),
        "url": url,
        "type": prog_type,
        "source": source,
    }


def discover_links(page: Page, base_url: str) -> list[str]:
    """Find service-related links on the current page."""
    links = page.eval_on_selector_all(
        "a[href]",
        "els => els.map(e => ({href: e.href, text: e.innerText}))"
    )
    base_host = urlparse(base_url).netloc.lower()
    seen = set()
    result = []
    for link in links:
        href = link["href"].strip()
        text = link["text"].strip()
        if not href or SKIP_PATTERNS.search(href):
            continue
        parsed = urlparse(href)
        if parsed.netloc.lower() != base_host:
            continue
        clean = href.split("#")[0].rstrip("/")
        if clean in seen:
            continue
        if SERVICE_KEYWORDS.search(text) or SERVICE_KEYWORDS.search(href):
            seen.add(clean)
            result.append(clean)
    return result


def scrape_target(name: str, config: dict) -> list[dict]:
    """Scrape a single target using Playwright."""
    out_dir = OUTPUT_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    programs = []
    scraped_urls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Scrape root page
        root_url = config["root"]
        log.info("[%s] Root: %s", name, root_url)
        try:
            page.goto(root_url, wait_until="networkidle", timeout=30000)
            time.sleep(2)
            prog = extract_page_data(page, root_url, name)
            if prog:
                programs.append(prog)
                scraped_urls.add(root_url)

            # Discover additional links from root
            discovered = discover_links(page, root_url)
            log.info("[%s] Discovered %d links from root", name, len(discovered))
        except Exception as e:
            log.warning("[%s] Root page error: %s", name, e)
            discovered = []

        # Combine discovered + predefined service pages
        all_urls = list(dict.fromkeys(config.get("service_pages", []) + discovered))

        for url in all_urls:
            if url in scraped_urls:
                continue
            log.info("[%s] Scraping: %s", name, url)
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(1.5)
                prog = extract_page_data(page, url, name)
                if prog:
                    programs.append(prog)
                    scraped_urls.add(url)

                    # Follow one level deeper
                    sub_links = discover_links(page, url)
                    for sub_url in sub_links[:5]:
                        if sub_url in scraped_urls:
                            continue
                        log.info("[%s]   Sub: %s", name, sub_url)
                        try:
                            page.goto(sub_url, wait_until="networkidle", timeout=30000)
                            time.sleep(1.5)
                            sub_prog = extract_page_data(page, sub_url, name)
                            if sub_prog:
                                programs.append(sub_prog)
                                scraped_urls.add(sub_url)
                        except Exception as e:
                            log.warning("[%s]   Sub error: %s", name, e)
            except Exception as e:
                log.warning("[%s] Error on %s: %s", name, url, e)

        browser.close()

    # Save
    out_path = out_dir / "programs.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(programs, f, indent=2, ensure_ascii=False)
    log.info("[%s] Saved %d programs -> %s", name, len(programs), out_path)
    return programs


def main():
    parser = argparse.ArgumentParser(description="Scrape bot-blocked county sites with Playwright")
    parser.add_argument("--county", help="Scrape single target (carver, cap_hc)")
    args = parser.parse_args()

    targets = TARGETS
    if args.county:
        key = args.county.lower()
        if key not in targets:
            raise SystemExit(f"Unknown target '{key}'. Valid: {', '.join(targets)}")
        targets = {key: targets[key]}

    for name, config in targets.items():
        log.info("=" * 60)
        log.info("Target: %s", name)
        log.info("=" * 60)
        try:
            scrape_target(name, config)
        except Exception as e:
            log.error("[%s] Failed: %s", name, e, exc_info=True)


if __name__ == "__main__":
    main()
