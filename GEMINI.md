# NorthStar Navigator

## Project Overview
The "NorthStar Navigator" is a Python-based application built for the **Kaggle Gemma 4 Good Hackathon**. It aims to help users navigate government benefits programs (specifically in Minnesota) using plain language. The deadline for the competition is May 18, 2026.

The overarching goal is to use Gemma 4 models to address a real-world challenge. The competition targets a $100K Main Prize along with Special Technology tracks. This project aims for multiple prize targets, including the Main Track, Digital Equity, Safety & Trust, Ollama, and Unsloth tracks.

The application uses a 3-stage pipeline to process user input:
1. **Intake (`src/navigator/intake.py`)**: Extracts a user profile from the raw message using a local LLM to parse situations and ask clarifying questions.
2. **Eligibility (`src/navigator/eligibility.py`)**: Determines eligibility for various programs (focusing on ~15-20 federal, 15+ state, and specific Twin Cities metro county programs) using a RAG pipeline and predefined rules/function calling.
3. **Response Generation (`src/navigator/response.py`)**: Generates a plain-language response tailored to the user's reading level (Simple, Standard, Detailed) and language (English, Spanish, etc.), with rigorous citations and disclaimers.

The application leverages local Large Language Models (LLMs) via **Ollama** (specifically targeting the E4B size) to ensure user data remains private and secure, with fine-tuning implemented via **Unsloth** for the response generation stage. It features a UI built with **Gradio**.

## Architecture
The project architecture is divided into three main domains:
1. **RAG & Data Architecture**: Raw data is ingested into a ChromaDB vector store. A hybrid search (Vector embeddings via `sentence-transformers/all-MiniLM-L6-v2` + BM25 keyword search) is used to retrieve relevant program rules and eligibility criteria.
2. **Core Application**: A 3-stage pipeline orchestrated by `src/app.py` using components in `src/navigator/`.
3. **Training & Deployment**: Scripts for scraping data (DHS manuals, county pages, SAM.gov), preparing datasets (`.jsonl`), training the model (using Unsloth/Modal on Kaggle or Colab), and exporting GGUF artifacts for local Ollama consumption.

## Directory Structure
*   `data/`: Contains all data artifacts.
    *   `chroma_db/`: Local Chroma vector database.
    *   `fpl_tables/`: Federal Poverty Level tables.
    *   `programs/`: JSON files defining program rules.
    *   `raw/`: Raw scraped data from county pages and DHS manuals.
    *   `training/`: Datasets for model fine-tuning.
*   `deploy/`: Scripts for deploying to Modal.
*   `docs/`: Project documentation.
    *   `competition/`: Rules, overview, and Kaggle writeup materials.
    *   `ideas/`: Brainstormed competition ideas and plans.
    *   `research/`: Domain research reports.
    *   `superpowers/`: Design specs and implementation plans.
*   `scripts/`: Utility scripts for scraping (`scrape_dhs_manual.py`, `download_sam_gov.py`, etc.) and data ingestion (`ingest_all.py`).
*   `src/`: Application source code.
    *   `app.py`: Main Gradio application entry point.
    *   `navigator/`: Core application logic (Intake, Eligibility, RAG, Prompts, Tools, Readability).
*   `tests/`: `pytest` test suite (currently at 75 passing tests).
*   `training/`: Scripts and notebooks for Unsloth fine-tuning and GGUF export.

## Technology Stack
*   **Language**: Python 3.13+
*   **Environment Setup**: `uv` for package management, `direnv` for env vars.
*   **UI Framework**: Gradio 6.x
*   **LLM Integration**: Ollama (defaults to `gemma3:4b` in config until the Gemma 4 E4B model is available in GGUF)
*   **RAG Stack**: ChromaDB, Sentence-Transformers, Rank-BM25
*   **Data Processing**: Pandas, BeautifulSoup, Playwright
*   **Machine Learning/Training**: PyTorch, Unsloth (via Kaggle/Colab), Scikit-Learn
*   **Hardware Accel**: TensorFlow 2.21 (CUDA 12) + PyTorch (CUDA 13) + RAPIDS.

## Getting Started

### Prerequisites
1.  Python 3.13+
2.  `uv` (Python package manager)
3.  **Ollama**: Must be installed and running locally (`systemctl start ollama`). The application expects Ollama on `http://localhost:11434` and uses the `gemma3:4b` model by default (configurable in `src/navigator/config.py`).
    *   `ollama pull gemma3:4b`

### Installation
Install dependencies using `uv`. Important: The navigator dependencies are kept separate to avoid conflicts with the heavy RAPIDS/CUDA stack.
```bash
uv sync --extra navigator
```

### Running the Application
Launch the Gradio UI. Note: Always use `uv run` and set the required environment variable for ChromaDB:
```bash
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python uv run python src/app.py
```
The application will be available at `http://0.0.0.0:7860`.

### Running Tests
The project uses `pytest`. Run the test suite with:
```bash
uv run pytest tests/ -v
```

## Data Ingestion & Scraping Pipeline
To scrape external data and rebuild the RAG database:
```bash
# Scrape the manuals and pages
PYTHONPATH=src uv run python scripts/scrape_dhs_manual.py
PYTHONPATH=src uv run python scripts/scrape_county_pages.py
PYTHONPATH=src uv run python scripts/download_sam_gov.py  # Requires SAM_GOV_API_KEY

# Ingest into ChromaDB
PYTHONPATH=src PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python uv run python scripts/ingest_all.py
```

## Training
Fine-tuning scripts using Unsloth can be run in notebooks or via Modal for cloud-accelerated training.

### Local/Notebook (Kaggle/Colab)
```bash
python training/train_unsloth.py --dataset data/training/combined.jsonl
python training/export_gguf.py --model training/output/final
```

### Cloud (Modal)
The project includes a Modal deployment script for A100-accelerated fine-tuning.
```bash
modal run deploy/modal_finetune.py
```

## Troubleshooting & Known Issues
*   **ChromaDB Protocol Buffers**: If you see errors related to `well_known_types`, ensure `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` is set in your environment.
*   **Unsloth & TRL Compatibility**: Version `trl >= 0.12.0` introduced breaking changes. For Modal deployments, use `trl==0.11.4` and `transformers==4.46.3` for maximum stability with Unsloth's dynamic patching.
*   **UnslothGKDTrainer RuntimeError**: This `parameter without a default follows parameter with a default` error is caused by a signature mismatch in Unsloth's dynamic trainer generation. Installing `unsloth` directly from the GitHub repository (`unsloth @ git+https://github.com/unslothai/unsloth.git`) often resolves this as the team pushes hotfixes for dependency conflicts faster than PyPI releases.
*   **Missing Dependencies**: If running in a fresh container (like Modal), ensure `rich` is explicitly installed.

## Development Conventions
*   **Configuration**: Centralized in `src/navigator/config.py`. Uses `NAVIGATOR_DATA_DIR` environment variable to override data paths.
*   **Command Execution**: **Always prefix Python commands with `uv run`** to ensure the correct virtualenv is used.
*   **Schemas**: Uses `pydantic` for strict data modeling (`src/navigator/models.py`).
*   **Logging**: Standard Python `logging` is used throughout the application.
*   **Readability**: Responses are formatted to specific reading levels (Simple, Standard, Detailed) using the `textstat` library (`src/navigator/readability.py`).
*   **Safety/Disclaimers**: Mandatory disclaimers on every response — the app must *never* definitively say "you qualify", only assess potential eligibility.
## Tool Usage Guidelines
*   **Ignore .gitignore**: For this project ONLY, always ignore `.gitignore` when searching or listing files (e.g., use `no_ignore=true` for grep, `respect_git_ignore=false` for glob and list_directory).
