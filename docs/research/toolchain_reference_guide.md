# Plain Language Government Navigator -- Toolchain Reference Guide

Comprehensive documentation reference for every library, framework, tool, and platform needed to build the "Plain Language Government Navigator" for the Gemma 4 Good Hackathon.

Last updated: 2026-04-05

---

## Table of Contents

1. [Core AI / Model Tools](#core-ai--model-tools)
   - [Gemma 4 Models](#gemma-4-models)
   - [Ollama](#ollama)
   - [Unsloth](#unsloth)
2. [RAG Stack](#rag-stack)
   - [ChromaDB](#chromadb)
   - [sentence-transformers](#sentence-transformers)
   - [rank_bm25](#rank_bm25)
3. [Web UI](#web-ui)
   - [Gradio](#gradio)
4. [Deployment and Hosting](#deployment-and-hosting)
   - [HuggingFace Spaces](#huggingface-spaces)
   - [Kaggle Notebooks](#kaggle-notebooks)
   - [Google Colab](#google-colab)
5. [Google AI Tools](#google-ai-tools)
   - [Google AI Studio](#google-ai-studio)
   - [Vertex AI](#vertex-ai)
6. [Data Collection](#data-collection)
   - [Web Scraping](#web-scraping)
   - [Government APIs](#government-apis)
7. [Development Environment](#development-environment)
   - [uv](#uv)
   - [Jupyter Lab](#jupyter-lab)
8. [Evaluation and Quality](#evaluation-and-quality)
   - [textstat / Flesch-Kincaid](#textstat--flesch-kincaid)

---

## Core AI / Model Tools

### Gemma 4 Models

**What it is:** Google's open-weight multimodal model family (released April 2, 2026) with pretrained and instruction-tuned variants in E2B, E4B, 26B-A4B (MoE), and 31B parameter sizes. Licensed under Apache 2.0. Supports text, images, video, audio (smaller models), 128K-256K context windows, built-in function calling, and configurable thinking mode.

**Official documentation:**
- Model card: https://ai.google.dev/gemma/docs/core/model_card_4
- HuggingFace Transformers docs: https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/gemma4.md
- HuggingFace blog: https://huggingface.co/blog/gemma4
- Google blog: https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/

**Getting started:** https://ai.google.dev/gemma/docs/core/huggingface_inference

**Installation:**
```bash
uv add transformers accelerate torch
# For the E4B model:
# Model weights: google/gemma-4-E4B-it on HuggingFace
```

**Key concepts for our use case:**

- **Model selection:** E4B is the sweet spot for local development -- fits on an RTX 2080 Ti (11GB) in 4-bit quantized mode (~5GB VRAM). The 31B model is available for higher quality but requires 17-62GB depending on quantization.
- **For the Navigator:** Use E4B locally via Ollama for development iteration; deploy 26B-A4B or 31B on GPU Spaces / Kaggle for production-quality outputs.

#### Prompt Formatting (Gemma 4)

Gemma 4 uses a specific token-based prompt format:

```
<|turn>system
<|think|>You are a helpful government benefits navigator...
<turn|>
<|turn>user
I'm a single mom with two kids making $35,000/year. What benefits am I eligible for?
<turn|>
<|turn>model
[model response here]
<turn|>
```

**Key special tokens:**

| Token | Purpose |
|-------|---------|
| `<\|turn>system`, `<\|turn>user`, `<\|turn>model` | Start of a turn for each role |
| `<turn\|>` | End of a turn |
| `<\|think\|>` | Placed at start of system prompt to enable thinking mode |
| `<\|channel>thought` ... `<channel\|>` | Wraps the model's internal reasoning (when thinking enabled) |
| `<\|tool_call>` ... `<tool_call\|>` | Wraps function/tool calls |
| `<\|tool_response>` ... `<tool_response\|>` | Wraps tool/function results |
| `<\|tool>declaration:` ... `<tool\|>` | Declares available tools |
| `<\|"\|>` | String delimiter inside structured data blocks |

#### Function Calling / Tool Use

Gemma 4 has a native tool-call protocol with dedicated special tokens. Two ways to define tools:

1. **JSON schema** -- manually construct a JSON dictionary with function name, description, parameters
2. **Raw Python functions** -- the system auto-generates JSON schema from type hints and docstrings

**Tool declaration format:**
```
<|tool>declaration:get_benefits{
  "name": "get_benefits",
  "description": "Look up eligible benefits for a household",
  "parameters": {
    "type": "object",
    "properties": {
      "state": {"type": "string"},
      "income": {"type": "number"},
      "household_size": {"type": "integer"}
    },
    "required": ["state", "income", "household_size"]
  }
}<tool|>
```

**Model's function call output:**
```
<|tool_call>call:get_benefits{state:<|"|>California<|"|>, income:35000, household_size:3}<tool_call|>
```

**Feeding results back:**
```
<|tool_response>response:get_benefits{programs:[<|"|>CalFresh<|"|>, <|"|>Medi-Cal<|"|>]}<tool_response|>
```

**For our use case:** Function calling enables the Navigator to call RAG retrieval, eligibility calculators, and external APIs (benefits screening, income limit lookups) as structured tool calls rather than prompt-injected context.

Reference: https://ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4

#### Thinking Mode

- **Enable:** Include `<|think|>` at the very start of the system prompt
- **Disable:** Omit the `<|think|>` token
- **Output format:** When enabled, reasoning appears in `<|channel>thought\n[reasoning]<channel|>` before the answer
- **Gotcha:** The 26B and 31B models may still emit thinking channel tags even when thinking is disabled. Workaround: add an empty thinking token to suppress.
- **For our use case:** Enable thinking for complex eligibility determinations (multi-program, edge cases). Disable for simple FAQ-type responses to reduce latency. You can instruct the model to "think efficiently" for a middle ground.

Reference: https://ai.google.dev/gemma/docs/capabilities/thinking

#### Multilingual Capabilities

- Pre-trained on 140+ languages; out-of-the-box quality support for 35+ languages
- E2B and E4B models include ASR and speech-to-translated-text
- **For our use case:** Critical for serving non-English-speaking populations. Spanish, Chinese, Vietnamese, Korean, Arabic, Tagalog, and Haitian Creole are the most common non-English languages for US benefits seekers. All are well-supported by Gemma 4.

#### Quantization Options

| Format | Size (E4B) | Size (31B) | Notes |
|--------|-----------|-----------|-------|
| BF16 | ~15 GB | ~62 GB | Full precision, best quality |
| Q8_0 | ~8 GB | ~31 GB | Near-lossless, good for export |
| Q4_K_M | ~5 GB | ~18 GB | Good quality/size balance |
| Q4_0 | ~5 GB | ~17 GB | Fast inference, slight quality loss |
| IQ4_XS | ~4 GB | ~16 GB | Aggressive but usable |
| Q2_K | ~3 GB | ~12 GB | Emergency low-VRAM option |

**For our use case:** Use Q4_K_M or Q4_0 for local Ollama development on the RTX 2080 Ti. Use BF16 or Q8_0 on Kaggle T4 (16GB) for evaluation runs.

GGUF files available from: https://huggingface.co/unsloth/gemma-4-E4B-it-GGUF

**Important caveats:**
- Requires `transformers >= 4.52.0` (released April 2026)
- The `any-to-any` pipeline is the easiest entry point for E2B/E4B
- HuggingFace token required to download gated models -- set `HF_TOKEN` env var
- When using Transformers directly, use `AutoModelForCausalLM` with `device_map="auto"` for multi-GPU
- The tokenizer handles special tokens automatically when using `apply_chat_template()`

**Best tutorial:** https://huggingface.co/blog/gemma4

---

### Ollama

**What it is:** A tool for running LLMs locally with a single command. Manages model downloads, quantization, GPU memory allocation, and exposes a local REST API compatible with the OpenAI API format. Same-day Gemma 4 support since v0.20.0.

**Official documentation:** https://github.com/ollama/ollama

**Getting started:** https://ollama.com/library/gemma4

**Installation:**
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Verify version (must be >= 0.20.0 for Gemma 4)
ollama --version
```

**Key concepts for our use case:**

- **Model management commands:**

| Command | Purpose |
|---------|---------|
| `ollama pull gemma4` | Download the default E4B model |
| `ollama pull gemma4:e2b` | Download the smallest edge model |
| `ollama pull gemma4:26b` | Download the MoE model |
| `ollama pull gemma4:31b` | Download the full flagship model |
| `ollama list` | Show all downloaded models |
| `ollama ps` | Show models currently loaded in memory |
| `ollama rm gemma4:31b` | Delete a model |
| `ollama run gemma4` | Interactive chat |
| `ollama serve` | Start the API server (usually auto-started) |

- **Python client:**

```bash
uv add ollama
```

```python
from ollama import chat

response = chat(
    model="gemma4",
    messages=[
        {"role": "system", "content": "You are a government benefits navigator..."},
        {"role": "user", "content": "What SNAP benefits am I eligible for?"},
    ],
)
print(response.message.content)
```

- **Streaming responses (for Gradio integration):**

```python
from ollama import chat

stream = chat(
    model="gemma4",
    messages=messages,
    stream=True,
)
for chunk in stream:
    print(chunk.message.content, end="", flush=True)
```

- **REST API (for web app backends):**

```bash
# Default endpoint
curl http://localhost:11434/v1/chat/completions \
  -d '{"model": "gemma4", "messages": [{"role": "user", "content": "Hello"}]}'

# Expose to network
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

- **Thinking mode in Ollama:** Pass `think: true` in the API request options, or use `/set think` in interactive mode.

**Important caveats:**
- E4B is the default when you run `ollama run gemma4` -- good choice for development
- Ollama v0.20.0+ required; earlier versions lack Gemma 4 support
- Tool/function calling works out of the box with Gemma 4 in Ollama -- no prompt engineering needed
- Running `ollama pull gemma4` again updates to the latest version (only downloads diffs)
- When importing fine-tuned models, the chat template must match what was used during training

**Best tutorial:** https://ai.google.dev/gemma/docs/integrations/ollama

---

### Unsloth

**What it is:** An optimized training framework that makes LoRA/QLoRA fine-tuning 2-5x faster with 50-80% less VRAM through hand-written backpropagation kernels. The primary tool for fine-tuning Gemma 4 on consumer hardware. Supports text, vision, audio, and RL fine-tuning.

**Official documentation:** https://docs.unsloth.ai/

**Getting started:** https://unsloth.ai/docs/models/gemma-4/train

**Installation:**
```bash
# In a Kaggle/Colab notebook:
pip install unsloth
# Or with uv:
uv add unsloth
```

**Key concepts for our use case:**

#### Fine-tuning Gemma 4 E4B with QLoRA

```python
from unsloth import FastLanguageModel

# Load model in 4-bit (QLoRA)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/gemma-4-E4B-it",
    max_seq_length=4096,
    load_in_4bit=True,
)

# Apply LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,                    # LoRA rank
    lora_alpha=32,           # Scaling factor
    lora_dropout=0.05,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    use_gradient_checkpointing="unsloth",  # Critical for low VRAM
)
```

#### VRAM Requirements

| Model | Precision | Training VRAM | Inference VRAM |
|-------|-----------|---------------|----------------|
| E4B | QLoRA 4-bit | ~8-10 GB | ~5 GB |
| E4B | BF16 | ~15 GB | ~15 GB |
| 26B-A4B | QLoRA 4-bit | ~14 GB | ~10 GB |

- **RTX 2080 Ti (11 GB):** Can fine-tune E4B with QLoRA. Use `gradient_checkpointing="unsloth"` and `per_device_train_batch_size=2` or lower.
- **Kaggle T4 (16 GB):** Comfortable for E4B QLoRA. Can attempt 26B-A4B QLoRA with aggressive settings.

#### Dataset Format

Unsloth supports several formats. For our use case, **ChatML** (the most common) or **ShareGPT** format:

**ChatML format (recommended):**
```json
[
  {
    "messages": [
      {"role": "system", "content": "You are a plain-language benefits navigator..."},
      {"role": "user", "content": "I make $28,000 and have 3 kids. What help can I get?"},
      {"role": "assistant", "content": "Based on your income and family size..."}
    ]
  }
]
```

**ShareGPT format:**
```json
{
  "conversations": [
    {"from": "system", "value": "You are a plain-language benefits navigator..."},
    {"from": "human", "value": "I make $28,000 and have 3 kids..."},
    {"from": "gpt", "value": "Based on your income and family size..."}
  ]
}
```

Use `standardize_sharegpt()` to convert ShareGPT to ChatML if needed.

**Key functions:**
- `get_chat_template(tokenizer, chat_template="gemma-4")` -- sets the correct template
- `formatting_prompts_func()` -- custom formatting function for your dataset

#### Training

```python
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    args=TrainingArguments(
        output_dir="./gemma4-navigator-finetuned",
        per_device_train_batch_size=2,      # Lower for 11GB VRAM
        gradient_accumulation_steps=8,       # Effective batch = 16
        num_train_epochs=3,
        learning_rate=2e-4,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        bf16=True,
        logging_steps=10,
        save_strategy="epoch",
    ),
)
trainer.train()
```

#### Exporting to Ollama

```python
# Save as GGUF for Ollama
model.save_pretrained_gguf(
    "gemma4-navigator",
    tokenizer,
    quantization_method="q4_k_m",  # or "q8_0" for higher quality
)

# Unsloth auto-generates the Modelfile for Ollama
# Then import into Ollama:
# ollama create navigator -f ./gemma4-navigator/Modelfile
```

**Important caveats:**
- The most common cause of bad results after export is **mismatched chat templates**. Always use the same template for training and inference.
- `use_gradient_checkpointing="unsloth"` (not `True`) -- the Unsloth-specific variant saves 30% more VRAM than standard gradient checkpointing.
- Export to Q8_0 first for best quality, then quantize further if needed.
- Kaggle notebooks have ~12 hours max runtime; plan checkpoint saves accordingly.
- Unsloth Studio (web UI) is now available for no-code fine-tuning, but the Python API gives more control.

**Best tutorial:** https://unsloth.ai/docs/models/gemma-4/train

---

## RAG Stack

### ChromaDB

**What it is:** An open-source vector database designed for AI applications. Handles embedding storage, similarity search, metadata filtering, and full-text search. The 2025 Rust-core rewrite provides up to 4x performance improvement.

**Official documentation:** https://docs.trychroma.com/

**Getting started:** https://docs.trychroma.com/docs/overview/getting-started

**Installation:**
```bash
uv add chromadb
```

**Key concepts for our use case:**

#### Basic Setup with Persistent Storage

```python
import chromadb

# Persistent client -- data survives restarts
client = chromadb.PersistentClient(path="./chroma_benefits_db")

# Create a collection for benefits documents
benefits_collection = client.get_or_create_collection(
    name="benefits_documents",
    metadata={"hnsw:space": "cosine"},  # Use cosine similarity
)
```

#### Adding Documents with Metadata

```python
benefits_collection.add(
    documents=[
        "SNAP provides monthly food assistance to low-income households...",
        "Medicaid provides free or low-cost health coverage...",
    ],
    metadatas=[
        {"program": "SNAP", "state": "federal", "category": "food"},
        {"program": "Medicaid", "state": "federal", "category": "health"},
    ],
    ids=["snap_overview", "medicaid_overview"],
)
```

#### Querying with Metadata Filters

```python
# Find benefits relevant to a query, filtered by state
results = benefits_collection.query(
    query_texts=["food assistance for families with children"],
    n_results=5,
    where={
        "$or": [
            {"state": "federal"},
            {"state": "California"},
        ]
    },
)
# Returns: documents, distances, metadatas, ids
```

**Filter operators:** `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$and`, `$or`, `$contains`, `$not_contains`

#### Custom Embedding Functions

```python
from chromadb.utils import embedding_functions

# Use sentence-transformers (our choice)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="benefits_docs",
    embedding_function=ef,
)
```

**Important caveats:**
- Default embedding function is `all-MiniLM-L6-v2` -- which is exactly what we want
- `PersistentClient` is for local development. For production on HF Spaces, use `HttpClient` or embed directly.
- The `where` filter runs AFTER vector search, so set `n_results` higher than needed and re-rank
- Collection names must be 3-63 characters, start/end with alphanumeric, no consecutive dots
- On HF Spaces with persistent storage, store the Chroma DB under `/data/` to survive restarts

**Best tutorial:** https://www.datacamp.com/tutorial/chromadb-tutorial-step-by-step-guide

---

### sentence-transformers

**What it is:** A Python library for generating dense vector embeddings from text. The `all-MiniLM-L6-v2` model is a fast (5x faster than MPNET), small (22MB), and accurate embedding model producing 384-dimensional vectors. Ideal for semantic search in RAG pipelines.

**Official documentation:** https://sbert.net/

**Getting started:** https://sbert.net/docs/quickstart.html

**Installation:**
```bash
uv add sentence-transformers
```

**Key concepts for our use case:**

```python
from sentence_transformers import SentenceTransformer

# Load model (downloads ~22MB on first use, runs on CPU)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode documents
doc_embeddings = model.encode([
    "SNAP eligibility is based on household income...",
    "WIC provides nutrition assistance to pregnant women...",
])

# Encode a query
query_embedding = model.encode("Am I eligible for food stamps?")

# Compute similarity
from sentence_transformers.util import cos_sim
similarities = cos_sim(query_embedding, doc_embeddings)
```

**For our use case:**
- Use as the embedding function for ChromaDB (ChromaDB uses it by default)
- Run on CPU -- no GPU needed for embedding generation
- Encode all benefits documents offline, store in ChromaDB
- At query time, ChromaDB handles encoding the user question automatically
- 384-dimensional vectors keep storage small even with thousands of benefits documents

**Important caveats:**
- Max input length is 256 tokens; longer documents should be chunked (aim for 200-300 word chunks)
- For government documents, chunk by section/paragraph rather than fixed token count
- The model understands English well; for multilingual queries, consider `paraphrase-multilingual-MiniLM-L12-v2` instead
- No GPU required -- inference is fast enough on CPU for real-time queries

**Best tutorial:** https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

---

### rank_bm25

**What it is:** A Python implementation of BM25, a classic keyword-based ranking algorithm. When combined with vector search (hybrid retrieval), it catches exact keyword matches that embedding models sometimes miss -- critical for government program names, acronyms, and legal terms.

**Official documentation:** https://pypi.org/project/rank-bm25/

**Getting started:** https://github.com/dorianbrown/rank_bm25

**Installation:**
```bash
uv add rank-bm25
```

**Key concepts for our use case:**

```python
from rank_bm25 import BM25Okapi

# Tokenize your corpus
corpus = [
    "SNAP provides monthly food assistance to eligible households",
    "WIC provides nutrition support to women infants and children",
    "TANF provides temporary cash assistance to families",
]
tokenized_corpus = [doc.lower().split() for doc in corpus]

# Create BM25 index
bm25 = BM25Okapi(tokenized_corpus)

# Query
query = "food stamps eligibility"
tokenized_query = query.lower().split()
scores = bm25.get_scores(tokenized_query)
top_docs = bm25.get_top_n(tokenized_query, corpus, n=3)
```

#### Hybrid Retrieval Pattern

```python
def hybrid_search(query, collection, bm25_index, corpus, k=5, alpha=0.5):
    """Combine vector search and BM25 for better retrieval."""
    # Vector search via ChromaDB
    vector_results = collection.query(query_texts=[query], n_results=k * 2)

    # BM25 keyword search
    tokenized_query = query.lower().split()
    bm25_scores = bm25_index.get_scores(tokenized_query)

    # Normalize and combine scores
    # alpha controls the weight: 0 = pure BM25, 1 = pure vector
    # For government docs, alpha=0.4-0.6 works well
    combined = alpha * vector_scores + (1 - alpha) * bm25_scores

    return top_k_by_combined_score
```

**For our use case:** Government benefits documents contain many specific terms (SNAP, TANF, WIC, Section 8, LIHEAP, EITC) that users search by name. BM25 catches these exact keyword matches that embedding similarity might rank lower. Hybrid search gives the best of both worlds.

**Important caveats:**
- BM25 is stateless (no persistence) -- rebuild the index when documents change
- Tokenization matters: consider using NLTK or spaCy tokenizer instead of `.split()` for government text
- BM25 does not understand synonyms ("food stamps" vs "SNAP") -- that is what the vector search handles
- Keep alpha tunable; test with real user queries to find the best balance

**Best tutorial:** https://medium.com/@aunraza021/combining-bm25-vector-search-a-hybrid-approach-for-enhanced-retrieval-performance-a374b4ba4644

---

## Web UI

### Gradio

**What it is:** A Python library for building web interfaces for ML models. `gr.ChatInterface` provides a production-ready chat UI with streaming, message history, and sidebar components. Deploys to HuggingFace Spaces with one command.

**Official documentation:** https://www.gradio.app/docs

**Getting started:** https://www.gradio.app/guides/creating-a-chatbot-fast

**Installation:**
```bash
uv add gradio
```

**Key concepts for our use case:**

#### Basic Chat Interface with Streaming

```python
import gradio as gr
from ollama import chat

def respond(message, history):
    """Stream responses from Ollama/Gemma 4."""
    messages = [{"role": "system", "content": "You are a government benefits navigator..."}]
    for msg in history:
        messages.append(msg)
    messages.append({"role": "user", "content": message})

    stream = chat(model="gemma4", messages=messages, stream=True)
    response = ""
    for chunk in stream:
        response += chunk.message.content
        yield response

demo = gr.ChatInterface(
    fn=respond,
    title="Government Benefits Navigator",
    description="Find benefits you may be eligible for",
    type="messages",  # OpenAI-style message format
)
demo.launch()
```

#### One-Line Ollama Backend

```python
import gradio as gr

# If Ollama is running locally:
demo = gr.load_chat(
    "http://localhost:11434/v1/",
    model="gemma4",
)
demo.launch()
```

#### Adding Sidebar Components (User Profile)

```python
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Your Profile")
            state = gr.Dropdown(label="State", choices=["CA", "NY", "TX", ...])
            household_size = gr.Number(label="Household Size", value=1)
            income = gr.Number(label="Annual Income")
            has_children = gr.Checkbox(label="Children under 18?")
            submit_profile = gr.Button("Update Profile")

        with gr.Column(scale=3):
            chatbot = gr.ChatInterface(
                fn=respond,
                additional_inputs=[state, household_size, income, has_children],
                type="messages",
            )
```

#### Collapsible Sources Panel

```python
with gr.Accordion("Sources", open=False):
    sources_display = gr.Markdown("No sources yet.")
```

#### Streaming Optimization

Gradio only sends the "diff" of each message from server to frontend, reducing latency and data consumption. The `yield` pattern handles this automatically.

#### Deploying to HuggingFace Spaces

```python
demo.launch()  # Local
# For Spaces: just push the code -- auto-builds on commit
```

#### Gradio + FastAPI

```python
import gradio as gr
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok"}

demo = gr.ChatInterface(fn=respond, type="messages")
app = gr.mount_gradio_app(app, demo, path="/")
```

**Important caveats:**
- Use `type="messages"` (not the older `type="tuples"`) for OpenAI-compatible message format
- `gr.ChatInterface` function must accept `(message: str, history: list)` as first two args
- Additional inputs (sidebar fields) come after history in the function signature
- For file uploads (e.g., tax documents), add `multimodal=True` to ChatInterface
- Gradio auto-generates a shareable link with `demo.launch(share=True)` for demo purposes
- Theme customization: `gr.themes.Soft()` or `gr.themes.Default()` -- use `gr.themes.builder()` for custom themes

**Best tutorial:** https://www.gradio.app/guides/creating-a-chatbot-fast

---

## Deployment and Hosting

### HuggingFace Spaces

**What it is:** A hosting platform for ML demo apps. Supports Gradio, Streamlit, and Docker. Offers free CPU instances and paid GPU instances (A10G from ~$0.60/hr). Integrated with HuggingFace model hub.

**Official documentation:** https://huggingface.co/docs/hub/spaces

**Getting started:** https://huggingface.co/docs/hub/spaces-sdks-gradio

**Key concepts for our use case:**

#### Setup

1. Create a new Space at https://huggingface.co/new-space
2. Select "Gradio" SDK
3. Push code via git or web interface

#### Space Configuration (README.md header)

```yaml
---
title: Government Benefits Navigator
emoji: 🏛️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.x
app_file: app.py
pinned: true
suggested_hardware: a10g-small
suggested_storage: small
---
```

#### GPU Spaces

| Hardware | VRAM | Cost/hr | Use Case |
|----------|------|---------|----------|
| cpu-basic | 0 | Free | UI-only, API calls |
| cpu-upgrade | 0 | $0.03 | Heavier CPU tasks |
| t4-small | 16 GB | $0.60 | E4B inference |
| a10g-small | 24 GB | $1.05 | 26B-A4B inference |
| a10g-large | 24 GB | $3.15 | 31B inference |

#### ZeroGPU (Free GPU Access)

HuggingFace offers ZeroGPU for Spaces -- dynamic GPU allocation that is free for most uses. Decorate GPU-needing functions with `@spaces.GPU`:

```python
import spaces

@spaces.GPU
def generate_response(message):
    # This function gets a GPU when called
    ...
```

#### Persistent Storage

Set `HF_HOME=/data/.huggingface` in Space settings so model downloads persist across restarts. Storage tiers: small (20GB), medium (150GB), large (1TB).

#### Environment Variables / Secrets

Set via the Space Settings page. Access in code as `os.environ["SECRET_NAME"]`. Use for API keys, HF tokens, etc.

**Important caveats:**
- Spaces auto-sleep after inactivity (configurable); first request after sleep takes 30-60s to cold start
- GPU Spaces bill by the hour even when idle (unless using ZeroGPU)
- Persistent storage is billed monthly ($5/mo for small)
- Git LFS required for files > 10MB
- Build failures are the most common issue -- test `requirements.txt` locally first

**Best tutorial:** https://huggingface.co/docs/hub/en/spaces-gpus

---

### Kaggle Notebooks

**What it is:** Free cloud notebooks with GPU access (T4 x2, 16GB each). Up to 30 hours/week of GPU time. Pre-installed ML libraries. Used for hackathon submission.

**Official documentation:** https://www.kaggle.com/docs

**Getting started:** https://www.kaggle.com/docs/packages

**Key concepts for our use case:**

- **GPU access:** Select "GPU T4 x2" from the Accelerator dropdown in notebook settings. Up to 30 hrs/week free.
- **Installing packages:** Enable "Internet" in Settings, then `!pip install package_name` in a cell
- **Kaggle Secrets:** Settings > Add-ons > Secrets. Access via:

```python
from kaggle_secrets import UserSecretsClient
secrets = UserSecretsClient()
hf_token = secrets.get_secret("HF_TOKEN")
```

- **Session limits:** 12-hour max runtime. Save checkpoints to `/kaggle/working/` (persists as notebook output).
- **Competition submission:** The notebook itself IS the submission artifact. Include all code, outputs, and results.

**Important caveats:**
- Internet must be enabled BEFORE the session starts for pip installs
- `/kaggle/working/` is the output directory that persists
- Notebooks attached to competitions may have internet disabled -- check competition rules
- T4 x2 gives 32GB total VRAM but requires PyTorch DataParallel/DistributedDataParallel to use both GPUs

**Best tutorial:** https://www.kaggle.com/docs/packages

---

### Google Colab

**What it is:** Google's hosted Jupyter environment. Free tier includes T4 GPU; Colab Pro ($12/mo) offers A100 (40GB) and longer runtimes. Good for Unsloth training runs that exceed Kaggle's 12-hour limit.

**Official documentation:** https://colab.research.google.com/

**Key concepts for our use case:**

- **GPU selection:** Runtime > Change runtime type > A100 (Colab Pro) or T4 (free)
- **Installing packages:**
```python
!pip install unsloth
```
- **Mounting Drive (for checkpoints):**
```python
from google.colab import drive
drive.mount('/content/drive')
# Save to: /content/drive/MyDrive/gemma4-checkpoints/
```
- **Running Unsloth training:** Same code as above, but set `output_dir="/content/drive/MyDrive/checkpoints"` to persist through session disconnects
- **Session management:** Colab Pro sessions can last 24 hours. Free tier disconnects after ~90 minutes of inactivity. Keep a browser tab open.

**Important caveats:**
- Free tier A100 access is rare and unreliable -- Colab Pro is worth the $12/mo for this project
- Always save checkpoints to Google Drive, not local storage
- Colab uses its own Python environment -- install Unsloth fresh each session
- High RAM runtime (available in Pro) useful for loading large datasets

**Best tutorial:** Unsloth provides Colab-ready notebooks: https://unsloth.ai/docs/models/gemma-4/train

---

## Google AI Tools

### Google AI Studio

**What it is:** A free web-based IDE for prototyping with Google AI models, including Gemma 4. Offers a playground for prompt engineering, a "Thoughts" toggle for inspecting chain-of-thought reasoning, and a "Get Code" button to export working prompts to Python code. Available via the Gemini API.

**Official documentation:** https://aistudio.google.com/

**Getting started:** https://aistudio.google.com/ (log in with Google account)

**Key concepts for our use case:**

- **Prompt engineering:** Iterate on system prompts for the Navigator in the playground before coding
- **Thinking mode debugging:** Toggle "Thoughts" to see the model's chain-of-thought -- invaluable for debugging eligibility logic
- **Code export:** Once a prompt works, click "Get Code" to get Python/Node.js/cURL code using the Gemini API
- **Tool calling testing:** Test function calling schemas in the playground before implementing locally
- **Image input:** Drop images directly into prompts (useful for testing document parsing later)
- **Free API tier:** Gemma 4 is accessible through the Gemini API with a free tier

**Limitations vs. running your own model:**
- Cannot fine-tune through AI Studio
- Rate limits on free tier
- Data goes through Google's servers (privacy consideration for PII in benefits applications)
- Less control over generation parameters than local Ollama
- No persistent sessions or user state

**Best tutorial:** https://dev.to/googleai/hacking-with-multimodal-gemma-4-in-ai-studio-3had

---

### Vertex AI

**What it is:** Google Cloud's enterprise ML platform. Can deploy Gemma 4 to dedicated endpoints with auto-scaling. Relevant if you need cloud-hosted inference without managing your own GPU server.

**Official documentation:** https://cloud.google.com/vertex-ai

**Getting started:** https://cloud.google.com/blog/products/ai-machine-learning/gemma-4-available-on-google-cloud

**Key concepts for our use case:**

- **Free tier:** New Google Cloud users get $300 in credits for 90 days. "Express mode" free tier available without billing info.
- **Model Garden:** Deploy Gemma 4 from the Model Garden with a few clicks -- select model, provision compute, deploy.
- **Gemini API access:** Gemma 4 is also accessible via the Gemini API endpoints on Vertex AI.
- **When to use:** If HuggingFace Spaces GPU becomes too expensive for sustained demo access, Vertex AI with free credits is an alternative.

**Important caveats:**
- No built-in monthly spend cap -- set budget alerts
- More complex setup than HF Spaces for a hackathon demo
- For this project, HF Spaces or Ollama local are probably better choices unless you need enterprise-grade scaling
- The $300 free credit is generous enough for the entire hackathon period

**Best resource:** https://docs.google.com/vertex-ai/generative-ai/docs/start/express-mode/overview

---

## Data Collection

### Web Scraping

**What it is:** Extracting structured data from government benefits websites. You are experienced with this, so keeping it brief.

**Best tools for government sites:**

| Tool | Use Case | Install |
|------|----------|---------|
| `requests` + `BeautifulSoup4` | Static pages, simple scraping | `uv add requests beautifulsoup4` |
| `Scrapy` | Large-scale crawling, sitemaps | `uv add scrapy` |
| `Playwright` | JavaScript-rendered pages (some .gov sites) | `uv add playwright` |

**robots.txt for government sites:**
- Most federal .gov sites allow scraping (public information doctrine)
- Always check `https://domain.gov/robots.txt` first
- Respect `Crawl-delay` directives
- State sites vary more -- some block scrapers
- Add a descriptive `User-Agent` header identifying your project

**SAM.gov API:**
- Register at https://sam.gov/profile/details to get a Public API Key
- Pass key as URL query parameter: `?api_key=YOUR_KEY`
- Non-federal accounts get 1,000 requests/day (10/day without registration)
- Entity API docs: https://open.gsa.gov/api/entity-api/
- Registration takes ~10 business days

---

### Government APIs

#### api.data.gov

- **What:** A unified API key system for many federal government APIs
- **Get API key:** https://api.data.gov/signup/ (instant, free)
- **Usage:** Include key as `api_key` query parameter
- **For our use:** Gateway to DOL, HUD, and other federal data APIs

#### NYC Benefits Screening API

- **What:** Machine-readable eligibility calculations for 35+ City, State, and Federal programs (SNAP, Cash Assistance, WIC, HEAP, Medicaid, etc.)
- **Docs:** https://screeningapidocs.cityofnewyork.us/
- **Auth:** API key required -- register at the docs site
- **How to use:** Send household composition data (income, family size, ages, etc.) and receive eligibility determinations
- **For our use:** The gold standard for benefits screening logic. Even if we build for multiple states, NYC's API provides a reference implementation. Can use their eligibility rules as training data for fine-tuning.
- **Limitation:** NYC programs only -- need to build/find equivalent logic for other jurisdictions

#### CMS Marketplace API

- **What:** Health insurance plan data from HealthCare.gov marketplace
- **Docs:** https://developer.cms.gov/marketplace-api/
- **Auth:** API key from https://developer.cms.gov/
- **How to use:** Query plans by zip code, income, family size; get premium estimates, subsidy calculations
- **For our use:** Essential for the health insurance component of the Navigator. Covers 30 states using HealthCare.gov.

#### HUD API (Income Limits)

- **What:** Housing and Urban Development income limits data by area
- **Docs:** https://www.huduser.gov/portal/dataset/fmr-api.html
- **Auth:** Free, no API key required for basic access
- **How to use:** Look up Area Median Income (AMI) by county/metro area to determine eligibility for Section 8, public housing, and other HUD programs
- **For our use:** Critical for housing benefit eligibility. AMI percentages (30%, 50%, 80%) determine program eligibility.

#### CareerOneStop API

- **What:** Employment, training, and job search data from the Department of Labor
- **Docs:** https://www.careeronestop.org/Developers/WebAPI/web-api.aspx
- **API Explorer:** https://api.careeronestop.org/api-explorer/
- **Auth:** Bearer token -- register at https://www.careeronestop.org/Developers/WebAPI/registration.aspx
- **Usage:**
```python
headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
response = requests.get(
    "https://api.careeronestop.org/v1/...",
    headers=headers,
)
```
- **For our use:** Job training programs, workforce development boards, career services -- relevant for connecting benefits recipients with employment resources.

---

## Development Environment

### uv

**What it is:** A fast Python package manager written in Rust. Already in use in this project.

**Official documentation:** https://docs.astral.sh/uv/

**Key commands:**
```bash
uv sync                     # Install/sync all dependencies from lockfile
uv add chromadb gradio      # Add new dependencies
uv add --dev pytest         # Add dev dependencies
uv run python script.py     # Run a script in the managed environment
uv lock                     # Update the lockfile
```

**For our use case:** All new dependencies should be added via `uv add`. The `uv.lock` file ensures reproducible builds across local dev, Kaggle, and HF Spaces.

**Best tutorial:** https://docs.astral.sh/uv/getting-started/

---

### Jupyter Lab

**What it is:** Already in use. The primary notebook: `gemma4_goodhackathon_main.ipynb`.

**Useful extensions for this project:**
- `jupyterlab-git` -- git integration in the sidebar
- `jupyterlab-lsp` -- code completion and linting
- No special extensions needed beyond what is already configured

**Launch:** `jupyter lab` (from project root, with direnv active)

---

## Evaluation and Quality

### textstat / Flesch-Kincaid

**What it is:** A Python library for calculating readability statistics from text. Implements Flesch-Kincaid Grade Level, Flesch Reading Ease, and many other readability formulas. Essential for ensuring the Navigator's output is genuinely "plain language."

**Official documentation:** https://pypi.org/project/textstat/

**Source / README:** https://github.com/textstat/textstat

**Installation:**
```bash
uv add textstat
```

**Key concepts for our use case:**

```python
import textstat

response = "You may be eligible for SNAP benefits. SNAP helps families buy food..."

# Flesch-Kincaid Grade Level (target: <= 8.0 for plain language)
grade = textstat.flesch_kincaid_grade(response)
# Returns float, e.g., 6.2 means a 6th grader can understand it

# Flesch Reading Ease (target: >= 60 for plain language)
ease = textstat.flesch_reading_ease(response)
# 90-100: very easy, 60-70: standard, 0-30: very confusing

# Other useful metrics
textstat.gunning_fog(response)          # Gunning Fog Index
textstat.coleman_liau_index(response)   # Coleman-Liau Index
textstat.text_standard(response)        # Consensus grade level
```

#### Integration into the Pipeline

```python
def post_process_response(response_text: str) -> dict:
    """Check if the Navigator's response meets plain language standards."""
    grade = textstat.flesch_kincaid_grade(response_text)
    ease = textstat.flesch_reading_ease(response_text)

    return {
        "text": response_text,
        "grade_level": grade,
        "reading_ease": ease,
        "meets_standard": grade <= 8.0 and ease >= 60,
    }

# If meets_standard is False, you could:
# 1. Re-prompt the model to simplify
# 2. Flag for human review
# 3. Log for fine-tuning data collection
```

**Target metrics for our Navigator:**
- Flesch-Kincaid Grade Level: 6th-8th grade (match government plain language guidelines)
- Flesch Reading Ease: 60+ (easily understood by the general public)
- Federal Plain Language Act guidelines: https://www.plainlanguage.gov/

**Important caveats:**
- Readability scores are approximations -- they measure surface features (sentence length, syllable count), not comprehension
- Technical terms like "SNAP" or "Medicaid" inflate the grade level even though users know them -- consider a custom dictionary
- Run readability checks on the model's output, not the RAG source documents
- Use as a guardrail, not a hard gate -- some eligibility explanations inherently require complex language
- The `text_standard()` function provides a consensus grade level across multiple formulas

**Best tutorial:** https://www.kaggle.com/code/yhirakawa/textstat-how-to-evaluate-readability

---

## Quick Reference: All Installation Commands

```bash
# Core AI
uv add transformers accelerate torch
uv add ollama

# RAG Stack
uv add chromadb sentence-transformers rank-bm25

# Web UI
uv add gradio

# Data Collection
uv add requests beautifulsoup4 scrapy

# Evaluation
uv add textstat

# Unsloth (Kaggle/Colab only -- heavy deps)
pip install unsloth
```

---

## Quick Reference: Key URLs

| Tool | Start Here |
|------|-----------|
| Gemma 4 | https://huggingface.co/blog/gemma4 |
| Gemma 4 Prompt Format | https://ai.google.dev/gemma/docs/core/prompt-formatting-gemma4 |
| Gemma 4 Function Calling | https://ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4 |
| Gemma 4 Thinking Mode | https://ai.google.dev/gemma/docs/capabilities/thinking |
| Ollama + Gemma 4 | https://ai.google.dev/gemma/docs/integrations/ollama |
| Unsloth + Gemma 4 | https://unsloth.ai/docs/models/gemma-4/train |
| ChromaDB | https://docs.trychroma.com/docs/overview/getting-started |
| sentence-transformers | https://sbert.net/docs/quickstart.html |
| Gradio ChatInterface | https://www.gradio.app/guides/creating-a-chatbot-fast |
| HuggingFace Spaces | https://huggingface.co/docs/hub/spaces-sdks-gradio |
| Google AI Studio | https://aistudio.google.com/ |
| NYC Benefits API | https://screeningapidocs.cityofnewyork.us/ |
| CMS Marketplace API | https://developer.cms.gov/marketplace-api/ |
| textstat | https://github.com/textstat/textstat |

---

## Hackathon Prize Strategy Notes

This toolchain positions us for multiple prize tracks:

- **Main Track ($100K):** The Navigator itself -- impactful AI application using Gemma 4
- **Ollama Special Technology Prize ($10K):** Using Ollama as the inference backend
- **Unsloth Special Technology Prize ($10K):** Fine-tuning with Unsloth for plain-language benefits responses
- Projects can win BOTH Main Track AND Special Technology prizes simultaneously

To maximize prize eligibility, ensure the demo clearly shows:
1. Gemma 4 model usage (required)
2. Ollama as the serving layer (Special Tech)
3. Unsloth fine-tuning pipeline (Special Tech)
4. Live, functional demo (required deliverable)
