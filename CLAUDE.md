# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kaggle "Gemma 4 Good Hackathon" competition entry. The goal is to build a solution using Gemma 4 models that addresses a real-world challenge. Deadline: May 18, 2026.

Deliverables: video demo (≤3 min), Kaggle writeup (≤1500 words), public code repo, live demo.

## Environment Setup

- **Python 3.13** managed with **uv** (lock file: `uv.lock`)
- Uses **direnv** — run `direnv allow` to set `LD_LIBRARY_PATH` for CUDA/cuDNN libs
- GPU stack: TensorFlow 2.21 (CUDA 12) + PyTorch (CUDA 13) + RAPIDS cuDF/cuML/cuGraph (CUDA 12)
- CUDA libs are preloaded via ctypes in the notebook's GPU cell (dual cu12/cu13 setup)
- Environment variables in `.env` (gitignored)

## Commands

```bash
uv sync                    # Install/sync dependencies
uv sync --extra navigator  # Install navigator-specific deps (chromadb, gradio, etc.)
uv add <package>           # Add a dependency
jupyter lab                # Launch JupyterLab
uv run pytest tests/ -v    # Run test suite (uv run required for correct env)
uv run python src/app.py   # Launch Gradio UI
```

**Important:** Always prefix Python/pytest commands with `uv run` to use the correct virtualenv.

## Project Status

- **Active idea: Plain Language Government Navigator** — benefits eligibility navigator for MN
  - Design spec: `docs/superpowers/specs/2026-04-05-plain-language-government-navigator-design.md`
  - Implementation plan: `docs/superpowers/plans/2026-04-05-plain-language-government-navigator.md`
  - Full plan: `docs/ideas/plans/plain_language_government_navigator.md`
  - Architecture: Three-stage pipeline (Intake → Eligibility → Response) with Gemma 4 E4B via Ollama
  - Prize targets: Main + Digital Equity + Safety & Trust + Ollama + Unsloth ($130K ceiling)

## Project Structure

- `src/navigator/` — Core Navigator application
  - `models.py` — Pydantic data models (UserProfile, Program, EligibilityResult)
  - `intake.py` — Stage 1: situation parsing and profile extraction
  - `eligibility.py` — Stage 2: rule-based + RAG eligibility engine
  - `response.py` — Stage 3: plain language response generation
  - `ollama_client.py` — Ollama API wrapper
  - `prompts.py` — System prompts for all pipeline stages
  - `readability.py` — Flesch-Kincaid reading level checking
  - `config.py` — Settings, paths, model configuration
  - `rag/` — RAG pipeline (ChromaDB, BM25, hybrid retrieval, ingestion)
  - `tools/` — Function calling tools (FPL calc, benefits search, county programs, docs)
- `src/app.py` — Gradio UI entry point
- `scripts/` — Data scraping and ingestion scripts
- `training/` — Unsloth fine-tuning and GGUF export
- `tests/` — Full test suite (pytest, `pythonpath = ["src"]` in pyproject.toml)
- `data/` — Scraped data, ChromaDB store, training datasets
- `models/` — Gemma 4 model weights (31B + E4B)
- `docs/competition/` — competition rules and overview
- `docs/ideas/` — brainstormed competition ideas and plans
- `docs/research/` — domain research reports from sub-agent research
- `docs/superpowers/` — design specs and implementation plans
- `gemma4_goodhackathon_main.ipynb` — primary working notebook
- `notebook_images/` — images referenced by notebooks

## Navigator Dependencies

Navigator deps are in `[project.optional-dependencies] navigator` to avoid conflicts with the heavy RAPIDS/CUDA stack. Install with `uv sync --extra navigator`.

## Competition Notes

- Prize tracks: Main ($100K), Impact ($50K across 5 areas), Special Technology ($50K across 5 tools — Cactus, LiteRT, llama.cpp, Ollama, Unsloth)
- Projects can win both Main Track and Special Technology prizes simultaneously
- NEC, AWS D1.1, IPC/UPC trade standards are copyrighted — use educational summaries and inspection checklists for RAG, not full standard text

## Key Technical Notes

- `cuml.accel` is disabled due to RAPIDS cu12 vs system CUDA 13.1 header mismatch; use cuML via direct imports instead
- The notebook preloads both cu12 and cu13 shared libraries to support TensorFlow and PyTorch simultaneously
- Plotting uses Plotly (not matplotlib for interactive charts)
- ChromaDB requires `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` env var (set in `tests/conftest.py`)
- ChromaDB 1.5.5 `EmbeddingFunction` is a Protocol, not an abstract base class — adapter needs `name()`, `get_config()`, `build_from_config()`
- Navigator implementation is in worktree `.claude/worktrees/navigator-implementation/` (branch: `worktree-navigator-implementation`)
