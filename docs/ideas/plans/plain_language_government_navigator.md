# Comprehensive Plan: Plain Language Government Navigator

## The Problem

Government benefits in the United States are a labyrinth. Across federal, state, and county levels, dozens of programs exist to help people in crisis — but finding and understanding them requires navigating bureaucratic jargon, multi-step eligibility questionnaires, and jurisdictional complexity that defeats even motivated applicants.

The numbers tell the story:
- **26 million Americans** eligible for SNAP don't receive it
- An estimated **$60+ billion** in federal benefits go unclaimed annually
- Minnesota alone has **15+ state-level programs** administered across **4 different agencies** (DHS, DCYF, DEED, Commerce) — a restructuring in July 2024 split programs between DHS and the new DCYF, creating confusion even among caseworkers
- Non-English speakers and low-literacy populations are disproportionately excluded
- The closest existing tool in Minnesota (**Bridge to Benefits**) is a 12-question web form covering ~12 programs — not conversational, not multilingual, no county-specific guidance

**No existing tool combines conversational AI, comprehensive program coverage (health/cash/food/housing/energy/employment/childcare), county-specific guidance, and plain-language explanations.**

---

## The Solution

An AI-powered benefits navigator powered by Gemma 4 that takes a plain-language description of someone's situation and returns a personalized, prioritized list of every program they may qualify for — with plain-language eligibility explanations, required documents, and direct application links. In their language, at their reading level.

**Example interaction:**
> **User:** "I'm a single mom with two kids, ages 3 and 7. I just got laid off from my warehouse job where I made $32K. We're in Ramsey County and I'm worried about paying rent and feeding my kids."
>
> **Navigator:** Returns 9 programs (SNAP, MFIP, Unemployment Insurance, Emergency Assistance, Medical Assistance, CCAP, Energy Assistance, Ramsey County Dislocated Worker Program, CAPRW services), a consolidated document checklist, and grouped application links (MNbenefits.mn.gov, uimn.org, mnsure.org, ramseycountymn.gov, caprw.org) — all in plain language with cited sources.

---

## Scope

### Three-Tier Jurisdiction Model

| Tier | Scope | Programs |
|------|-------|----------|
| **Federal** | ~15-20 major programs | SNAP, Medicaid, SSI/SSDI, EITC, CTC, Section 8, WIC, LIHEAP, TANF, UI, Veterans benefits, Pell Grants, ACA marketplace, school meals, Head Start |
| **Minnesota State** | 15+ state programs | MFIP, Medical Assistance, MinnesotaCare, GA, MSA, DWP, CCAP, EAP, MFAP, Housing Support, Bridging Benefits, Dislocated Worker, CLIMB, SNAP E&T, CareerForce |
| **County** | 5 Twin Cities metro counties | Ramsey (Dislocated Worker Program, CAPRW), Hennepin (Pathways, CAP-HC, SNAP E&T), Dakota (CAP Agency), Scott (CAP Agency), Carver (CAP Agency) |

### Multilingual Support

Primary: **English**, **Spanish**
Secondary (beta): **Hmong**, **Somali**, **Karen** — key Twin Cities immigrant/refugee communities

### Reading Level Adaptation

Three modes: **Simple** (5th grade), **Standard** (8th grade), **Detailed** (full detail with defined terms)

---

## Architecture

### Three-Stage Agentic Pipeline

```
User Input (any language)
    |
    v
+----------------------------------+
|  STAGE 1: INTAKE & EXTRACTION    |  <- E4B (Ollama, fine-tuned)
|  - Language detection            |
|  - Situation parsing             |
|  - Structured fact extraction    |
|  - Clarifying questions if needed|
|  Output: UserProfile JSON        |
+----------------+-----------------+
                 |
                 v
+----------------------------------+
|  STAGE 2: ELIGIBILITY ENGINE     |  <- 26B A4B MoE (Kaggle/Colab)
|                                  |     or E4B (Ollama, local mode)
|  Agentic loop:                   |
|  1. RAG search benefits KB       |
|  2. Function calls to APIs       |
|  3. Cross-reference programs     |
|  4. Identify overlaps/conflicts  |
|  5. Prioritize by impact/urgency |
|  Output: EligiblePrograms[]      |
+----------------+-----------------+
                 |
                 v
+----------------------------------+
|  STAGE 3: RESPONSE GENERATION    |  <- E4B (Ollama, fine-tuned)
|  - Plain language explanations   |
|  - Reading level adaptation      |
|  - Required documents list       |
|  - Application links & next steps|
|  - Source citations              |
|  - Translation (if needed)       |
|  Output: Personalized action plan|
+----------------------------------+
```

### Two-Model Split

| Model | Size (Q4_0) | Where | Role |
|-------|-------------|-------|------|
| **Gemma 4 E4B Instruct** | ~5 GB | Local via Ollama (RTX 2080 Ti) | Intake, output generation, local demo. Fine-tuned with Unsloth. |
| **Gemma 4 26B A4B MoE** | ~15.6 GB | Kaggle T4 / Colab A100 | Complex eligibility reasoning, multi-API orchestration. |
| **Gemma 4 31B Dense** | ~17.4 GB | Kaggle 2xT4 (dataset generation only) | Generate silver training data. Not in production pipeline. |

For the **local-only demo** (Ollama prize), E4B handles all three stages. For the **full-power mode**, Stage 2 routes to 26B MoE.

### Function Calling Tools (Gemma 4 Native)

| Tool | Data Source | Purpose |
|------|-----------|---------|
| `calculate_fpl_threshold` | HHS FPL tables (local JSON) | Determine poverty level % for income + household size |
| `search_benefits_kb` | ChromaDB + BM25 (local) | RAG search over federal + state + county programs |
| `check_program_eligibility` | NYC Screening API + local rules | Eligibility check given household data |
| `get_hud_income_limits` | HUD API | Area-specific income limits for housing assistance |
| `get_healthcare_options` | CMS Marketplace API | Medicaid/CHIP/marketplace eligibility |
| `get_unemployment_info` | CareerOneStop API | State-specific UI filing info |
| `get_county_programs` | Local KB | County-specific programs + CAP agencies |
| `get_document_requirements` | Local KB | Required documents per program + applicant profile |
| `cross_reference_programs` | Local logic | Identify overlaps, conflicts, application groupings |

### RAG Architecture

- **Embedding model**: `all-MiniLM-L6-v2` (80 MB, runs on CPU)
- **Vector store**: ChromaDB (lightweight, persistent, no server)
- **Hybrid retrieval**: Vector similarity + BM25 keyword matching (via `rank_bm25`). Government program names (SNAP, WIC, MFIP) need exact keyword matching.
- **Chunk strategy**: One chunk per program section (~512 tokens, 50-token overlap)
- **Jurisdiction filtering**: Every KB entry tagged with jurisdiction (federal, state:MN, county:ramsey, etc.). Retrieval filtered by user's location.

### Knowledge Base

| Source | Content | Access Method | Priority |
|--------|---------|--------------|----------|
| SAM.gov Assistance Listings | 2,200+ federal program descriptions + eligibility | API | P0 |
| DHS Combined Manual | MN cash/food eligibility rules (MFIP, SNAP, GA, MSA, EA, EGA) | Scrape | P0 |
| DHS Eligibility Policy Manual | MN health care eligibility (MA, MinnesotaCare) | Scrape | P0 |
| MN House Research publications | Plain-language program summaries (CCAP, MinnesotaCare, EGA, MHFA) | PDF download | P0 |
| County social services pages (5 counties) | County-specific programs, contacts, application links | Scrape | P0 |
| CCAP Policy Manual | Child care assistance eligibility | Scrape | P1 |
| LawHelp Minnesota | Plain-language legal explainers (EGA, GA, SNAP, housing) | Scrape | P1 |
| CAP agency program pages (3 agencies) | CAPRW, CAP-HC, CAP Agency programs per county | Scrape | P1 |
| MNsure income guidelines | Health coverage income thresholds | PDF | P0 |
| Energy Assistance guidelines (Commerce) | EAP/LIHEAP income thresholds and benefit amounts | Scrape | P1 |
| Open Eligibility Taxonomy | Service classification backbone | GitHub download | P1 |
| CareerForce / DEED pages | Dislocated Worker, CLIMB, UI info | Scrape | P1 |
| Bridge to Benefits | Screening logic reference (reverse-engineer) | Analyze | P2 |
| Ramsey County Open Data | 130+ datasets, Dislocated Worker data story | API | P2 |
| Combined Application Form (DHS-5223) | Question flow design reference | PDF | P2 |

---

## Fine-Tuning Strategy (Unsloth + QLoRA)

### Configuration

| Parameter | Value |
|-----------|-------|
| Base model | Gemma 4 E4B Instruct |
| Method | QLoRA (4-bit quantized base + LoRA adapters) |
| LoRA rank | 16 |
| Target modules | All linear layers |
| Learning rate | 2e-4, cosine schedule |
| Epochs | 3-5 |
| Batch size | 1 (gradient accumulation 4-8) |
| Training hardware | Kaggle T4 (16 GB) — ~4-8 hours per run |

### Training Data (~2,000-3,000 examples)

1. **Situation extraction** (~500 examples) — Natural language situation description -> UserProfile JSON
2. **Plain language generation** (~1,500 examples) — Government text -> plain-language rewrite at target reading level. Source: WikiAuto (CC BY-SA 3.0), Cochrane Simplification (CC BY 4.0), synthetic from 31B.
3. **Benefits Q&A** (~500 examples) — Situation + program info -> personalized eligibility explanation. Synthetic from 31B + DHS Manual content, human-reviewed.

### Dataset Construction Workflow

1. Scrape DHS Combined Manual, county pages, MN House Research PDFs
2. Use 31B on Kaggle 2xT4 to generate plain-language rewrites and synthetic Q&A pairs
3. Manually review/correct 100-200 gold examples
4. Train E4B with Unsloth on Kaggle T4
5. Export to GGUF format -> load into Ollama via `ollama create`

---

## Compute Strategy

| Task | Platform | Cost |
|------|----------|------|
| Daily dev, testing, prompt iteration | Local RTX 2080 Ti + Ollama | Free |
| Fine-tuning E4B (Unsloth) | Kaggle T4 (30 hr/week quota) | Free |
| 31B inference for dataset generation | Kaggle 2xT4 or Colab Pro A100 | Free or $10/mo |
| 26B MoE inference for evaluation | Kaggle T4 | Free |
| Live demo hosting | HuggingFace Spaces A10G GPU | ~$0.60/hr |
| Prompt prototyping | Google AI Studio (Gemini Pro) | Free with Pro account |

**Total estimated cost: $30-60** (Colab Pro one month + HF Spaces GPU during judging).

---

## UI Design (Gradio)

### Three-Panel Layout

**Left sidebar:**
- Extracted user profile (editable) — income, household size, county, employment status
- Reading level toggle (Simple / Standard / Detailed)
- Language selector (English, Spanish, Hmong, Somali, Karen)

**Center (main):**
- Chat interface with streaming responses
- Priority-grouped program recommendations
- Consolidated document checklist
- Application links grouped by portal (MNbenefits, MNsure, uimn.org, etc.)

**Bottom of each response:**
- Expandable "Sources & Reasoning" accordion showing retrieved KB chunks and eligibility logic
- Disclaimer: "This is an informational tool, not legal advice."

**Footer:**
- Privacy indicator: "Running locally via Ollama - your data never leaves this device"
- Last updated date

### Deployment

| Environment | Stack | Purpose |
|-------------|-------|---------|
| Local | Gradio -> Ollama API (localhost:11434) -> E4B | Live demo, Ollama prize, privacy |
| HuggingFace Spaces | Gradio -> E4B (GPU Space, A10G) | Public live demo for judges |
| Kaggle Notebook | Transformers -> 26B MoE | Full-power submission artifact |

---

## Available Datasets

### Text Simplification (for fine-tuning)

| Dataset | Size | License | Use |
|---------|------|---------|-----|
| WikiAuto | Hundreds of thousands of aligned pairs | CC BY-SA 3.0 | Plain language generation training |
| Cochrane Simplification | ~4,459 paragraph pairs | CC BY 4.0 | Medical/technical text simplification |
| OneStopEnglish | 189 texts x 3 reading levels | CC BY-SA 4.0 | Multi-level readability examples |

### Government / Legal

| Dataset | Size | License | Use |
|---------|------|---------|-----|
| StateCodes + LaborBench | 8.7 GB (all 50 states) | Public domain | State eligibility rules, unemployment law |
| SAM.gov Assistance Listings | 2,200+ programs | Public domain | Federal program directory for RAG |
| GSA BEARS eligibility rules | Small | Public domain | Structured eligibility criteria |
| 18F SNAP rules | Small | Public domain | SNAP eligibility as code |

### APIs

| API | Access | Use |
|-----|--------|-----|
| NYC Benefits Screening API | Free, token auth | Eligibility determination for 40+ programs |
| CMS Marketplace API | Free API key | Healthcare eligibility |
| CareerOneStop API | Free bearer token | Unemployment info by state |
| HUD Income Limits API | Free | Housing assistance thresholds |
| SAM.gov API | Free | Federal program data |
| Federal Register API | Free, no key | Current regulations |

### Competition Compliance

All datasets and APIs listed above are:
- Publicly available and accessible to all participants at no cost
- Licensed under OSI-approved or public domain licenses
- Compatible with the CC-BY 4.0 winner license requirement

**Excluded resources:**
- Newsela (NDA required) — DISQUALIFIED
- ASSET dataset (CC BY-NC) — non-commercial clause concern
- PolicyEngine code (AGPL-3.0) — copyleft conflicts with CC-BY 4.0 winner license. Use as reference only, not in submission.
- 211 data (registration-gated, proprietary) — competition compliance UNCERTAIN

---

## Minnesota-Specific Data

### State Programs Covered (15+)

**Health:** Medical Assistance (Medicaid), MinnesotaCare, MNsure marketplace
**Cash:** MFIP (TANF), General Assistance, MSA, Diversionary Work Program
**Food:** SNAP (MN uses generous 200% FPL BBCE threshold), MFAP (for noncitizens), WIC
**Emergency:** EA (families), EGA (individuals)
**Child Care:** CCAP (income-based with SMI tiers)
**Housing:** Housing Support, Bridging Benefits, Section 8 via Metro HRA, MHFA loans
**Energy:** EAP/LIHEAP ($200-$1,400 heating, $600 crisis), Weatherization
**Employment:** Unemployment Insurance, Dislocated Worker Program, CLIMB, SNAP E&T, CareerForce

### Key Organizational Context

Minnesota restructured in July 2024, creating DCYF which now administers SNAP, MFIP, CCAP, and EA (previously under DHS). This causes confusion for applicants — a key differentiator for our Navigator.

**Application portals:**
- **MNbenefits.mn.gov** — primary unified application (SNAP, MFIP, GA, MSA, EA, CCAP, Housing Support)
- **MNsure.org** — health coverage (MA, MinnesotaCare, marketplace plans)
- **uimn.org** — unemployment insurance
- **CareerForce** — dislocated worker, employment services
- **County/CAP offices** — energy assistance, Head Start, specialized programs

### County-Specific Differentiation

| Feature | Ramsey | Hennepin | Dakota | Scott | Carver |
|---------|--------|----------|--------|-------|--------|
| Open Data Portal | Yes (130+ datasets) | GIS + HS data | GIS via MN Geospatial | No portal | GIS via ArcGIS |
| Dislocated Worker | County-run (own app) | Via Hennepin-Carver WDB | Via CareerForce | Via CareerForce | Via Hennepin-Carver WDB |
| CAP Agency | CAPRW | CAP-HC | CAP Agency (SCD) | CAP Agency (SCD) | CAP Agency (SCD) |
| Multilingual Phone | Yes (5 langs, 24/7) | Yes | Standard hours | Standard hours | Standard hours |
| Special Programs | Dislocated Worker interest form | Hennepin Pathways, SNAP E&T | Aging/Disability | Mental Health case mgmt | Small county |

### Community Action Agencies

| Agency | Serves | Key Programs |
|--------|--------|-------------|
| CAPRW | Ramsey, Washington | Energy assistance, Head Start, car loans, VITA tax clinic, Section 8, SNAP application help |
| CAP-HC | Hennepin | Energy, water, rental assistance, vehicle repair, homebuyer services |
| CAP Agency | Scott, Carver, Dakota | 20+ programs, 50K people/year, energy assistance, Head Start, chore program for seniors |

---

## Competition Alignment

### Prize Tracks Targeted

| Track | Prize Pool | Strategy |
|-------|-----------|----------|
| **Main Track** | up to $50K | Lead with impact: 26M eligible Americans don't receive SNAP, $60B unclaimed. Show human cost of bureaucratic complexity. |
| **Digital Equity & Inclusivity** | $10K | Multilingual (Hmong, Somali, Spanish, Karen). Reading level adaptation. Designed for people the system currently fails. |
| **Safety & Trust** | $10K | Sources & Reasoning panel. Every claim cited. Transparent eligibility logic. Disclaimers. Never says "you qualify." |
| **Ollama** | $10K | Entire system runs locally via Ollama. No data leaves device. Privacy-first. |
| **Unsloth** | $10K | Fine-tuned E4B for plain language generation. Published weights and benchmarks. |

**Maximum prize ceiling: $130K** (Main 1st + Digital Equity + Safety & Trust + Ollama + Unsloth)

### Competitive Differentiators

1. **No existing tool** combines conversational AI + comprehensive program coverage + county-specific guidance + plain language
2. **DHS/DCYF transition confusion** — we handle a real-world navigational problem
3. **County-level specificity** — Ramsey's Dislocated Worker Program, CAPRW's car loan program
4. **Privacy-first architecture** — runs entirely locally, critical for people sharing sensitive financial/immigration info
5. **Five prize tracks from one coherent system** — not bolt-ons, one architecture serving all narratives

---

## Demo Strategy (Video — 3 min max)

**Narrative arc:**

- **0:00-0:30 — The problem.** Show a real government benefits website. Highlight the jargon, the maze, the 47-page PDF. "This is what a single mother facing eviction sees when she tries to find help."
- **0:30-1:30 — The solution.** Live demo: user types their situation, Navigator returns prioritized programs with plain-language explanations, documents, and application links. Show the Sources panel. Switch to Spanish — same quality.
- **1:30-2:15 — Technical depth.** Architecture diagram. Ollama terminal running locally. Function calling log. RAG retrieval. Unsloth fine-tuning results.
- **2:15-3:00 — Impact and vision.** "26 million Americans eligible for SNAP don't receive it. This navigator doesn't just simplify — it acts as an advocate that speaks your language, running entirely on your own device."

---

## Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Eligibility accuracy — hallucinated thresholds | HIGH | Never generate rules from weights. Always retrieve from KB + cite. Hard-code FPL tables. Prominent disclaimer. |
| Fine-tuning marginal improvement | MEDIUM | Prompt engineering first (Week 2). Fine-tuning is incremental. Still qualify for Unsloth prize via training process. |
| DHS/DCYF data staleness | MEDIUM | Timestamp all KB entries. "Last verified: April 2026" on responses. |
| E4B too weak for complex eligibility | MEDIUM | E4B for common cases, 26B MoE for complex. Demo uses tested scenarios. |
| Multilingual quality varies (Hmong/Somali/Karen) | MEDIUM | Test thoroughly. English/Spanish primary, others labeled "beta." |
| Live demo outage during judging | HIGH | Backup screen recording. HF Spaces auto-restart. Local Ollama fallback. |
| AGPL license conflict (PolicyEngine) | HIGH | Do NOT include PolicyEngine code. Reference only. Build own rule logic. |
| Scope creep | MEDIUM | Strict priorities: federal + MN state + 5 counties. Features have P0/P1/P2 tiers. |

---

## Timeline (6 Weeks, 40 hrs/week = 240 hrs)

### Week 1: Data Collection & Foundation (40 hrs)
- Scrape DHS Combined Manual, EPM, CCAP Manual (14 hrs)
- Scrape county pages (5 counties) + CAP agencies (6 hrs)
- Download SAM.gov federal programs via API (4 hrs)
- Download MN House Research PDFs, extract text (3 hrs)
- Set up Ollama + Gemma 4 E4B locally (2 hrs)
- Set up ChromaDB + embeddings pipeline, ingest data (6 hrs)
- Set up project structure (src/, data/) (3 hrs)
- Read Gradio docs, build hello-world chat (2 hrs)
- **Deliverable:** All raw data collected. ChromaDB populated. Ollama running.

### Week 2: RAG Pipeline & Core Agent (40 hrs)
- Build hybrid retrieval (ChromaDB + BM25) with jurisdiction filtering (8 hrs)
- Implement function calling tools (FPL calc, KB search, eligibility, county, docs) (10 hrs)
- Build intake extraction (system prompt + few-shot) (6 hrs)
- Build response generation (system prompt + output template) (6 hrs)
- Wire three-stage pipeline end-to-end (6 hrs)
- Test with 10 scenarios, iterate prompts (4 hrs)
- **Deliverable:** Working end-to-end pipeline. Type a situation, get benefits list.

### Week 3: Fine-Tuning & Multilingual (40 hrs)
- Build fine-tuning datasets (situation extraction, plain language, Q&A) (18 hrs)
- Run Unsloth fine-tuning on Kaggle T4 (4 hrs)
- Evaluate fine-tuned vs base model (4 hrs)
- Export to GGUF for Ollama (2 hrs)
- Test multilingual (Spanish, Hmong, Somali) (6 hrs)
- Add reading level adaptation + textstat checks (4 hrs)
- Iterate prompts based on results (2 hrs)
- **Deliverable:** Fine-tuned E4B in Ollama. Multilingual + reading levels working.

### Week 4: UI, Integration & Polish (40 hrs)
- Build Gradio UI (chat + profile card + settings) (12 hrs)
- Add Sources accordion, document checklist, application links (7 hrs)
- Integrate 26B MoE path for complex cases (6 hrs)
- Add county-specific logic and CAP programs (4 hrs)
- Edge case testing (20+ scenarios) (6 hrs)
- Add disclaimers, privacy footer, error handling (2 hrs)
- Bug fixes and prompt refinement (3 hrs)
- **Deliverable:** Polished, working application. All features integrated.

### Week 5: Deployment & Demo Prep (40 hrs)
- Deploy to HuggingFace Spaces (GPU) (4 hrs)
- Create Kaggle notebook (26B MoE demo) (6 hrs)
- Stress test live demo (4 hrs)
- Script video demo narrative (6 hrs)
- Record demo footage (6 hrs)
- Clean up code, add documentation (6 hrs)
- Prepare GitHub repo for public submission (4 hrs)
- Write draft Kaggle writeup (1,500 words) (4 hrs)
- **Deliverable:** Live demo deployed. Video footage recorded. Code repo public.

### Week 6: Submission (40 hrs)
- Edit video (3 min max) (10 hrs)
- Finalize Kaggle writeup (6 hrs)
- Final testing of live demo (4 hrs)
- Cover image and media gallery (3 hrs)
- Create backup demo (screen recording) (2 hrs)
- Final code cleanup and commit (4 hrs)
- Submit on Kaggle (2 hrs)
- Buffer for unexpected issues (9 hrs)
- **Deliverable:** Submitted.

---

## MVP vs Stretch

### Must Have (Weeks 1-4)
- Federal programs (~15-20) + MN state programs (15+) + 5 county programs
- Plain-language eligibility explanations with source citations
- Consolidated document checklist + grouped application links
- English language
- Runs via Ollama locally (E4B)
- Gradio chat interface with profile card

### Should Have (Weeks 3-4)
- Unsloth fine-tuned E4B (plain language + extraction)
- Spanish + Hmong multilingual support
- Three reading levels with toggle
- Sources & Reasoning accordion
- 26B MoE path for complex cases

### Stretch (Weeks 5-6)
- Somali + Karen language support
- Cross-program conflict detection and application grouping
- Personalized benefits action plan (structured output)
- Proactive follow-up ("Based on your situation, you should also check...")
- HuggingFace Spaces deployment with GPU

### Won't Have (Post-Competition)
- All 50 states deep coverage
- Real-time eligibility determination (vs. estimate)
- Integration with MNbenefits for direct application submission
- Mobile app (LiteRT/Cactus deployment)
- Ongoing data refresh pipeline

---

## Key Technical Notes

- `cuml.accel` is disabled in the project due to RAPIDS cu12 vs system CUDA 13.1 mismatch
- The notebook preloads both cu12 and cu13 shared libraries for TensorFlow + PyTorch simultaneously
- 31B weights already downloaded locally (Keras + Transformers formats) at `models/`
- Gemma 4 E4B supports audio input — could explore voice input as stretch goal
- Google AI Studio (Gemini Pro account) available for prompt prototyping before deploying to Gemma 4

## Mandatory Disclaimers (on every response)

- "This is an informational tool, not legal advice."
- "Eligibility determinations are unofficial estimates."
- "Always verify with the relevant agency before applying."
- "Program rules change — information last verified April 2026."
