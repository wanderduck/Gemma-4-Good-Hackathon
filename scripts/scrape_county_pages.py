"""Scrape social services pages for the 5 Twin Cities metro counties.

Target URLs (from docs/research/minnesota_benefits_deep_dive.md):
- Ramsey: https://www.ramseycountymn.gov/residents/assistance-support/
- Hennepin: https://www.hennepin.us/en/residents/human-services
- Dakota: https://www.co.dakota.mn.us/HealthFamily/PublicAssistance
- Scott: https://www.scottcountymn.gov/193/Social-Services
- Carver: https://www.carvercountymn.gov/departments/health-human-services

Also scrape CAP agency pages:
- CAPRW: https://www.caprw.org/
- CAP-HC: https://caphennepin.org/
- CAP Agency: https://capagency.org/

Output: data/raw/county_pages/ (one directory per county/agency)

Strategy:
1. For each county, fetch the main social services page
2. Follow links to individual program pages (1-2 levels deep)
3. Extract program descriptions, eligibility info, contacts
4. Save as JSON files with structure matching the Program model
"""

import argparse
import json
import logging
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup, Tag

from navigator.config import RAW_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

OUTPUT_DIR = RAW_DIR / "county_pages"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COUNTY_URLS = {
    "ramsey": "https://www.ramseycountymn.gov/residents/assistance-support/",
    "hennepin": "https://www.hennepin.us/en/residents/human-services",
    "dakota": "https://www.co.dakota.mn.us/HealthFamily/PublicAssistance",
    "scott": "https://www.scottcountymn.gov/193/Social-Services",
    "carver": "https://www.carvercountymn.gov/departments/health-human-services",
}

CAP_URLS = {
    "caprw": "https://www.caprw.org/",
    "cap_hc": "https://caphennepin.org/",
    "cap_agency": "https://capagency.org/",
}

# Keywords that suggest a link leads to a service/program page worth following.
SERVICE_KEYWORDS = re.compile(
    r"(assist|benefit|cash|food|hous|eligib|program|service|apply|snap|mfip|tanf|"
    r"emergency|energy|childcare|child.care|health|medical|mental|dental|transport|"
    r"shelter|rent|utility|utilities|employ|job|train|refugee|senior|disab|veteran|"
    r"immigrant|family|youth|crisis|support|resource|subsid|voucher|wic|heat)",
    re.IGNORECASE,
)

# Link paths/fragments to skip (navigation noise, file downloads we can't parse, etc.)
SKIP_PATTERNS = re.compile(
    r"(mailto:|tel:|javascript:|#|\.pdf$|\.doc$|\.docx$|\.xls$|\.xlsx$|"
    r"login|logout|search|sitemap|privacy|terms|disclaimer|feedback|survey|"
    r"twitter\.com|facebook\.com|linkedin\.com|youtube\.com|instagram\.com|"
    r"google\.com|maps\.google|gis\.|arcgis)",
    re.IGNORECASE,
)

REQUEST_DELAY = 1.5  # seconds between requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; GovernmentBenefitsBot/1.0; "
        "+https://github.com/wanderduck; educational/research use)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def make_client() -> httpx.Client:
    return httpx.Client(
        headers=HEADERS,
        follow_redirects=True,
        timeout=30.0,
    )


def fetch(client: httpx.Client, url: str) -> BeautifulSoup | None:
    """Fetch a URL and return a BeautifulSoup parse tree, or None on error."""
    try:
        log.debug("GET %s", url)
        resp = client.get(url)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")
    except httpx.HTTPStatusError as exc:
        log.warning("HTTP %s for %s", exc.response.status_code, url)
    except httpx.RequestError as exc:
        log.warning("Request error for %s: %s", url, exc)
    return None


# ---------------------------------------------------------------------------
# Content extraction
# ---------------------------------------------------------------------------

# Ordered list of CSS selectors for the main page content area.
# We try each in turn and use the first that yields a non-trivial result.
CONTENT_SELECTORS = [
    "main",
    '[role="main"]',
    "#main-content",
    "#content",
    ".main-content",
    ".page-content",
    ".content-area",
    ".field-body",
    ".entry-content",
    "article",
    ".region-content",         # Drupal
    "#block-system-main",      # Drupal 7
    ".view-content",           # Drupal Views
    ".sfContentBlock",         # Sitefinity
    ".wysiwyg-content",
    ".body-content",
    "section.content",
]

# Tags that are almost always navigation/chrome rather than body content.
NOISE_TAGS = {
    "header", "footer", "nav", "aside",
    "script", "style", "noscript", "iframe",
    "form",  # usually search/login forms
}

# Class/id substrings that mark noise elements even inside the main area.
NOISE_CLASSES = re.compile(
    r"(nav|menu|breadcrumb|sidebar|footer|header|banner|alert|cookie|"
    r"social|share|print|skip|search|pagination|related|promo|ad-|"
    r"widget|modal|dialog|overlay)",
    re.IGNORECASE,
)


def _is_noise(tag: Tag) -> bool:
    """Return True if this element looks like chrome/navigation rather than content."""
    if tag.name in NOISE_TAGS:
        return True
    classes = " ".join(tag.get("class", []))
    tag_id = tag.get("id", "")
    return bool(NOISE_CLASSES.search(classes) or NOISE_CLASSES.search(tag_id))


def _get_content_root(soup: BeautifulSoup) -> Tag:
    """Return the most specific element that contains the main page body."""
    for selector in CONTENT_SELECTORS:
        candidate = soup.select_one(selector)
        if candidate:
            text = candidate.get_text(separator=" ", strip=True)
            if len(text) > 200:  # ignore trivially small results
                return candidate
    # Fallback: strip obvious noise from <body>
    body = soup.find("body") or soup
    return body


def _clean_text(raw: str) -> str:
    """Normalise whitespace and remove zero-width / control chars."""
    raw = re.sub(r"[\u200b\u00ad\ufeff]", "", raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw.strip()


def extract_main_text(soup: BeautifulSoup) -> str:
    """Extract clean body text from the main content area."""
    root = _get_content_root(soup)
    # Remove noisy child elements in-place on a copy so we don't mutate the tree.
    import copy
    root_copy = copy.copy(root)
    for tag in root_copy.find_all(True):
        if _is_noise(tag):
            tag.decompose()
    return _clean_text(root_copy.get_text(separator="\n", strip=True))


def extract_title(soup: BeautifulSoup) -> str:
    """Best-effort page title: h1 > og:title > <title>."""
    h1 = soup.find("h1")
    if h1:
        return _clean_text(h1.get_text())
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return _clean_text(og["content"])
    title_tag = soup.find("title")
    if title_tag:
        return _clean_text(title_tag.get_text())
    return ""


def extract_contact(soup: BeautifulSoup) -> str:
    """Scrape any phone numbers, email addresses, or explicit 'contact' sections."""
    root = _get_content_root(soup)
    text = root.get_text(separator=" ")

    phones = re.findall(
        r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}", text
    )
    emails = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)

    parts: list[str] = []
    if phones:
        # Deduplicate while preserving order.
        seen: set[str] = set()
        unique_phones = []
        for p in phones:
            norm = re.sub(r"[\s\-.()+]", "", p)
            if norm not in seen and len(norm) >= 10:
                seen.add(norm)
                unique_phones.append(p.strip())
        if unique_phones:
            parts.append("Phone: " + ", ".join(unique_phones[:5]))

    if emails:
        seen_emails: set[str] = set()
        unique_emails = []
        for e in emails:
            if e.lower() not in seen_emails:
                seen_emails.add(e.lower())
                unique_emails.append(e)
        parts.append("Email: " + ", ".join(unique_emails[:3]))

    # Look for an explicit address block (crude heuristic).
    address_match = re.search(
        r"\d{1,5}\s[\w\s.]{3,40},\s*(?:MN|Minnesota|Minneapolis|St\.?\s*Paul|"
        r"Eagan|Apple Valley|Shakopee|Chaska|Farmington)\b[^.]{0,50}",
        text,
        re.IGNORECASE,
    )
    if address_match:
        parts.append("Address: " + address_match.group(0).strip())

    return "; ".join(parts)


def extract_eligibility(text: str) -> str:
    """Pull out any paragraph(s) that discuss eligibility, requirements, or who qualifies."""
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    eligibility_kw = re.compile(
        r"(eligib|qualif|requir|income limit|household|age |citizen|resident|"
        r"must be|may apply|who can|who is eligible|to qualify|criteria)",
        re.IGNORECASE,
    )
    matched = [p for p in paragraphs if eligibility_kw.search(p)]
    return " | ".join(matched[:3]) if matched else ""


def classify_program_type(title: str, text: str) -> str:
    """Rough classification of program type from title + body text."""
    combined = (title + " " + text[:500]).lower()
    mapping = [
        (r"food|snap|nutrition|meal", "food_assistance"),
        (r"cash|mfip|tanf|ga\b|general assist|dwp", "cash_assistance"),
        (r"hous|rent|shelter|homeless|evict", "housing"),
        (r"energy|heat|utility|liheap|cool", "energy_utilities"),
        (r"child.?care|day.?care|early.?learn", "childcare"),
        (r"health|medical|medicaid|mnsure|dental|vision|prescri", "healthcare"),
        (r"mental|behavioral|counsel|therapy|substanc|chemical", "mental_health"),
        (r"employ|job|work|train|career|workforce", "employment"),
        (r"transport|bus pass|ride|transit", "transportation"),
        (r"senior|elder|aging|older adult", "senior_services"),
        (r"disab|disability|special.?need|access", "disability_services"),
        (r"veteran|veter", "veteran_services"),
        (r"refugee|immigrant|new.?american|asylee", "refugee_immigrant"),
        (r"youth|teen|young adult|juvenile|child welfare", "youth_services"),
        (r"emergency|crisis|urgent|immediate", "emergency_services"),
    ]
    for pattern, label in mapping:
        if re.search(pattern, combined):
            return label
    return "general_services"


# ---------------------------------------------------------------------------
# Link discovery
# ---------------------------------------------------------------------------


def _same_domain(base_url: str, href: str) -> bool:
    base_host = urlparse(base_url).netloc.lower()
    href_host = urlparse(href).netloc.lower()
    # Accept empty host (relative URL already resolved) or exact match.
    return href_host == "" or href_host == base_host


def collect_service_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    """Return same-domain links that plausibly lead to service/program pages."""
    seen: set[str] = set()
    links: list[str] = []

    for a in soup.find_all("a", href=True):
        raw_href = a["href"].strip()
        if not raw_href or SKIP_PATTERNS.search(raw_href):
            continue

        full_url = urljoin(base_url, raw_href)

        # Must stay on the same site.
        if not _same_domain(base_url, full_url):
            continue

        # Remove fragment.
        full_url = full_url.split("#")[0].rstrip("/")

        if full_url in seen:
            continue

        # Filter by link text or URL containing service-related words.
        link_text = a.get_text(strip=True)
        if SERVICE_KEYWORDS.search(link_text) or SERVICE_KEYWORDS.search(full_url):
            seen.add(full_url)
            links.append(full_url)

    return links


# ---------------------------------------------------------------------------
# Page scraping
# ---------------------------------------------------------------------------


def scrape_page(client: httpx.Client, url: str, source_name: str) -> dict | None:
    """Fetch a single page and return a program dict, or None if it's not useful."""
    soup = fetch(client, url)
    if soup is None:
        return None

    title = extract_title(soup)
    text = extract_main_text(soup)

    if len(text) < 100:
        log.debug("Skipping %s — too little text (%d chars)", url, len(text))
        return None

    contact = extract_contact(soup)
    eligibility = extract_eligibility(text)
    program_type = classify_program_type(title, text)

    return {
        "name": title or url,
        "description": text[:3000],  # cap at 3 kB; full text retained in raw file
        "eligibility": eligibility,
        "contact": contact,
        "url": url,
        "type": program_type,
        "source": source_name,
    }


def save_programs(programs: list[dict], out_dir: Path, filename: str = "programs.json") -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(programs, fh, indent=2, ensure_ascii=False)
    log.info("Saved %d programs → %s", len(programs), out_path)


# ---------------------------------------------------------------------------
# Source scraping (main + follow links)
# ---------------------------------------------------------------------------


def scrape_source(
    client: httpx.Client,
    name: str,
    root_url: str,
    limit: int | None = None,
) -> list[dict]:
    """Scrape one county or CAP agency: root page + 1-2 levels of service links."""
    out_dir = OUTPUT_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resume: load previously saved programs keyed by URL.
    saved_path = out_dir / "programs.json"
    existing_by_url: dict[str, dict] = {}
    if saved_path.exists():
        try:
            with saved_path.open(encoding="utf-8") as fh:
                for prog in json.load(fh):
                    existing_by_url[prog["url"]] = prog
            log.info("[%s] Resuming — %d pages already scraped", name, len(existing_by_url))
        except (json.JSONDecodeError, KeyError):
            log.warning("[%s] Could not load existing programs.json — starting fresh", name)

    programs: list[dict] = list(existing_by_url.values())
    scraped_urls: set[str] = set(existing_by_url.keys())

    def _add(prog: dict) -> None:
        programs.append(prog)
        scraped_urls.add(prog["url"])

    def _should_skip(url: str) -> bool:
        return url in scraped_urls

    # ---- Level 0: root page -----------------------------------------------
    if not _should_skip(root_url):
        log.info("[%s] Fetching root: %s", name, root_url)
        root_prog = scrape_page(client, root_url, name)
        if root_prog:
            _add(root_prog)
        time.sleep(REQUEST_DELAY)

    # ---- Collect level-1 links from root ----------------------------------
    root_soup = fetch(client, root_url)
    time.sleep(REQUEST_DELAY)

    level1_links: list[str] = []
    if root_soup:
        level1_links = collect_service_links(root_soup, root_url)
        log.info("[%s] Found %d level-1 links", name, len(level1_links))

    if limit is not None:
        level1_links = level1_links[:limit]

    # ---- Level 1: individual service pages --------------------------------
    for url in level1_links:
        if _should_skip(url):
            log.debug("[%s] Skip (already scraped): %s", name, url)
            continue

        log.info("[%s] Level-1: %s", name, url)
        soup = fetch(client, url)
        if soup is None:
            time.sleep(REQUEST_DELAY)
            continue

        prog = scrape_page(client, url, name)
        if prog:
            _add(prog)

        # ---- Level 2: follow links from this page --------------------------
        level2_links = collect_service_links(soup, url)
        # Only follow links that are "deeper" than the root (avoid going back up).
        root_path = urlparse(root_url).path.rstrip("/")
        level2_links = [
            lnk for lnk in level2_links
            if urlparse(lnk).path.rstrip("/").startswith(root_path)
            or SERVICE_KEYWORDS.search(lnk)  # always follow strong keyword matches
        ]

        if limit is not None:
            level2_links = level2_links[:max(1, limit // 2)]

        for l2_url in level2_links:
            if _should_skip(l2_url):
                continue
            log.info("[%s] Level-2: %s", name, l2_url)
            time.sleep(REQUEST_DELAY)
            l2_prog = scrape_page(client, l2_url, name)
            if l2_prog:
                _add(l2_prog)

        # Checkpoint: save after every level-1 page to enable resume.
        save_programs(programs, out_dir)
        time.sleep(REQUEST_DELAY)

    # Final save.
    save_programs(programs, out_dir)
    log.info("[%s] Done — %d programs total", name, len(programs))
    return programs


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape Twin Cities county social services pages.",
    )
    parser.add_argument(
        "--county",
        metavar="NAME",
        help=(
            "Scrape a single county or CAP agency by key "
            "(e.g. ramsey, hennepin, caprw). "
            "Omit to scrape all."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Limit number of level-1 pages per source (useful for testing).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable DEBUG logging.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    all_sources = {**COUNTY_URLS, **CAP_URLS}

    if args.county:
        key = args.county.lower()
        if key not in all_sources:
            valid = ", ".join(sorted(all_sources))
            raise SystemExit(f"Unknown source '{key}'. Valid keys: {valid}")
        sources = {key: all_sources[key]}
    else:
        sources = all_sources

    log.info("Scraping %d source(s) → %s", len(sources), OUTPUT_DIR)

    with make_client() as client:
        for name, url in sources.items():
            log.info("=" * 60)
            log.info("Source: %s  (%s)", name, url)
            log.info("=" * 60)
            try:
                scrape_source(client, name, url, limit=args.limit)
            except Exception as exc:
                log.error("[%s] Unhandled error: %s", name, exc, exc_info=True)


if __name__ == "__main__":
    main()
