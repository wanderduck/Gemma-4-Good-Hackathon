"""Export DHS cookies after solving Radware CAPTCHA.

Opens a visible browser window to the DHS Combined Manual.
Solve the CAPTCHA manually, then press Enter in the terminal.
Cookies are saved for the scraper to reuse.

Usage:
    PYTHONPATH=src uv run python scripts/export_dhs_cookies.py
"""

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from navigator.config import RAW_DIR

COOKIE_FILE = RAW_DIR / "dhs_combined_manual" / "_cookies.json"
DHS_URL = (
    "https://www.dhs.state.mn.us/main/idcplg?IdcService=GET_DYNAMIC_CONVERSION"
    "&RevisionSelectionMethod=LatestReleased&dDocName=CombinedManual"
)


def main():
    COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Opening browser to DHS Combined Manual...")
    print("1. Solve the CAPTCHA in the browser window")
    print("2. Wait for the manual page to fully load")
    print("3. Come back here and press Enter")
    print()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()
        page.goto(DHS_URL, wait_until="domcontentloaded", timeout=60000)

        input(">>> Press Enter after solving the CAPTCHA and the page has loaded... ")

        # Verify we got past the CAPTCHA
        body_text = page.query_selector("body").inner_text()[:300]
        if "solve this captcha" in body_text.lower() or "your activity and behavior" in body_text.lower():
            print("ERROR: Still on CAPTCHA page. Try again.")
            browser.close()
            return

        # Save cookies
        cookies = context.cookies()
        COOKIE_FILE.write_text(json.dumps(cookies, indent=2))
        print(f"Saved {len(cookies)} cookies to {COOKIE_FILE}")

        # Also grab the TOC links while we're here
        links = page.evaluate("""
            () => {
                const results = [];
                document.querySelectorAll('a[href]').forEach(a => {
                    const href = a.getAttribute('href') || '';
                    const text = a.innerText.trim();
                    if (href && text) {
                        results.push({href, text});
                    }
                });
                return results;
            }
        """)
        toc_file = RAW_DIR / "dhs_combined_manual" / "_toc_fresh.json"
        toc_file.write_text(json.dumps(links, indent=2))
        print(f"Saved {len(links)} TOC links to {toc_file}")

        browser.close()

    print("Done! Now run the scraper:")
    print("  PYTHONPATH=src uv run python scripts/scrape_dhs_manual.py")


if __name__ == "__main__":
    main()
