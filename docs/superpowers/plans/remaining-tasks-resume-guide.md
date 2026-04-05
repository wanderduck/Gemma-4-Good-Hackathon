# Navigator Implementation — Resume Guide

**Purpose:** If the IDE crashes or context is lost, use this file to resume implementation from where we left off. Give this file to a new Claude session along with the full implementation plan.

**Full plan:** `docs/superpowers/plans/2026-04-05-plain-language-government-navigator.md`
**Design spec:** `docs/superpowers/specs/2026-04-05-plain-language-government-navigator-design.md`
**Worktree:** `.claude/worktrees/navigator-implementation/` (branch: `worktree-navigator-implementation`)

---

## All Tasks Complete (1-19)

| # | Task | Key Files Created | Tests |
|---|------|-------------------|-------|
| 1 | Project Scaffolding & Dependencies | `pyproject.toml`, `src/navigator/__init__.py`, `config.py`, `tests/conftest.py`, `src/app.py` stub | 0 |
| 2 | Data Models | `src/navigator/models.py`, `tests/test_models.py` | 7 |
| 3 | FPL Calculator Tool | `src/navigator/tools/fpl.py`, `data/fpl_tables/fpl_2026.json`, `tests/test_fpl.py` | 9 |
| 4 | Ollama Client Wrapper | `src/navigator/ollama_client.py`, `tests/test_ollama_client.py` | 5 |
| 5 | System Prompts | `src/navigator/prompts.py` | 0 |
| 6 | RAG — Embeddings & ChromaDB Store | `src/navigator/rag/embeddings.py`, `src/navigator/rag/store.py`, `tests/test_embeddings.py`, `tests/test_store.py` | 8 |
| 7 | RAG — BM25 & Hybrid Retrieval | `src/navigator/rag/bm25.py`, `src/navigator/rag/retrieval.py`, `tests/test_bm25.py`, `tests/test_retrieval.py` | 8 |
| 8 | RAG — Document Ingestion Pipeline | `src/navigator/rag/ingest.py`, `tests/test_ingest.py` | 4 |
| 9 | Readability Checker | `src/navigator/readability.py`, `tests/test_readability.py` | 6 |
| 10 | Stage 1 — Intake & Extraction | `src/navigator/intake.py`, `tests/test_intake.py` | 5 |
| 11 | Benefits Search Tool | `src/navigator/tools/benefits_search.py`, `tests/test_benefits_search.py` | 3 |
| 12 | County Programs & Document Requirements | `src/navigator/tools/county_programs.py`, `src/navigator/tools/document_requirements.py`, `tests/test_county_programs.py`, `tests/test_document_requirements.py` | 9 |
| 13 | Stage 2 — Eligibility Engine | `src/navigator/eligibility.py`, `tests/test_eligibility_engine.py` | 8 |
| 14 | Stage 3 — Response Generation | `src/navigator/response.py`, `tests/test_response.py` | 3 |
| 15 | End-to-End Integration Test | `tests/test_integration.py` | 4 |
| 16 | Gradio UI | `src/app.py` (full rewrite) | 0 (manual) |
| 17 | Data Scraping Scripts | `scripts/scrape_dhs_manual.py`, `scripts/scrape_county_pages.py`, `scripts/download_sam_gov.py`, `scripts/ingest_all.py` | 0 |
| 18 | Unsloth Fine-Tuning Script | `training/train_unsloth.py`, `training/export_gguf.py` | 0 |
| 19 | Update CLAUDE.md | `CLAUDE.md` | 0 |

**Total tests: 75 (all passing)**

**Implementation complete.** The full Navigator pipeline is built: data models, FPL calculator, Ollama client, system prompts, full RAG pipeline (embeddings, ChromaDB, BM25, hybrid retrieval, ingestion), readability checker, intake processor, benefits search tool, county programs (5 counties), document requirements, eligibility engine (10 programs + county), response generator, integration tests, Gradio UI, scraping script stubs, and Unsloth fine-tuning scripts.

**Known issues:**
- ChromaDB requires `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` env var (set in conftest.py)
- Navigator deps are in `[project.optional-dependencies]` — install with `uv sync --extra navigator`
- Gradio UI adapted for Gradio 6.x API (examples as lists-of-lists, theme moved to launch())
- Scraping scripts (Task 17) are stubs — user implements the actual scraping logic
- Training scripts (Task 18) require unsloth/trl/transformers/datasets installed separately (Kaggle/Colab only)
