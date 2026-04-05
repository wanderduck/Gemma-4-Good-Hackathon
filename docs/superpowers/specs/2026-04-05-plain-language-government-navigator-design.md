# Design Spec: Plain Language Government Navigator

**Date:** 2026-04-05
**Competition:** Gemma 4 Good Hackathon (Kaggle)
**Deadline:** May 18, 2026
**Prize Tracks:** Main ($50K), Digital Equity ($10K), Safety & Trust ($10K), Ollama ($10K), Unsloth ($10K)

---

## 1. Overview

A conversational AI benefits navigator that takes a plain-language description of someone's situation and returns personalized, prioritized eligibility guidance for federal, Minnesota state, and Twin Cities metro county programs — with plain-language explanations, document checklists, and application links. Multilingual. Runs locally via Ollama for privacy.

## 2. Scope

**Geographic:** US federal programs + Minnesota state + 5 Twin Cities metro counties (Ramsey, Hennepin, Dakota, Scott, Carver)
**Languages:** English (primary), Spanish (primary), Hmong/Somali/Karen (secondary/beta)
**Programs:** ~15-20 federal + 15+ state + county-specific programs and CAP agencies
**Reading levels:** Simple (5th grade), Standard (8th grade), Detailed

## 3. Architecture

Three-stage agentic pipeline:
1. **Intake & Extraction** (E4B via Ollama) — parse situation, extract structured profile, ask clarifying questions
2. **Eligibility Engine** (26B A4B MoE or E4B) — RAG search + function calling + cross-referencing + prioritization
3. **Response Generation** (E4B via Ollama, fine-tuned) — plain language output with citations, documents, links

Two-model split: E4B (5 GB, local Ollama) for intake/output + 26B MoE (15.6 GB, Kaggle/Colab) for complex reasoning.

RAG: ChromaDB + BM25 hybrid retrieval with jurisdiction filtering. Embedding: all-MiniLM-L6-v2 on CPU.

Function calling: 9 tools (FPL calculator, benefits KB search, program eligibility, HUD income limits, healthcare options, unemployment info, county programs, document requirements, cross-reference).

## 4. Model Strategy

- **E4B Instruct Q4_0** — local inference via Ollama, fine-tuned with Unsloth (QLoRA, rank 16, ~2,500 examples)
- **26B A4B MoE Q4_0** — complex eligibility reasoning on Kaggle T4
- **31B Dense** — dataset generation only (Kaggle 2xT4)
- Fine-tuning targets: situation extraction (500 ex), plain language generation (1,500 ex), benefits Q&A (500 ex)

## 5. Data Sources

**APIs:** SAM.gov, NYC Benefits Screening, CMS Marketplace, CareerOneStop, HUD, Federal Register
**Scrape:** DHS Combined Manual, DHS EPM, CCAP Manual, county pages (5), CAP agencies (3), MN House Research, LawHelp MN
**Datasets:** WikiAuto (CC BY-SA 3.0), Cochrane Simplification (CC BY 4.0), StateCodes/LaborBench (public domain)
**All sources are publicly available, free, and competition-compliant.**

## 6. UI

Gradio three-panel layout: profile sidebar (editable) + chat center + sources accordion. Reading level toggle, language selector. Privacy footer. Deployed on HF Spaces (GPU) + local Ollama.

## 7. Timeline

6 weeks, 40 hrs/week (240 hrs total):
- Week 1: Data collection, ChromaDB, Ollama setup
- Week 2: RAG pipeline, function calling, end-to-end agent
- Week 3: Fine-tuning (Unsloth), multilingual, reading levels
- Week 4: Gradio UI, 26B integration, county logic, testing
- Week 5: Deployment, video prep, code cleanup, writeup draft
- Week 6: Video edit, writeup finalize, submit

## 8. Risks

- Eligibility accuracy: mitigated by RAG-only (never generate from weights), hard-coded FPL, mandatory disclaimers
- AGPL license conflict: PolicyEngine as reference only, not in codebase
- E4B reasoning limits: tiered to 26B MoE for complex cases
- Multilingual quality variance: English/Spanish primary, others labeled beta
- Scope creep: strict MVP/should-have/stretch tiers

## 9. Key Decisions

- Minnesota-only (not multi-state) for depth over breadth
- Five metro counties for county-level differentiation
- E4B as primary model (fine-tuned, local) — not 31B (too large for local)
- Hybrid RAG (vector + keyword) — government program names need exact match
- Gradio over Streamlit — better chat component, HF Spaces deployment, streaming
- Unsloth fine-tuning on plain language (not eligibility rules — those stay in RAG)
- Mandatory disclaimers on every response — never say "you qualify"

## 10. Success Criteria

- User can describe their situation in plain language and receive accurate, personalized benefits guidance
- At least 15 federal + 15 state + county-specific programs covered
- English and Spanish working with correct eligibility information
- System runs entirely locally via Ollama with no data leaving the device
- Sources cited for every eligibility claim
- Fine-tuned model shows measurable improvement in plain language output quality
- Live demo stable on HuggingFace Spaces
- Video tells a compelling story in under 3 minutes

## References

- Full plan: `docs/ideas/plans/plain_language_government_navigator.md`
- Federal data research: `docs/research/plain_language_gov_navigator_research.md`
- Minnesota deep dive: `docs/research/minnesota_benefits_deep_dive.md`
- Competition overview: `docs/competition/competition_overview.md`
- Competition rules: `docs/competition/competition_rules.md`
- Model card: `models/gemma4_model_card.md`
