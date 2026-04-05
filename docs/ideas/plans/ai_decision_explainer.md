# Comprehensive Plan: AI Decision Explainer

## The Problem

AI systems increasingly make consequential decisions about people's lives — loan approvals, hiring screens, medical risk scores. When denied a loan or rejected by an ATS, affected individuals receive little to no meaningful explanation. Existing XAI tools (SHAP, LIME, DiCE) produce technical outputs — waterfall plots, coefficient tables, feature importance charts — that are intelligible to data scientists but opaque to the people actually affected.

The regulatory pressure is real and intensifying:
- **EU AI Act** (August 2026 compliance deadline): Credit scoring, hiring, and medical diagnostics are classified "high-risk" — requiring transparency, human oversight, and conformity assessment
- **GDPR Article 22**: Right to "meaningful information about the logic involved" in automated decisions. CJEU confirmed in 2025 (Case C-203/22) that individuals are entitled to genuine explanation
- **US CFPB**: Creditors cannot use "black-box" underwriting and claim the tech is too complicated to explain. Must provide specific, accurate reasons for adverse actions (ECOA/Reg B)
- **NYC Local Law 144**: Annual bias audits required for automated hiring tools. Penalties: $500-$1,500/day
- **Colorado AI Act** (June 2026): Requires reasonable care to prevent algorithmic discrimination in hiring
- **Illinois AI Video Interview Act** (2026 amendment): Gives candidates recourse rights against AI discrimination

**The gap:** Every XAI tool stops at technical output. None translate those outputs into plain-language explanations a loan applicant, job candidate, or patient can understand. None combine attribution ("why this happened"), contrastive explanation ("why X instead of Y"), and recourse ("what to change") into a unified narrative adapted to the audience.

---

## The Solution

A tool that takes an AI model's decision, runs it through established XAI methods, and uses Gemma 4 to translate the results into human-readable explanations. For any consequential AI decision, it produces:

1. **Attribution** — what factors drove the decision, in plain language
2. **Contrastive explanation** — why this outcome instead of the alternative
3. **Algorithmic recourse** — specific, actionable, feasible steps to change the outcome
4. **Confidence indicators** — how certain the model is, where its limitations lie
5. **Audience adaptation** — different explanation depth for affected individuals vs. compliance officers vs. auditors

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                            │
│  Model (sklearn/XGBoost/etc.) + Input Data + Decision Output  │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    XAI ENGINE LAYER                            │
│                                                                │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐  │
│  │    SHAP      │  │    DiCE     │  │  Fairness Metrics    │  │
│  │  Feature     │  │  Diverse    │  │  (AIF360/Fairlearn)  │  │
│  │  Attribution │  │  Counter-   │  │  Optional bias       │  │
│  │              │  │  factuals   │  │  detection           │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬───────────┘  │
│         │                │                     │               │
│         └────────────────┼─────────────────────┘               │
│                          │                                     │
│              Structured XAI Output (JSON)                      │
│              - Top N feature attributions                      │
│              - K diverse counterfactuals                       │
│              - Fairness metrics (if applicable)                │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                GEMMA 4 TRANSLATION LAYER                      │
│                                                                │
│  Structured prompt containing:                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  - XAI engine output (JSON)                               │ │
│  │  - Domain context (lending / hiring / medical)            │ │
│  │  - Feature metadata (which are actionable, immutable,     │ │
│  │    protected)                                             │ │
│  │  - Audience level (individual / compliance / auditor)     │ │
│  │  - Feasibility constraints (what can realistically change)│ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  Gemma 4 31B Instruct generates:                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  1. Plain-language decision summary                       │ │
│  │  2. Key factors explanation (contrastive)                 │ │
│  │  3. Actionable recourse suggestions                       │ │
│  │  4. Confidence/uncertainty indicators                     │ │
│  │  5. Limitations and caveats                               │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Key Technical Decisions

- **XAI engine is the source of truth:** Gemma 4 translates, it does not generate explanations from scratch. This prevents hallucinated explanations. The XAI methods (SHAP, DiCE) provide the ground truth; the LLM provides the communication layer.
- **Feature metadata is critical:** Each feature must be annotated as actionable (income — yes), immutable (age — no), or protected (race — never suggest changing). This prevents harmful recourse suggestions.
- **Domain-specific prompting:** Lending explanations reference ECOA/FCRA. Hiring explanations reference anti-discrimination law. Medical explanations reference informed consent and shared decision-making.
- **Faithfulness guardrail:** The explanation must faithfully represent the XAI output — no embellishment, no omission of unfavorable factors. Include a structured verification step comparing the narrative against the raw XAI JSON.

---

## Target Domains

### Lending (Primary — Best Data, Clearest Regulations)

- **Common models:** Logistic regression (regulatory benchmark), XGBoost, Random Forest, Explainable Boosting Machines
- **Key features:** Credit score/history, income, debt-to-income ratio, employment history, checking account balance, loan amount, collateral
- **Protected classes (ECOA):** Race, color, religion, national origin, sex, marital status, age, public assistance receipt
- **Proxy discrimination risk:** Zip code and education level can serve as race proxies. Minneapolis Fed (2024) found that lender-reported reasons for mortgage denials don't adequately explain racial disparities
- **Recourse example:** "Your application would likely be approved if your outstanding debt were $5,000 lower or your credit history were 2 years longer"

### Hiring (Secondary — High Impact, Regulatory Momentum)

- **Current state:** 48% of hiring managers used AI for resume screening in 2024, projected 83% by end of 2025
- **Documented bias:** Stanford found AI resume screening gave older male candidates higher ratings than equally qualified female/young candidates. Brookings (2025) confirmed gender, racial, and intersectional bias in LLM-based resume retrieval
- **Key challenge:** Explaining why a candidate was ranked lower is legally and ethically fraught. Recourse is more complex ("get 2 more years of experience" vs. "change your name")
- **Regulatory pressure:** NYC Local Law 144, Illinois AI Video Interview Act, Colorado AI Act, California AI hiring regulations

### Medical Risk (Tertiary — Highest Stakes, Most Nuanced)

- **Common models:** Clinical risk scores (APACHE, SOFA, Framingham, ASCVD), gradient boosting, neural networks for sepsis/readmission prediction
- **Explanation audiences differ radically:** Clinicians validate against domain expertise; patients need to understand risk and next steps
- **Unique concern:** Over-trust leads to missed diagnoses; under-trust leads to treatment non-adherence. Trust calibration is critical
- **Key gap:** Most medical XAI targets clinicians. Patient-facing explanation of AI risk scores is underserved

---

## Available Datasets

### Lending (Excellent Coverage)

| Priority | Dataset | Size | Contents | License |
|----------|---------|------|----------|---------|
| 1 | German Credit (UCI) | 1,000 | 20 attributes, good/bad credit risk, cost matrix | CC BY 4.0 |
| 2 | Give Me Some Credit (Kaggle) | 150,000 | Income, debt ratio, delinquencies, revolving utilization | Kaggle open |
| 3 | Home Credit Default Risk (Kaggle) | 307,511 | 74 attributes, multiple relational tables | Kaggle competition |
| 4 | Default of Credit Card Clients — Taiwan (UCI) | 30,000 | 6 months payment history, binary default target | CC BY 4.0 |
| 5 | Financial Risk for Loan Approval (Kaggle) | Varies | Financial risk indicators | Kaggle open |
| 6 | imodels Credit Card (HF) | 30,000 | Tagged "interpretability" and "fairness" | Check HF |

### Hiring

| Priority | Dataset | Size | Contents | License |
|----------|---------|------|----------|---------|
| 1 | Recruitment Bias & Fairness AI (Kaggle) | Varies | Candidate profiles with demographics + hiring outcomes | Kaggle open |
| 2 | AI-Powered Resume Screening (Kaggle) | 1,000+ | Synthetic profiles with AI screening scores | Kaggle open |
| 3 | 70k+ Job Applicants (Kaggle) | 70,000+ | HR-relevant features | Kaggle open |
| 4 | Resume Screening Dataset (HF) | Varies | Resumes with category labels | Check HF |

### Medical

| Priority | Dataset | Size | Contents | License |
|----------|---------|------|----------|---------|
| 1 | Heart Disease — Cleveland (UCI) | 303 | 13 interpretable features, severity target | CC BY 4.0 |
| 2 | Pima Indians Diabetes (Kaggle) | 768 | 8 features, binary diabetes target | CC0 Public Domain |
| 3 | Cardiovascular Disease (Kaggle) | 70,000 | Lifestyle features + cardiovascular disease target | Kaggle open |
| 4 | HealthRisk-1500 (HF) | 1,500 | Medical risk labels | CC BY 4.0 |
| 5 | MIMIC-III (PhysioNet) | ~40,000 ICU patients | Full clinical records — requires CITI training + DUA | Credentialed access |
| 6 | Synthea (GitHub) | Unlimited synthetic | Generates realistic patient records (FHIR, CSV) | Apache 2.0 |

### Fairness Benchmarks (Cross-Domain)

| Priority | Dataset | Size | Contents | License |
|----------|---------|------|----------|---------|
| 1 | Folktables/ACS Income (GitHub/HF) | 1,664,500 | Modern Adult replacement (NeurIPS 2021), annual updates | Public domain |
| 2 | Adult/Census Income (UCI) | 48,842 | Most-used fairness benchmark — race, sex explicit | CC BY 4.0 |
| 3 | COMPAS Recidivism (ProPublica) | 6,170 | Canonical algorithmic bias case study | Open |

### XAI Training & Evaluation

| Priority | Dataset / Tool | Size | Contents | License |
|----------|----------------|------|----------|---------|
| 1 | e-SNLI (HF) | 569,033 | Human-written natural language explanations for NLI tasks | Open |
| 2 | CARLA (GitHub) | N/A | Benchmarks 11 counterfactual methods, bundled datasets | MIT |
| 3 | DiCE (GitHub) | N/A | Diverse counterfactual generation, feasibility constraints | MIT |
| 4 | AIF360 (GitHub) | N/A | 70+ fairness metrics, 10+ mitigation algorithms | Apache 2.0 |

---

## Existing Research to Build On

### LLMs for Explanation Generation (Directly Relevant)

This is an active research area (2024-2026) and validates the exact approach:

- **"A Three-Level Framework for LLM-Enhanced XAI" (2025, Information Systems Frontiers):** Proposes (1) technical XAI computation, (2) LLM translation to natural language, (3) audience adaptation. Validates the architecture above.
- **Renze (2024-2025):** Pilot user study found majority of participants favored LLM narrative explanations over technical XAI outputs — finding them easier to understand and more informative.
- **Nancy Project (EU-funded):** Demonstrates combining SHAP values with LLMs for "clear, contextual explanations, perfect for business stakeholders."
- **"LLMs for Explainable AI: A Comprehensive Survey" (2025, arXiv:2504.00125):** Surveys the field systematically.

### Algorithmic Recourse

- **Wachter et al. (2017):** Foundational paper — counterfactual explanations as optimization
- **DiCE (Mothilal et al., 2020):** Diverse counterfactuals — multiple paths to different outcome
- **FACE (Poyiadzi et al., 2020):** Feasible counterfactuals following realistic data paths
- **Ustun et al. (2019):** Actionable recourse with practical cost formalization
- **Open problem:** Only 21% of counterfactual methods have been user-tested. Robustness under model retraining is unsolved

### Trust Calibration

Research shows explanations can cause over-trust (user follows AI blindly) or under-trust (user ignores valid output). Design implications:
- Include confidence/uncertainty indicators
- State limitations explicitly
- Use neutral framing (inform, don't persuade)
- Provide model performance context ("This model correctly predicts 87% of the time")
- Differentiate between high-confidence and moderate-confidence factors

---

## Competition Alignment

| Track | Prize | Fit |
|-------|-------|-----|
| Main Track | Up to $50,000 | Strong — addresses regulatory urgency and real human impact |
| Safety & Trust | $10,000 | Direct — "Pioneer frameworks for transparency and reliability, ensuring AI remains grounded and explainable" |
| Ollama | $10,000 | If Gemma 4 translation runs locally via Ollama (privacy story) |

**Maximum potential prize: $70,000** (Main + Safety & Trust + one Special Technology)

---

## Demo Strategy (Video)

1. **Open with the denial** — someone checking their phone, seeing "Your loan application has been denied." No explanation. The feeling of helplessness.
2. **The regulatory context** — quick overlay: EU AI Act deadline August 2026, CFPB requirements, NYC Law 144. This is not hypothetical.
3. **Run the tool** — feed the same loan decision into the AI Decision Explainer. Show the three-layer output:
   - **For the applicant:** "Your application was denied primarily because your debt-to-income ratio (42%) exceeds the typical approval threshold. To improve your chances, reducing your outstanding debt by approximately $8,000 would bring your ratio to 35%."
   - **For the compliance officer:** Detailed factor breakdown with SHAP values, protected class impact analysis, regulatory citation
   - **For the auditor:** Full technical report with fairness metrics, counterfactual analysis, model performance context
4. **Switch domains** — quick cut to a hiring decision explanation, then a medical risk score. Same tool, three domains.
5. **The privacy angle** — show it running entirely locally via Ollama. "Your most sensitive decisions, explained without leaving your device."
6. **Close with scale** — "Every consequential AI decision deserves a human explanation."

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hallucinated explanations | LLM invents factors not in XAI output | Structured verification: compare narrative against raw XAI JSON before presenting. Gemma 4 translates, never generates from scratch |
| Harmful recourse suggestions | "Change your race" or infeasible actions | Feature metadata classifies each attribute as actionable/immutable/protected. DiCE feasibility constraints enforce realistic suggestions |
| Over-trust in explanations | Users treat explanation as legal advice | Disclaimers, confidence indicators, explicit limitations. "This is an informational tool, not legal or financial advice" |
| Faithfulness drift | Explanation diverges from technical truth | Automated faithfulness check: extract claims from narrative, verify each maps to XAI output |
| Model-specific limitations | Tool only works with certain model types | Start with sklearn/XGBoost (SHAP supports natively). Expand to neural nets via Captum |

---

## MVP Scope (6-Week Hackathon)

### Must Have
- **Lending domain** fully working end-to-end
- Train a model on German Credit or Give Me Some Credit dataset
- SHAP feature attribution → Gemma 4 plain-language explanation
- DiCE counterfactual generation → Gemma 4 recourse narrative
- Three audience levels (individual / compliance / auditor)
- Confidence indicators and limitations disclosure
- Streamlit or Gradio web UI for demo

### Should Have
- Second domain: **medical risk** (Heart Disease dataset — small, clean, interpretable)
- Fairness metrics integration (AIF360 or Fairlearn)
- Side-by-side comparison: raw SHAP plot vs. Gemma 4 narrative (powerful demo visual)

### Won't Have (Post-Competition)
- Hiring domain (complex bias/legal issues)
- Arbitrary model ingestion (start with pre-trained models you control)
- Local Ollama deployment (use cloud Gemma 4 for MVP reliability)
- Fine-tuning Gemma 4 on e-SNLI for explanation quality (prompt engineering first)
