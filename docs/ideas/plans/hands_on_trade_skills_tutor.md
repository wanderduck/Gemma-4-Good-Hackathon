# Comprehensive Plan: Hands-On Trade Skills Tutor

## The Problem

The skilled trades are facing a workforce crisis. Over 500,000 construction workers are short in 2026, with 1.4 million trade jobs projected unfilled by 2030 — representing $325.6 billion in lost GDP annually. Electricians alone have ~81,000 annual openings (9% growth). For every tradesperson retiring, only 0.6 new workers enter the pipeline.

The training bottleneck compounds the shortage: apprenticeship completion rates are below 35% nationally, with 60% of dropouts leaving in year one. The #1 constraint is instructor shortage — qualified tradespeople earn too much in the field to take pay cuts to teach. Training methods haven't changed since the 1950s.

**No existing product lets trade students photograph their real work-in-progress and get AI feedback on quality, code violations, and safety.** Industrial weld inspection AI exists (IBM, MeltTools), VR simulators exist, but the "snap a photo, get expert feedback" gap is wide open.

---

## The Solution

A multimodal AI tutor powered by Gemma 4 that lets trade students (electricians, welders, plumbers, carpenters) photograph their work-in-progress and receive:

1. **Quality assessment** — is this weld/wiring/joint/framing up to standard?
2. **Defect identification** — specific issues (porosity, improper box fill, wrong fitting, panel gaps)
3. **Code violation detection** — references to NEC, AWS D1.1, IPC/UPC, IRC/IBC standards
4. **Safety hazard flagging** — PPE compliance, immediate danger identification
5. **Explanatory corrections** — why it's wrong, how to fix it, with reference to trade principles

Designed to run **offline-first** on a phone or cheap laptop, because trade students work on job sites without reliable internet.

---

## Target Trades (Ranked by Visual Assessability)

| Trade | Visual Signal | Key Standards | Common Student Mistakes |
|-------|--------------|---------------|------------------------|
| **Welding** | Highest (~60% defects visible) | AWS D1.1 (structural steel) | Porosity, undercut, cold lap, inconsistent bead, wrong travel speed |
| **Electrical** | High | NEC/NFPA 70 | Box fill violations, improper cable routing, missing GFCI, exposed splices |
| **Carpentry/Framing** | High | IRC/IBC | Panel gaps, wrong nailing patterns, missing fire blocking, misaligned studs |
| **Plumbing** | Moderate | IPC/UPC | Wrong fitting type, improper slope, missing cleanouts, bad solder joints |
| **HVAC** | Lowest (system-level) | IMC | Duct leaks, improper refrigerant lines — many issues not photo-assessable |

**Recommendation:** Start with welding and electrical — highest visual signal, best dataset availability, most dangerous mistakes.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                 Student Device                   │
│  (Phone / Laptop — Offline-First)               │
│                                                  │
│  ┌──────────┐    ┌──────────────────────────┐   │
│  │  Camera   │───▶│  Gemma 4 E4B / 12B       │   │
│  │  Input    │    │  (Local Inference)        │   │
│  └──────────┘    │                            │   │
│                   │  1. Image analysis         │   │
│                   │  2. Defect classification  │   │
│                   │  3. Code reference lookup  │   │
│                   │  4. Explanation generation │   │
│                   └──────────┬───────────────┘   │
│                              │                    │
│  ┌──────────────────────────▼───────────────┐   │
│  │  RAG Knowledge Base (Local)               │   │
│  │  - Trade code summaries & principles      │   │
│  │  - Common defect patterns + corrections   │   │
│  │  - Safety checklists                      │   │
│  └──────────────────────────────────────────┘   │
│                              │                    │
│                   ┌──────────▼───────────────┐   │
│                   │  Student-Facing UI        │   │
│                   │  - Annotated photo        │   │
│                   │  - Issue list + severity  │   │
│                   │  - "How to fix" guidance  │   │
│                   │  - Progress tracking      │   │
│                   └──────────────────────────┘   │
└──────────────────────┬──────────────────────────┘
                       │ (when connected)
                       ▼
              ┌────────────────────┐
              │  Instructor        │
              │  Dashboard (Cloud) │
              │  - Student progress│
              │  - Common errors   │
              │  - Batch review    │
              └────────────────────┘
```

### Key Technical Decisions

- **Model size:** Gemma 4 E4B for phone deployment (runs in <1.5 GB RAM), 12B or 31B for cloud/laptop with GPU
- **Deployment runtime:** LiteRT-LM (mobile), Ollama (laptop), or llama.cpp — each aligns with a $10K Special Technology Prize
- **RAG for codes:** Trade standards (NEC, AWS, IPC) are copyrighted. Use freely available educational summaries, inspection checklists, and code violation guides rather than full standard text. Reference section numbers without quoting
- **Multimodal pipeline:** Gemma 4's native vision capabilities handle image understanding; no separate vision model needed
- **Offline-first:** All inference and RAG retrieval happens locally. Cloud sync is optional for instructor dashboard

### Jurisdictional Note

Trade codes vary by jurisdiction (e.g., NEC adoption differs by state/county). The MVP should target the most common national standards and note where local amendments may apply.

---

## Available Datasets

### Welding (Strongest Coverage)

| Dataset | Size | Contents | License |
|---------|------|----------|---------|
| Intel Robotic Welding Multimodal (HF) | 4,000+ samples | Video, audio, sensor data, 5 post-weld images/weld, 12 defect categories | Intel Labs release |
| LoHi-WELD (GitHub) | 3,022 images | Real MAG weld bead photos (low+high res), 4 defect types | Research use |
| Welding Defect Object Detection (Kaggle) | Varies | Weld bead images with bounding box annotations | Open |
| Weld Quality Instance Segmentation (Kaggle) | Varies | Pixel-level defect segmentation | Open |
| TIG Aluminium 5083 (Kaggle) | Varies | TIG weld quality on Aluminium 5083 | Open |
| TIG Stainless Steel 304 (Kaggle) | Varies | TIG weld quality on SS304 | Open |
| GDXray+ Welds | 68 radiographs | X-ray weld inspection images with defect annotations | Research/educational only |

### Electrical (Gap — Needs Custom Data)

| Dataset | Size | Contents | License |
|---------|------|----------|---------|
| Electric Wires Image Segmentation (Kaggle) | Varies | Wire images with segmentation annotations | Open |
| PCB Defect Dataset (Kaggle) | Varies | PCB images with YOLO annotations — proxy for circuit inspection | Open |
| DsPCBSD+ (Nature) | 10,259 images | 20,276 defects across 9 categories | CC BY 4.0 |
| STEM-AI Electrical Engineering (HF) | Text | Electrical engineering educational content for RAG | Check HF |
| Circuit Breakers (Roboflow) | 40 images | Circuit breaker switch identification | Roboflow terms |

**Key gap:** No public dataset for residential/commercial electrical wiring quality or NEC code violations. Will need to create custom data or use PCB datasets for transfer learning.

### Construction/Carpentry

| Dataset | Size | Contents | License |
|---------|------|----------|---------|
| BD3 (GitHub) | 3,965 images | 6 building defect types (cracks, peeling, spalling, etc.) | Academic |
| SDNET2018 (Kaggle) | 56,096 images | Cracked/non-cracked concrete (0.06-25mm cracks) | Open academic |
| UAV Building Surface Defects (Nature) | 14,471 images | 6 structural types, 5 defect categories | CC BY 4.0 |

### Plumbing

| Dataset | Size | Contents | License |
|---------|------|----------|---------|
| Sewer-ML (AAU Denmark) | 1.3M images | Pipe defects from CCTV inspection, multi-label annotations | CC BY-NC-SA 4.0 |
| CCTV-Pipe (VideoPipe) | 575 videos (87 hrs) | 16 defect categories from real urban pipe systems | Check project |

**Key gap:** Datasets focus on sewer/infrastructure CCTV, not close-up plumbing joint/fitting quality.

### Safety/PPE (Cross-Trade)

| Dataset | Size | Contents | License |
|---------|------|----------|---------|
| SH17 (Kaggle/Zenodo) | 8,099 images | 75,994 instances across 17 PPE classes | CC BY-NC-SA 4.0 |
| Construction-PPE (Ultralytics) | Varies | 11 classes: helmets, vests, gloves, boots, goggles + missing counterparts | AGPL-3.0 (code) |

### Transfer Learning / General

| Dataset | Size | Contents | License |
|---------|------|----------|---------|
| MVTec AD (MVTec) | 5,000+ images | 15 object/texture categories with pixel-precise anomaly annotations | CC BY-NC-SA 4.0 |
| Severstal Steel Defects (Kaggle) | 18,074 images | 4 defect classes on steel sheets with pixel-level segmentation | Kaggle terms |
| NEU Surface Defects (Kaggle) | 1,800 images | 6 metal surface defect classes | Open academic |

---

## Competition Alignment

This project can target **multiple prize tracks simultaneously**:

| Track | Prize | Fit |
|-------|-------|-----|
| Main Track | Up to $50,000 | Strong — addresses a massive, real workforce crisis |
| Future of Education | $10,000 | Direct — this is an AI tutor for underserved learners |
| LiteRT | $10,000 | If deployed via LiteRT on mobile |
| Ollama | $10,000 | If deployed via Ollama on laptop |
| llama.cpp | $10,000 | If deployed via llama.cpp on constrained hardware |
| Unsloth | $10,000 | If fine-tuned using Unsloth |

**Maximum potential prize: $70,000+** (Main + Education + one Special Technology)

---

## Demo Strategy (Video)

The competition is judged primarily on video (70% of score is Impact/Vision + Storytelling). Demo plan:

1. **Open with the crisis** — statistics on the trades shortage, show empty classrooms, aging workforce
2. **Show the problem** — a student alone on a job site, no instructor available, unsure if their work is right
3. **The moment** — student takes a photo of their weld/wiring, gets instant expert-level feedback on their phone
4. **Walk through the feedback** — annotated image, defect identification, code reference, "how to fix" guidance
5. **The instructor view** — dashboard showing class-wide progress, common errors, targeted intervention
6. **Edge story** — show it working in airplane mode, on a cheap phone, on a construction site
7. **Close with impact** — "Every tradesperson who completes their apprenticeship helps close a $325B gap"

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Copyrighted trade standards | Can't distribute NEC/AWS text | Reference section numbers, use educational summaries and inspection checklists |
| Electrical dataset gap | No training data for wiring inspection | Use PCB datasets for transfer learning; create small custom dataset; rely on Gemma 4's general vision + RAG |
| Model accuracy on safety-critical feedback | Wrong advice could cause injury | Always include disclaimer; flag confidence level; never say "this is safe" — only flag issues |
| E4B model too small for nuanced assessment | Poor quality feedback on phone | Tiered deployment: E4B for initial triage, cloud fallback for complex assessments when connected |
| Jurisdictional code variation | NEC amendments differ by locality | MVP targets national standards; note "check local amendments" where relevant |

---

## MVP Scope (6-Week Hackathon)

### Must Have
- Photo input → defect/quality assessment for **welding** (best data availability)
- Annotated image output highlighting issues
- Natural language explanation of each issue with severity
- Code/standard references where applicable
- Runs offline via Ollama or llama.cpp on a laptop with GPU

### Should Have
- Second trade: **electrical** wiring assessment
- Safety/PPE check as a secondary feature
- Simple progress tracking (local history of submissions)

### Won't Have (Post-Competition)
- Full instructor dashboard
- All five trades
- Mobile phone deployment (E4B)
- Jurisdictional code customization
