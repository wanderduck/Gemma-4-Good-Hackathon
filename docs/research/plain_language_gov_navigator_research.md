# Plain Language Government Navigator - Data & API Research

*Research compiled: 2026-04-05 for the Gemma 4 Good Hackathon*

---

## 1. Government Benefits / Services APIs

### 1.1 NYC Benefits Screening API (TOP PICK)

- **URL**: https://screeningapidocs.cityofnewyork.us/
- **GitHub**: https://github.com/CityOfNewYork/screeningapi-docs
- **What it does**: Accepts household composition data (income, household size, ages, etc.) and returns eligibility determinations for 40+ Federal, State, and City programs including SNAP, Cash Assistance, WIC, HEAP, Medicaid/CHIP. No PII required.
- **Access**: Free, public API with token-based authentication.
- **License**: Open source documentation (NYC Opportunity).
- **Competition compliance**: Excellent -- publicly available, free.
- **How to use**: Core eligibility determination engine. Could serve as the primary "function call" target for the agent. Even if scoped to NYC, it covers major federal programs and demonstrates the concept.
- **Concern**: NYC-specific, but covers federal programs that exist nationwide.

### 1.2 CMS Marketplace API (Healthcare)

- **URL**: https://developer.cms.gov/marketplace-api/
- **What it does**: Health insurance plan data, provider directories, and Medicaid/CHIP eligibility estimates used by HealthCare.gov.
- **Access**: Free API key required (auto-renewing every 60 days).
- **License**: Public government data.
- **How to use**: Healthcare eligibility screening, Medicaid/CHIP income thresholds.

### 1.3 VA Lighthouse API Platform (Veterans)

- **URL**: https://developer.va.gov/
- **GitHub**: https://github.com/department-of-veterans-affairs/vets-api-clients
- **What it does**: Multiple APIs -- Benefits Claims, Community Care Eligibility (MISSION Act), Veteran Service History and Eligibility, Loan Guaranty (VA Home Loans), facilities lookup.
- **Access**: Free API key for sandbox; production requires demo/approval.
- **How to use**: Veterans benefits eligibility checks. Sandbox is sufficient for competition demo.

### 1.4 CareerOneStop APIs (Unemployment & Career)

- **URL**: https://api.careeronestop.org/api-explorer/
- **What it does**: Unemployment insurance info by state (filing URLs, phone numbers, eligibility info), career resources, training programs.
- **Access**: Free API with Bearer Token.
- **License**: U.S. Department of Labor public data.
- **How to use**: Unemployment benefits navigation, linking to state-specific filing resources.

### 1.5 SAM.gov Assistance Listings API (Federal Programs Directory)

- **URL**: https://sam.gov/assistance-listings
- **API**: https://open.gsa.gov/api/ (Assistance Listings Public API)
- **What it does**: Detailed descriptions of 2,200+ federal assistance programs (grants, loans, scholarships, insurance) including authorizing legislation, objectives, eligibility criteria, and compliance requirements. Formerly the Catalog of Federal Domestic Assistance (CFDA).
- **Access**: Free, public API.
- **How to use**: Master directory of all federal programs. Build RAG knowledge base of program descriptions and eligibility criteria.

### 1.6 SSA Open Data (Social Security / Disability)

- **URL**: https://www.ssa.gov/data/
- **What it does**: OASDI beneficiary data by state, disability application statistics. Eligibility questionnaire at ssa.gov/prepare/check-eligibility-for-benefits.
- **Access**: Public datasets and API for beneficiary statistics.
- **Limitation**: No programmatic eligibility determination API -- criteria would need to be encoded manually or extracted from published rules.

### 1.7 HUD Data & APIs (Housing)

- **URL**: https://www.huduser.gov/portal/pdrdatas_landing.html
- **Open Data**: https://hudgis-hud.opendata.arcgis.com/
- **What it does**: Income limits by area (determines Section 8/public housing eligibility), assisted housing data, fair market rents.
- **How to use**: Look up income limits by location to determine housing assistance eligibility.

### 1.8 Federal Register API

- **URL**: https://www.federalregister.gov/developers/documentation/api/v1
- **What it does**: Full-text search and retrieval of Federal Register documents. JSON or CSV. No API key required.
- **License**: Public domain.
- **How to use**: Retrieve current regulations and rule changes affecting benefit programs.

### 1.9 GovInfo API + CFR Bulk Data

- **URL**: https://api.govinfo.gov/docs/
- **Bulk Data**: https://www.govinfo.gov/bulkdata/CFR
- **GitHub**: https://github.com/usgpo/api
- **What it does**: Access to Code of Federal Regulations (CFR), Federal Register, Congressional bills. XML bulk data for CFR back to 1996.
- **Access**: Free API key via api.data.gov.
- **How to use**: Pull actual regulatory text. Key CFR titles: Title 7 (Food/Nutrition), Title 20 (Employees' Benefits), Title 42 (Public Health), Title 45 (Public Welfare).

### 1.10 USA.gov / Benefits Finder

- **URL**: https://www.usa.gov/benefit-finder (replaced benefits.gov in September 2024)
- **What it does**: Interactive questionnaire matching users to 1,000+ federal benefit programs.
- **Limitation**: No structured API -- matching logic is embedded in the web tool. No public data export of rules.
- **How to use**: Reference for program coverage and question flow design.

### 1.11 211 National Data Platform (United Way)

- **URL**: https://www.211.org/
- **Developer Portal**: https://register.211.org/
- **What it does**: Largest database of health and human services in the US. Locally curated. Covers food, housing, utilities, healthcare, employment, crisis services.
- **APIs**: Export API (bulk download) and Search API (keyword/guided search).
- **Access**: Developer portal registration required.
- **License**: Proprietary (curated by individual 211 centers).
- **Competition compliance**: UNCERTAIN -- registration-gated access may or may not meet the "Reasonableness Standard."

### 1.12 Data.gov Benefits Tag

- **URL**: https://catalog.data.gov/dataset/?tags=benefits
- **What it does**: 82+ datasets tagged "benefits" in various formats.
- **Access**: Free, public.

---

## 2. Datasets for Training / Fine-Tuning / RAG

### 2.1 Text Simplification Datasets

| Dataset | Source | Size | License | Competition OK? |
|---|---|---|---|---|
| **WikiAuto** | [HuggingFace](https://huggingface.co/datasets/chaojiang06/wiki_auto) | Hundreds of thousands of aligned pairs | CC BY-SA 3.0 | Yes |
| **Cochrane Simplification** | [HuggingFace](https://huggingface.co/datasets/GEM/cochrane-simplification) | ~4,459 paragraph pairs | CC BY 4.0 | Yes (perfect match) |
| **OneStopEnglish** | [GitHub](https://github.com/nishkalavallabhi/OneStopEnglishCorpus) | 189 texts x 3 levels (567 total) | CC BY-SA 4.0 | Yes |
| **ASSET** | [HuggingFace](https://huggingface.co/datasets/asset) | 2,359 sentences x 10 simplifications | CC BY-NC 4.0 | CONCERN (NC clause) |
| **TurkCorpus** | [HuggingFace](https://huggingface.co/datasets/turk) | 2,359 sentences x 8 simplifications | GNU GPL | Check copyleft |
| **Newsela** | [newsela.com](https://newsela.com/legal/data) | 1,911 articles x 4 levels | NDA required | DISQUALIFIED |

**Recommendation**: WikiAuto (largest, permissive license) + Cochrane (perfect CC-BY 4.0 license, domain-adapted) + OneStopEnglish (multi-level readability).

### 2.2 Legal / Government Text Datasets

| Dataset | Source | Size | License | Notes |
|---|---|---|---|---|
| **StateCodes + LaborBench** | [arXiv](https://arxiv.org/abs/2508.19365) / HuggingFace | 8.7GB (all 50 states' statutes + 45 states' regulations) | Likely public domain | LaborBench has structured unemployment rules for all 50 states across 101 dimensions |
| **Pile of Law** | [HuggingFace](https://huggingface.co/datasets/pile-of-law/pile-of-law) | 256GB | CC BY-NC-SA 4.0 | Government-authored portions are public domain |
| **LegalBench** | [HuggingFace](https://huggingface.co/datasets/nguha/legalbench) | 162 tasks | Mixed (mostly CC BY 4.0) | Legal reasoning evaluation |
| **LegalBench-RAG** | [GitHub](https://github.com/zeroentropy-ai/legalbenchrag) | Retrieval benchmark | Check repo | RAG quality benchmark |

**Top pick**: StateCodes/LaborBench -- provides exactly the kind of structured state-level eligibility rules data needed, with LaborBench specifically covering unemployment insurance law differences across all 50 states.

### 2.3 Government Program Datasets

- **SAM.gov Assistance Listings**: 2,200+ federal program descriptions with eligibility criteria (see API section 1.5)
- **CWED2** (http://cwed2.org/): Comparative welfare entitlements data with eligibility criteria for unemployment, sickness, pensions
- **WIC Public Assistance Data** (Kaggle): https://www.kaggle.com/datasets/jpmiller/publicassistance
- **State Medicaid/CHIP Data**: https://data.medicaid.gov/

---

## 3. Knowledge Bases for RAG

### 3.1 SAM.gov Assistance Listings
The single best source for structured federal program descriptions and eligibility criteria. 2,200+ programs.

### 3.2 CFR Bulk Data (Code of Federal Regulations)
Full regulatory text. Key titles: 7 (Food/Nutrition), 20 (Employees' Benefits), 42 (Public Health), 45 (Public Welfare).

### 3.3 Federal Plain Language Guidelines
- **URL**: https://www.plainlanguage.gov/media/FederalPLGuidelines.pdf
- Public domain. Embed as system prompt instructions for output style.

### 3.4 Open Eligibility Taxonomy
- **GitHub**: https://github.com/auntbertha/openeligibility (also https://github.com/openreferral/openeligibility)
- Standardized taxonomy: Human Services (housing, food, counseling) + Human Situations (veterans, disability, seniors). Available in XML, CSV, JSON, YAML.
- **License**: CC BY-SA 3.0.
- **How to use**: Classification backbone for matching users to services.

### 3.5 Open Referral / HSDS (Human Services Data Specification)
- **URL**: https://docs.openreferral.org/
- **GitHub**: https://github.com/openreferral/specification
- Standardized data format for health/human/social services. OpenAPI-spec'd protocols.
- **License**: CC BY-SA.

### 3.6 plainlanguage.gov
Before/after samples of government writing simplification. Training examples for jargon-to-plain-language transformation.

---

## 4. Existing Open-Source Tools

### 4.1 PolicyEngine US (TOP PICK -- with caveats)
- **GitHub**: https://github.com/PolicyEngine/policyengine-us
- **URL**: https://www.policyengine.org/us
- Complete Python rules engine for the US tax-benefit system across all 50 states. Based on OpenFisca. Includes AI-powered plain language explanations.
- **License**: AGPL-3.0 (OSI-approved).
- **CRITICAL**: AGPL copyleft may conflict with competition's CC-BY 4.0 winner license. Using it as an external API/service (not modifying its source) may be acceptable. Alternatively, use its rules data as reference to build your own permissively-licensed implementation.

### 4.2 OpenFisca
- **GitHub**: https://github.com/openfisca
- Country-independent rules-as-code framework. Used by France, NZ, Australia, Canada.
- **License**: AGPL-3.0 (same concern as PolicyEngine).

### 4.3 CMS BenefitAssist
- **GitHub**: https://github.com/CMSgov/BenefitAssist
- Node.js rules-based eligibility engine. Originally by Intuit, donated to HHS.
- Likely public domain (government work).

### 4.4 HHSIDEAlab Medicaid Eligibility
- **GitHub**: https://github.com/HHSIDEAlab/medicaid_eligibility
- MAGI-based Medicaid income eligibility determination. REST API, no PII.
- Likely public domain (government work).

### 4.5 18F Eligibility Rules Service
- **GitHub**: https://github.com/18F/eligibility-rules-service
- Prototype SNAP eligibility rules as code. Public domain (18F/GSA).

### 4.6 GSA-TTS BEARS (Archived May 2024)
- **GitHub**: https://github.com/GSA-TTS/usagov-benefits-eligibility
- **Rules**: https://github.com/GSA/usagov-benefits-eligibility-rules
- Benefits finder for death, disability, retirement life events. English + Spanish.
- The rules repo contains structured eligibility criteria data.

### 4.7 GSA Public Benefits Studio
- **GitHub**: https://github.com/GSA/public-benefits-studio
- Coordinates government benefits technology efforts.

---

## 5. Competition Compliance Quick Reference

| Resource | Free | License OK | Available to All |
|---|---|---|---|
| NYC Screening API | Yes | Yes | Yes |
| CMS Marketplace API | Yes (key) | Yes | Yes |
| VA Lighthouse | Yes (sandbox) | Yes | Yes |
| CareerOneStop | Yes (token) | Yes | Yes |
| SAM.gov | Yes | Yes (public domain) | Yes |
| PolicyEngine US | Yes | AGPL (copyleft concern) | Yes |
| WikiAuto | Yes | CC BY-SA 3.0 | Yes |
| Cochrane Simplification | Yes | CC BY 4.0 | Yes |
| OneStopEnglish | Yes | CC BY-SA 4.0 | Yes |
| StateCodes/LaborBench | Yes | Likely public domain | Yes |
| Pile of Law | Yes | CC BY-NC-SA (concern) | Yes |
| ASSET | Yes | CC BY-NC (concern) | Yes |
| Newsela | NDA | Restricted | **NO** |
| 211 Data | Registration | Proprietary | **UNCERTAIN** |
| Open Eligibility Taxonomy | Yes | CC BY-SA 3.0 | Yes |
