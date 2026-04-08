# Kaggle Competition: Gemma 4 Good Hackathon

# Overview
[insert personal goal and overview for competition here once decided upon]

# File Structure

This section outlines the architecture and data flows of the project across three key domains: RAG & Data Architecture, Core Application Architecture, and Training, Scripts & Deployment.

### 1. RAG & Data Architecture
This diagram outlines how raw data, parsed programs, and Federal Poverty Level (FPL) tables flow into the RAG pipeline (`src/navigator/rag/`) and are exposed via tool endpoints.

```mermaid
flowchart TD
    subgraph Data ["📁 data/"]
        ChromaDB[("chroma_db/<br>chroma.sqlite3")]
        Programs[/"programs/*.json"/]
        FPL[/"fpl_tables/fpl_2026.json"/]
        Raw[/"raw/..."/]
    end

    subgraph RAG ["📁 src/navigator/rag/"]
        Store["store.py<br>(Chroma Vector Store)"]
        BM25["bm25.py<br>(Keyword Search)"]
        Embeddings["embeddings.py<br>(Embedding Model)"]
        Retrieval["retrieval.py<br>(Hybrid Search)"]
        Ingest["ingest.py<br>(Data Loading)"]
    end

    subgraph Tools ["📁 src/navigator/tools/"]
        BenefitsSearch["benefits_search.py"]
    end

    Ingest -->|Reads| Programs
    Ingest -->|Reads| Raw
    Ingest -->|Writes| ChromaDB
    
    Store -->|Reads/Writes| ChromaDB
    Store -->|Uses| Embeddings
    
    Retrieval -->|Uses| Store
    Retrieval -->|Uses| BM25
    
    BenefitsSearch -->|Uses| Retrieval
    BenefitsSearch -->|Reads| FPL
```

### 2. Core Application Architecture
This diagram maps `src/app.py` and the `src/navigator/` package, highlighting the 3-stage pipeline used to process user input.

```mermaid
flowchart TD
    %% File System Structure using Subgraphs
    subgraph src ["📁 src/"]
        App["app.py<br/>(Gradio UI & Orchestrator)"]
        
        subgraph navigator ["📁 navigator/"]
            subgraph pipeline ["🔄 Pipeline Stages"]
                Intake["intake.py<br/>(Stage 1: IntakeProcessor)"]
                Eligibility["eligibility.py<br/>(Stage 2: EligibilityEngine)"]
                ResponseGen["response.py<br/>(Stage 3: ResponseGenerator)"]
            end
            
            subgraph shared ["⚙️ Shared Infrastructure"]
                Models["models.py<br/>(Pydantic Schemas)"]
                Ollama["ollama_client.py<br/>(LLM Wrapper)"]
                Prompts["prompts.py<br/>(System Prompts)"]
                Config["config.py<br/>(Settings & Constants)"]
                Readability["readability.py<br/>(Readability Utils)"]
            end
            
            Tools["📁 tools/<br/>(benefits_search, fpl, etc.)"]
        end
    end

    %% Pipeline Orchestration / Data Flow (Solid Blue lines)
    App == "1. raw message" ==> Intake
    Intake == "2. UserProfile" ==> App
    App == "3. UserProfile" ==> Eligibility
    Eligibility == "4. BenefitsResponse" ==> App
    App == "5. BenefitsResponse" ==> ResponseGen
    ResponseGen == "6. Plain-language text" ==> App

    %% Component Dependencies (Dotted lines)
    App -. "Injects" .-> Ollama
    App -. "Imports" .-> Prompts

    Intake -. "Uses" .-> Ollama
    Intake -. "Uses" .-> Prompts
    Intake -. "Instantiates" .-> Models

    Eligibility -. "Uses" .-> Tools
    Eligibility -. "Instantiates" .-> Models

    ResponseGen -. "Uses" .-> Ollama
    ResponseGen -. "Uses" .-> Prompts
    ResponseGen -. "Reads" .-> Config
    ResponseGen -. "Uses" .-> Models

    Ollama -. "Reads URLs/Models" .-> Config
    Readability -. "Reads thresholds" .-> Config
    Readability -. "Uses" .-> Models

    style App fill:#f9f,stroke:#333,stroke-width:2px
    style Intake fill:#bbf,stroke:#333
    style Eligibility fill:#bbf,stroke:#333
    style ResponseGen fill:#bbf,stroke:#333
```

### 3. Training, Scripts, and Deployment
This maps out the project's outer directories: scraping the initial dataset, merging `.jsonl` files for fine-tuning, and handling deployment artifacts.

```mermaid
graph TD
    %% Define Styles
    classDef script fill:#f9d0c4,stroke:#333,stroke-width:1px;
    classDef data fill:#d4e6f1,stroke:#333,stroke-width:1px;
    classDef deploy fill:#d5f5e3,stroke:#333,stroke-width:1px;
    classDef train fill:#fcf3cf,stroke:#333,stroke-width:1px;
    classDef notebook fill:#ebdef0,stroke:#333,stroke-width:1px;

    %% Data Directories
    subgraph Data Layer
        D_RAW["data/raw/ <br/>(County pages, DHS manual)"]:::data
        D_PROG["data/programs/*.json <br/>(Program rules)"]:::data
        D_DB["data/chroma_db/ <br/>(RAG Vector Store)"]:::data
        D_TRN_BATCH["data/training/batch_*.jsonl"]:::data
        D_TRN_FINAL["data/training/final.jsonl"]:::data
    end

    %% Scripts
    subgraph Scripts & Ingestion
        S_SCRAPE["scripts/scrape_*.py <br/>scripts/download_sam_gov.py"]:::script
        S_BATCH["scripts/batch_extract_dhs.py <br/>scripts/extract_dhs_page.py"]:::script
        S_INGEST["scripts/ingest_all.py"]:::script
        
        S_SCRAPE -->|Scrape web content| D_RAW
        S_BATCH -->|Format JSON payloads to txt| D_RAW
        D_PROG --> S_INGEST
        D_RAW --> S_INGEST
        S_INGEST -->|Create embeddings| D_DB
    end

    %% Training Pipeline
    subgraph Model Training
        T_PREP["training/prepare_dataset.py"]:::train
        T_TRAIN["training/train_unsloth.py"]:::train
        T_EXPGGUF["training/export_gguf.py"]:::train
        T_KAGGLE["training/kaggle_finetune.ipynb"]:::notebook
        
        D_TRN_BATCH --> T_PREP
        T_PREP -->|Combine, validate, dedup| D_TRN_FINAL
        D_TRN_FINAL --> T_TRAIN
        D_TRN_FINAL --> T_KAGGLE
        T_TRAIN -->|Fine-tune model| T_EXPGGUF
        T_EXPGGUF -->|Modelfile & .gguf| M_OUT["Ollama / GGUF Model Artifacts"]:::data
    end

    %% Deployment
    subgraph Deployment
        D_MODAL_FT["deploy/modal_finetune.py"]:::deploy
        D_MODAL_APP["deploy/modal_app.py"]:::deploy
        
        D_TRN_FINAL --> D_MODAL_FT
        D_MODAL_FT -->|Modal Cloud Fine-tuning| M_OUT
        
        D_DB --> D_MODAL_APP
        D_PROG --> D_MODAL_APP
        D_RAW -.-> D_MODAL_APP
    end

    %% Root
    subgraph Project Root
        R_MAIN["gemma4_goodhackathon_main.ipynb"]:::notebook
        R_SAMP["sample.ipynb"]:::notebook
    end
    
    %% Final Integration
    M_OUT -.->|Provides Model| D_MODAL_APP
    M_OUT -.->|Provides Model| R_MAIN
    D_DB -.->|Provides RAG| R_MAIN
```

