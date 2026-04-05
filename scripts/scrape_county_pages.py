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
2. Follow links to individual program pages
3. Extract program descriptions, eligibility info, contacts
4. Save as JSON files with structure matching the Program model
"""

from pathlib import Path

from navigator.config import RAW_DIR

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


def main():
    print(f"County pages scraper — output to {OUTPUT_DIR}")
    print("Implement scraping logic based on each site's structure.")
    # TODO: Implement for each county and CAP agency


if __name__ == "__main__":
    main()
