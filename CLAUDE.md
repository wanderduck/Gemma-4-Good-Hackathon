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
uv add <package>           # Add a dependency
jupyter lab                # Launch JupyterLab
```

## Project Status

- Concept phase — two candidate ideas under consideration (see `docs/ideas/plans/`)
  - **Hands-On Trade Skills Tutor** — `docs/ideas/plans/hands_on_trade_skills_tutor.md`
  - **AI Decision Explainer** — `docs/ideas/plans/ai_decision_explainer.md`

## Project Structure

- `gemma4_goodhackathon_main.ipynb` — primary working notebook
- `models/` — Gemma 4 31B instruct weights already downloaded (Keras + Transformers formats)
- `docs/competition/` — competition rules and overview
- `docs/ideas/` — brainstormed competition ideas and plans
- `docs/research/` — domain research reports from sub-agent research
- `src/` — Python modules (currently empty)
- `data/` — datasets (currently empty)
- `notebook_images/` — images referenced by notebooks

## Competition Notes

- Prize tracks: Main ($100K), Impact ($50K across 5 areas), Special Technology ($50K across 5 tools — Cactus, LiteRT, llama.cpp, Ollama, Unsloth)
- Projects can win both Main Track and Special Technology prizes simultaneously
- NEC, AWS D1.1, IPC/UPC trade standards are copyrighted — use educational summaries and inspection checklists for RAG, not full standard text

## Key Technical Notes

- `cuml.accel` is disabled due to RAPIDS cu12 vs system CUDA 13.1 header mismatch; use cuML via direct imports instead
- The notebook preloads both cu12 and cu13 shared libraries to support TensorFlow and PyTorch simultaneously
- Plotting uses Plotly (not matplotlib for interactive charts)
