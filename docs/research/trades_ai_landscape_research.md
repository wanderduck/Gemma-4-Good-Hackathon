# AI-Assisted Vocational/Trade Education: Landscape Research

*Research compiled April 2026 for the Gemma 4 Good Hackathon*

---

## 1. The Skilled Trades Shortage

### Scale of the Problem
- The U.S. construction industry alone faces a shortage of **500,000+ skilled workers in 2026**, with **349,000 new construction workers needed this year alone**.
- Across just seven trade categories, **1.4 million jobs are projected to go unfilled by 2030** (Bring Back The Trades).
- The aggregate economic impact: **$325.6 billion in lost GDP nationally** and **$71.3 billion in lost tax revenue** per year.
- The housing industry labor shortage alone carries an economic impact of **$10.8 billion/year** (NAHB, June 2025).

### Workforce Demographics
- The median age for workers in construction and maintenance roles is **~41 years old**.
- For every experienced tradesperson retiring, **only 0.6 new workers enter the pipeline**.
- Baby Boomers are retiring faster than replacements are trained.

### Most In-Demand Trades
| Trade | Annual Openings (BLS) | Growth Rate | Median Salary Range |
|-------|----------------------|-------------|-------------------|
| Electricians | ~81,000 | 9% (well above avg) | $60,000-$80,000+ |
| Plumbers/Pipefitters/Steamfitters | ~44,000 | 4% | $60,000-$80,000+ |
| HVAC Technicians | Growing | 5% | $60,000-$80,000+ |
| Welders | Growing | Stable | $50,000-$75,000+ |
| Carpenters | Growing | Stable | $50,000-$65,000+ |

Top earners in all trades regularly clear six figures. Data center construction and clean energy infrastructure are driving additional demand beyond traditional construction.

### Gen Z Interest
A Resume Builder survey found that **42% of Gen Z** were either working in or training for a skilled trade, with top motivations being avoiding student debt and minimizing the risk of getting replaced by AI.

**Key takeaway for hackathon:** The problem is enormous, well-documented, and bipartisan. The shortage is getting worse, not better, making any tool that accelerates training or improves quality extremely high-impact.

---

## 2. Existing AI Tools in Trades Education

### Current Landscape -- What Exists

**SkillCat** -- The most prominent AI-for-trades platform. Offers virtual simulations that replicate key job skills with an AI instructor. Focuses on HVAC, construction, and telecom. Skills-based hiring platform that trains and places blue-collar workers. Does NOT do visual work-in-progress inspection.

**BuildOps** -- Field service management software for commercial contractors. Incorporates AI for scheduling, dispatching, and business operations. Not focused on education or visual inspection.

**IBM Smart Edge for Welding** (with AWS) -- Uses computer vision and acoustic analysis to monitor welding processes in real time. Detects defects like porosity in welding beads. This is an industrial/manufacturing tool, NOT an educational tool.

**MeltTools** -- AI-powered welding cameras that detect anomalies and track geometric features in multi-pass welding. Industrial quality control, not education.

**Multisensor AI Welding Trainer** (research prototype) -- Integrated HD cameras, RGB-D sensors, and machine learning to evaluate welding techniques. Trainees using this system showed notably improved welding accuracy and accelerated learning curves vs. traditional instruction or VR training. This is the closest existing analog to what we're building.

**Virtual Welding Simulators** -- Products like Lincoln Electric's VRTEX and Miller's AugmentedArc use VR/AR for welding practice. These simulate the welding process but don't assess real physical work.

**ChatGPT/LLM-based assistance** -- Electricians and other tradespeople are already using ChatGPT to find wiring diagrams, confirm code compliance, and diagnose issues. But these are text-only, not visual.

### Competitive Gap Analysis
| Capability | Exists Today? | Who? |
|-----------|--------------|------|
| AI text-based code lookup | Yes | ChatGPT, general LLMs |
| VR/AR welding simulation | Yes | Lincoln VRTEX, Miller AugmentedArc |
| Industrial weld defect detection | Yes | IBM, MeltTools, various CV systems |
| AI-powered trade job matching | Yes | SkillCat |
| Photo-based work assessment for students | **NO** | **Gap in market** |
| Multimodal AI that identifies code violations from photos | **NO** | **Gap in market** |
| Offline-capable AI visual inspector for job sites | **NO** | **Gap in market** |
| Cross-trade educational feedback tool | **NO** | **Gap in market** |

**Key takeaway:** There is NO existing product that lets a trade student photograph their work-in-progress and get AI feedback on quality, code violations, and safety issues. This is a clear gap.

---

## 3. Trade Codes and Standards

### Electrical
- **NEC (NFPA 70)** -- National Electrical Code, published by the National Fire Protection Association. Updated every 3 years (2023 edition current, 2026 edition publishing). First published 1897.
- **Access:** Available for free online reading at nfpa.org (requires registration). Older editions available on UpCodes. Full purchase is paid/proprietary. The 2017 edition is available as a free PDF from some government sources.
- **Key sections for AI training:** Box fill calculations (314.16), GFCI requirements, wire sizing, conduit fill, grounding.

### Plumbing
- **IPC** -- International Plumbing Code, published by the International Code Council (ICC).
- **UPC** -- Uniform Plumbing Code, published by IAPMO.
- **Access:** Both are proprietary/paid. Some jurisdictions publish adopted versions online. UpCodes has some versions available for free browsing.
- **Key areas:** Drain slope requirements, venting rules, trap specifications, fixture unit calculations.

### Welding
- **AWS D1.1** -- Structural Welding Code (bridges, buildings, structural steel). Published by American Welding Society.
- **ASME Section IX** -- Pressure vessels and nuclear components.
- **API 1104** -- Pipeline welding.
- **Access:** All proprietary/paid. AWS publishes 240+ codes, recommended practices, and guides. Individual standards cost $50-$300+.

### HVAC
- **IMC** -- International Mechanical Code (ICC).
- **ACCA Manual J/D/S** -- Load calculations, duct design, equipment selection.
- **EPA Section 608** -- Refrigerant handling certification.
- **Access:** Mix of proprietary and publicly available. EPA regulations are public.

### Carpentry/Framing
- **IRC** -- International Residential Code (ICC).
- **IBC** -- International Building Code (ICC).
- **APA guidelines** -- Engineered wood association standards.
- **Access:** Proprietary, but many jurisdictions publish adopted versions. APA has free technical resources.

### Implications for the AI Tool
- Most codes are **proprietary** -- we cannot embed full code text in the model.
- However, **general principles, common violations, and safety rules** are widely published in educational materials, trade textbooks, and free online resources.
- The AI should reference code sections (e.g., "NEC 314.16") but explain the principle rather than quoting proprietary text.
- Fine-tuning on publicly available trade education content, inspection checklists, and common violation lists is feasible.
- Jurisdictional variation is a real challenge -- codes differ by state/city.

---

## 4. Common Student Mistakes by Trade

### Electrical -- Most Common/Dangerous Errors
1. **Overstuffing electrical boxes** -- Violates NEC 314.16. Generates heat, causes unreliable connections.
2. **Missing or improper GFCIs** -- Required in wet locations (kitchens, bathrooms, outdoors).
3. **Improper wire terminations** -- Wrong wire for terminal, over-stripping insulation, causing arcing.
4. **Reverse polarity at receptacles** -- Hot and neutral wires reversed; serious shock hazard.
5. **Inadequate cable support** -- NM cable not supported within 12" of boxes or every 4.5 ft.
6. **Improper wire splicing** -- Splices outside junction boxes, no wire nuts, exposed conductors.
7. **Wrong wire gauge for circuit amperage** -- Undersized wires overheat and cause fires.
8. **Non-IC rated lights in contact with insulation** -- Fire hazard.

**Visually detectable?** Many of these ARE visually detectable from photos: box fill, cable support, exposed splices, GFCI presence, wire routing.

### Welding -- Most Common Defects (Beginner)
1. **Porosity** -- Gas bubbles trapped in weld. Caused by dirty surface, wrong electrode, insufficient shielding gas.
2. **Undercut** -- Groove melted into base metal at weld toe. Too high current, too fast travel speed.
3. **Lack of fusion** -- Weld metal doesn't bond to base metal. Low current, poor joint prep, wrong angle.
4. **Incomplete penetration** -- Weld doesn't reach root of joint. Insufficient heat input.
5. **Excessive spatter** -- Metal droplets around weld. Wrong settings, dirty material.
6. **Poor bead profile** -- Inconsistent width, height, or shape.
7. **Burn-through** -- Excessive heat melts through base metal.
8. **Cracks** -- Most serious defect. Hot cracks from cooling stress, cold cracks from hydrogen.

**Visually detectable?** Approximately 60% of welding defects are detectable via visual inspection. Porosity, undercut, spatter, burn-through, and bead profile are all excellent candidates for AI visual assessment.

### Plumbing -- Most Common Code Violations
1. **Wrong drain slope** -- Must be 1/4" per foot for pipes 2.5" and smaller. Over-slope (>1/2"/ft) causes solids to be left behind.
2. **Inadequate/missing venting** -- No vents or undersized vents cause siphoning of traps, sewer gas entry.
3. **S-traps instead of P-traps** -- S-traps don't allow for proper venting; code violation.
4. **Flat or horizontal venting below flood rim** -- Code violation, prevents proper air flow.
5. **Undersized vent pipes** -- IPC specifies minimum sizes based on fixtures served.
6. **Improper materials** -- Using wrong pipe material for application (e.g., wrong glue, incompatible materials).

**Visually detectable?** Drain slope is hard from a photo (needs reference points). But trap type, venting presence, material choices, and connection quality are visually assessable.

### HVAC -- Most Common Installation Errors
1. **Incorrect refrigerant charge** -- Overcharging increases pressure/causes failure; undercharging damages compressor. (NOT visually detectable from external photos.)
2. **Poorly sealed ductwork** -- Leaky joints cause up to 30% energy loss.
3. **Wrong duct sizing** -- Causes pressure imbalances, uneven airflow.
4. **Unnecessary bends in ductwork** -- Reduces airflow and efficiency.
5. **Wrong materials for ducts** -- Affects durability and air quality.
6. **Improper refrigerant line installation** -- In ductless systems especially.

**Visually detectable?** Ductwork sealing, routing, and materials are visually assessable. Refrigerant issues require gauges/instruments.

### Carpentry/Framing -- Most Common Errors
1. **Missing panel gaps** -- OSB/plywood needs 1/8" expansion gaps or it buckles. Most common APA inspector finding.
2. **Wrong nailing patterns** -- Over-nailing or under-nailing structural sheathing. UBC specifies 6" edge / 12" field.
3. **Improper boring/notching of studs** -- Reduces structural capacity. Must follow code limits.
4. **Missing fire blocking** -- Concealed spaces >10' need fire blocking. One of the most common rough-frame violations.
5. **Unsupported columns** -- Columns resting on floor without blocking beneath crush underlying joists.
6. **Unbolted mudsills** -- Must be anchored to foundation.

**Visually detectable?** Nearly all framing errors are highly visually detectable -- panel gaps, nailing patterns, fire blocking, column support.

### Priority Trades for Visual AI (by detectability)
1. **Welding** -- Highest visual signal. Well-studied in CV literature. Clear defect taxonomy.
2. **Electrical** -- Many violations visible (box fill, cable routing, GFCI, splices). Some require removing covers.
3. **Carpentry/Framing** -- Highly visual during rough framing stage.
4. **Plumbing** -- Moderately visual (trap types, venting, connections visible during rough-in).
5. **HVAC** -- Mixed (ductwork visible, but many issues are system-level, not visual).

---

## 5. How Trade Education Currently Works

### Three Main Pathways

**1. Union Apprenticeships (JATC model)**
- Run by Joint Apprenticeship Training Committees -- partnership of unions and employer associations.
- Typically 4-5 years (8,000-10,000 hours OJT + classroom).
- Earn while you learn -- apprentices get regular pay increases as skills progress.
- Benefits include healthcare, retirement, and other union benefits.
- Structured progression: apprentice -> journeyman -> master.
- Examples: IBEW (electricians), UA (plumbers/pipefitters), Iron Workers, Carpenters unions.

**2. Community College / Trade School Programs**
- Certificate or associate degree programs, typically 1-2 years.
- Local trade unions often partner with community colleges as affiliated education providers.
- More classroom-heavy than apprenticeships.
- Students may need to find their own on-the-job training after completion.

**3. Non-Union / Open-Shop Apprenticeships**
- Run by contractor associations (e.g., ABC -- Associated Builders and Contractors).
- Similar structure to union programs but without union membership.
- Growing in some regions.

### Critical Pain Points

**Instructor Shortage**
- The biggest bottleneck is NOT student interest -- it's finding qualified instructors.
- The education industry pays far less than working in the trades.
- Skilled professionals earning $80,000-$120,000+ won't take a pay cut to teach.
- Colorado trade schools report instructor shortages even as student demand surges.

**Abysmal Completion Rates**
- Overall apprenticeship completion rate: **below 35%** (U.S. DOL, 2021).
- Construction apprenticeship completion: **41%** (down from 65% one year prior).
- **60% of dropouts leave within the first year**.
- Approximately half of all apprenticeship contracts are not completed.

**Causes of Dropout:**
- Employment-related interpersonal difficulties
- Poor quality training / instructors reading from textbooks
- Math skills deficiency
- Lack of mentoring and on-the-job guidance
- Financial hardship, childcare, transportation issues
- Excessive reliance on online rather than face-to-face training

**Outdated Training Methods**
- "The building trades have trained the same way since the 1950s, but in today's world it's not fast enough."
- Need to train faster in shorter periods to get more qualified people on the job.
- Traditional model assumes extensive 1-on-1 mentoring that is increasingly unavailable.

**Awareness Gap**
- Many young people and guidance counselors don't know apprenticeship programs exist.
- Cultural bias toward 4-year college degrees.

**Key takeaway for hackathon:** The instructor shortage and poor completion rates create a perfect use case for AI-assisted learning. An AI tool that provides instant, expert-level feedback on work quality could partially compensate for the lack of experienced mentors, improve first-year retention, and accelerate skill development.

---

## 6. Multimodal AI for Visual Inspection -- State of the Art

### Welding Defect Detection (Most Mature Area)
- **Transfer learning with CNNs:** ResNet-18 achieves 92.7% accuracy; ResNet-50 achieves 96.1% on weld defect classification.
- **EfficientNetB2/ResNet50:** 97.3% and 98.7% accuracy respectively.
- **Multi-camera fusion (IR + RGB):** 2-branch CNN for Submerged Arc Welding achieves 97.9-100% accuracy across defect classes.
- **WeldVGG:** VGG-inspired model for weld defect classification from radiographic images with visual interpretability.

### Manufacturing Defect Detection (Broader)
- Vision systems achieve **95-100% defect detection accuracy** in controlled environments.
- Detection speed: **under 200 milliseconds** for assembly/soldering defects.
- **RF-DETR** (2025): State-of-the-art detection transformer with real-time speed for production lines.
- **SAM 3** (Meta, Nov 2025): Open-vocabulary segmentation using natural language prompts -- enables adapting to new defect types without retraining.

### Multimodal Fusion Approaches
Three integration levels documented in literature:
1. **Early fusion** -- Combines raw signals at input level.
2. **Intermediate fusion** -- Parallel subnetworks learn unique representations before merging (most favored in recent work).
3. **Late fusion** -- Combines output probabilities from individual networks.

### Key Research Papers and Resources
- "Deep learning approaches for weld defect detection: A comprehensive review" (ScienceDirect, 2025)
- "Machine Vision-Assisted Welding Defect Detection System with CNNs" (Springer, 2025)
- "AI-enabled defect detection in industrial products: A comprehensive survey" (ScienceDirect, 2025)
- "Enhanced Vision-Based Quality Inspection: A Multiview AI Framework" (MDPI Sensors, 2025)
- "A survey of deep learning for industrial visual anomaly detection" (Springer AI Review, 2025)
- GitHub: M-3LAB/awesome-industrial-anomaly-detection -- Curated paper list and datasets.

### Relevance to Our Approach
Our approach differs from industrial inspection in key ways:
- **We use a general-purpose multimodal LLM (Gemma 4)** rather than a task-specific CNN.
- This trades some accuracy for massive flexibility -- one model handles all trades, all defect types, and can explain its reasoning in natural language.
- Gemma 4's native vision capabilities (object detection, OCR, document parsing) are well-suited for understanding photos of work-in-progress.
- The model can be fine-tuned with Unsloth on trade-specific datasets to improve domain accuracy.
- The 128K context window allows passing reference images alongside the query image.

---

## 7. Edge/Offline Deployment Considerations

### The Job Site Reality
- Construction/trade work happens on job sites that frequently lack reliable internet.
- Students may be in basements, crawl spaces, attics, or outdoor locations.
- Cell coverage is unreliable in many construction zones (especially new construction where towers may not cover the area yet).
- Workers need responses in seconds, not minutes -- waiting for cloud inference is impractical.

### Gemma 4 Edge Models
| Model | Effective Params | Memory Footprint | Target Hardware |
|-------|-----------------|------------------|-----------------|
| E2B | 2.3B effective | <1.5 GB (2-bit/4-bit quantized) | Mobile phones, Raspberry Pi |
| E4B | 4.5B effective | ~2-3 GB (quantized) | Modern smartphones, tablets |

### Performance on Edge Hardware
- **Raspberry Pi 5 (CPU):** 133 prefill tokens/sec, 7.6 decode tokens/sec.
- **Qualcomm Dragonwing IQ8 (NPU):** Substantially higher throughput.
- **Modern Android phones:** Gemma 4 E2B runs comfortably with multimodal capabilities.

### Deployment Stack Options

**LiteRT-LM (Google AI Edge)**
- Production-ready, high-performance inference framework for LLMs on edge devices.
- Cross-platform: Android, iOS, Web, Desktop, IoT (Raspberry Pi).
- CLI available for Linux, macOS, Raspberry Pi.
- Directly aligned with the **LiteRT Special Technology Prize ($10,000)**.

**Ollama**
- Run Gemma 4 locally via Ollama on laptops/desktops.
- Aligned with the **Ollama Special Technology Prize ($10,000)**.
- Good for instructor stations or workshop computers.

**llama.cpp**
- C++ inference engine for resource-constrained hardware.
- Aligned with the **llama.cpp Special Technology Prize ($10,000)**.
- Excellent for custom edge devices.

**Cactus**
- Local-first mobile framework with intelligent model routing.
- Aligned with the **Cactus Special Technology Prize ($10,000)**.

### Recommended Architecture
```
[Student's Phone/Tablet]
    |
    v
[Gemma 4 E2B/E4B running locally via LiteRT-LM]
    |
    +--> Offline mode: Full inference on device
    |
    +--> Online mode: Optional sync to cloud for
         larger model (26B/31B) second opinion,
         progress tracking, instructor dashboard
```

### Key Constraints to Design For
1. **Model size:** E2B at <1.5 GB is the sweet spot for mobile.
2. **Image processing:** Photos must be resized/compressed before inference.
3. **Response time:** Target <5 seconds for feedback on a single image.
4. **Battery life:** Inference is compute-intensive; design for intermittent use, not continuous.
5. **Storage:** Pre-load reference materials and common code summaries on device.
6. **First-run experience:** Model download must happen on WiFi before going to job site.

---

## Strategic Alignment with Hackathon

### Competition Track Fit
| Track | Fit | Prize |
|-------|-----|-------|
| Main Track | Strong | Up to $50,000 |
| Future of Education | **Perfect** -- "multi-tool agents that adapt to the individual and empower the educator" | $10,000 |
| Digital Equity & Inclusion | Strong -- "close the AI skills gap" for underserved populations | $10,000 |
| LiteRT | Strong if using LiteRT-LM for edge deployment | $10,000 |
| Ollama | Strong if demo runs via Ollama | $10,000 |
| Unsloth | Strong if fine-tuning Gemma 4 on trade data | $10,000 |

### Differentiation Points
1. **No competitor exists** in the photo-based trade work assessment space.
2. **Massive, well-documented social problem** (trades shortage, $325B GDP loss).
3. **Directly addresses instructor shortage** -- the #1 pain point in trade education.
4. **Offline-first design** matches real-world job site conditions and hackathon criteria ("classroom with spotty internet").
5. **Multimodal is essential** -- this problem REQUIRES vision + language, playing to Gemma 4's strengths.
6. **Clear path to multiple prize tracks** -- can target Main + Education + Technology prizes simultaneously.

---

## Sources

### Skilled Trades Shortage
- [Bring Back The Trades -- 1.4 Million Jobs Data](https://bringbackthetrades.org/press-release/new-research-data-reveals-nearly-1-4-million-trades-jobs-25-to-be-open/)
- [Bring Back The Trades -- $325.6B GDP Impact](https://bringbackthetrades.org/press-release/closing-the-skilled-trades-gap-could-unlock-325-6-billion-in-gdp-nationwide/)
- [Trade Colleges Directory -- Skilled Trades Shortage](https://tradecolleges.org/blog/skilled-trades-outlook/skilled-trades-shortage-opportunity/)
- [Tidewater Tech -- Job Outlook 2025+](https://tidewatertechtrades.edu/blog/job-outlook-skilled-trades/)
- [Metaintro -- Salary Guide 2026](https://www.metaintro.com/blog/skilled-trades-salary-guide-2026-electrician-plumber-hvac-welder-carpenter-machinist)
- [Fortune -- AI Boom Fueling Trades Demand](https://fortune.com/2026/03/20/skilled-trade-demand-randstand-report-electricans-technicans-construction-workers-six-figure-salaries-data-center-boom/)

### AI Tools in Trades
- [AWS -- AI in Industrial Welding](https://aws.amazon.com/blogs/industries/artificial-intelligence-in-industrial-welding-produces-near-real-time-insights-through-virtually-100-sample-sizes/)
- [IBM -- AWS Partnership for Welding AI](https://www.ibm.com/blog/ibm-and-aws-partnering-to-transform-industrial-welding-with-ai-and-machine-learning/)
- [Wevolver -- AI-Powered Welding CV](https://www.wevolver.com/article/ai-powered-welding-how-computer-vision-solutions-drive-precision-and-efficiency-in-metal-manufacturing)
- [SkillCat](https://www.skillcatapp.com/post/introducing-skillcat-we-match-skilled-trade-workers-with-high-paying-jobs)
- [BuildOps -- AI Reshaping Trades](https://buildops.com/resources/how-ai-is-reshaping-the-trades/)

### Trade Codes and Standards
- [NFPA 70 -- NEC](https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70)
- [NEC on UpCodes](https://up.codes/code/nfpa-70-national-electrical-code-2023)
- [AWS Codes and Standards](https://www.aws.org/standards-and-publications/codes-and-standards/)
- [Wikipedia -- National Electrical Code](https://en.wikipedia.org/wiki/National_Electrical_Code)
- [ESAB -- Welding Codes and Standards](https://esab.com/us/nam_en/esab-university/articles/what-you-should-know-about-welding-codes-and-standards/)

### Common Mistakes
- [Tradesmance -- Electrical Code Violations](https://www.tradesmance.com/career-central/common-electrical-code-violations)
- [EC&M -- Top 10 Electrical Code Violations](https://www.ecmweb.com/national-electrical-code/article/21256591/the-top-10-most-commonly-cited-electrical-code-violations)
- [Family Handyman -- Electrical Violations](https://www.familyhandyman.com/article/electrical-code-violations/)
- [RapidDirect -- 16 Welding Defects](https://www.rapiddirect.com/blog/types-of-welding-defects/)
- [Fractory -- Welding Defects Guide](https://fractory.com/welding-defects-types-causes-prevention/)
- [Roger Wakefield -- Plumbing Code Violations](https://rogerwakefield.com/plumbing-code-violations-to-look-out-for/)
- [Family Handyman -- Plumbing Violations](https://www.familyhandyman.com/article/most-common-plumbing-code-violations/)
- [NARS HVAC School -- Common HVAC Mistakes](https://narshvacschool.com/common-hvac-mistakes-and-how-to-avoid-them/)
- [Fine Homebuilding -- Common Framing Errors](https://www.finehomebuilding.com/project-guides/framing/avoiding-common-framing-errors)
- [APA -- Common Framing Errors](https://www.apawood.org/common-framing-errors)
- [Family Handyman -- Framing Mistakes](https://www.familyhandyman.com/list/14-framing-mistakes-to-avoid-at-all-costs/)

### Trade Education Models
- [CBS Colorado -- Instructor Shortage](https://www.cbsnews.com/colorado/news/colorado-trade-schools-face-instructor-shortage-student-demand-increase/)
- [AIR -- Improving Apprenticeship Completion Rates](https://www.air.org/resource/brief/improving-apprenticeship-completion-rates)
- [Construction News -- Apprenticeship Dropout Rates](https://www.constructionnews.co.uk/sections/long-reads/opinion/apprenticeships-why-the-dropout-rate-is-so-high-and-how-we-can-reduce-it-11-02-2026/)
- [U.S. DOL -- Apprenticeship Statistics](https://www.dol.gov/agencies/eta/apprenticeship/about/statistics/2021)
- [Social Finance -- Apprenticeship Retention](https://socialfinance.org/insight/reaching-one-million-active-apprentices-starts-with-retention-and-investments-in-the-right-supports/)
- [United Association -- Apprenticeship](https://ua.org/career-paths/apprentice/)

### Visual Inspection AI
- [ScienceDirect -- Deep Learning for Weld Defect Detection Review](https://www.sciencedirect.com/science/article/abs/pii/S036083522500871X)
- [Springer -- Machine Vision Welding Defect Detection with CNNs](https://link.springer.com/article/10.1007/s12541-025-01281-y)
- [ScienceDirect -- AI-enabled Defect Detection Survey](https://www.sciencedirect.com/science/article/pii/S1474034625009607)
- [MDPI -- Multiview AI Framework for Defect Detection](https://www.mdpi.com/1424-8220/25/6/1703)
- [Voxel51 -- Visual AI in Manufacturing 2025](https://voxel51.com/blog/visual-ai-in-manufacturing-2025-landscape)
- [GitHub -- awesome-industrial-anomaly-detection](https://github.com/M-3LAB/awesome-industrial-anomaly-detection)

### Edge Deployment
- [Google Developers -- Gemma 4 Edge Deployment](https://developers.googleblog.com/bring-state-of-the-art-agentic-skills-to-the-edge-with-gemma-4/)
- [Google -- Deploy Gemma on Mobile](https://ai.google.dev/gemma/docs/integrations/mobile)
- [Edge AI Vision Alliance -- Gemma 4 on Edge Devices](https://www.edge-ai-vision.com/2026/04/google-pushes-multimodal-ai-further-onto-edge-devices-with-gemma-4/)
- [GitHub -- LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM)
- [Google Blog -- Gemma 4 Announcement](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)
- [Unsloth -- Gemma 4 Local Deployment](https://unsloth.ai/docs/models/gemma-4)
