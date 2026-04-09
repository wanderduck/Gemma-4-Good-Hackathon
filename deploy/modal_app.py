"""Modal deployment for NorthStar Navigator.

Serves the Gradio UI + Ollama with Gemma model on a GPU instance.

Usage:
    modal serve deploy/modal_app.py     # Dev mode (ephemeral URL)
    modal deploy deploy/modal_app.py    # Production (persistent URL)

Cost estimate with $60 Modal credit:
    T4 GPU: ~$0.59/hr → ~100 hours of runtime
    Container scales to zero when idle (no cost when not in use)
"""

import subprocess
import time

import modal

# ---------------------------------------------------------------------------
# Image: Ollama + Navigator dependencies on CUDA base
# ---------------------------------------------------------------------------

navigator_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.6.3-runtime-ubuntu22.04", add_python="3.13"
    )
    .entrypoint([])
    # Install curl + Ollama
    .run_commands(
        "apt-get update && apt-get install -y curl zstd && rm -rf /var/lib/apt/lists/*",
        "curl -fsSL https://ollama.com/install.sh | sh",
    )
    # Install Navigator dependencies (subset needed for serving)
    .pip_install(
        "gradio>=5.29.0",
        "chromadb>=1.0.0",
        "sentence-transformers>=4.1.0",
        "rank-bm25>=0.2.2",
        "textstat>=0.7.4",
        "ollama>=0.5.1",
        "pydantic>=2.11.3",
        "httpx>=0.28.1",
    )
    # Bake application source into the image
    .add_local_dir("src", remote_path="/app/src", copy=True)
    .add_local_dir("data/programs", remote_path="/app/data/programs", copy=True)
    .add_local_dir(
        "data/raw/dhs_combined_manual",
        remote_path="/app/data/raw/dhs_combined_manual",
        copy=True,
        ignore=["_temp_*", "_toc_*", "_ch13_*"],
    )
)

# ---------------------------------------------------------------------------
# Volumes: persist model weights and ChromaDB across restarts
# ---------------------------------------------------------------------------

ollama_models_vol = modal.Volume.from_name(
    "navigator-ollama-models", create_if_missing=True
)
chroma_vol = modal.Volume.from_name(
    "navigator-chroma-db", create_if_missing=True
)

app = modal.App("plain-language-navigator", image=navigator_image)

OLLAMA_MODEL = "gemma3:4b"
GRADIO_PORT = 7860
MINUTES = 60


def _start_ollama():
    """Start Ollama server and wait for it to be ready."""
    import os

    proc = subprocess.Popen(
        ["ollama", "serve"],
        env={**os.environ, "OLLAMA_HOST": "0.0.0.0:11434"},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    import httpx
    for i in range(60):
        try:
            resp = httpx.get("http://localhost:11434/api/tags", timeout=2)
            if resp.status_code == 200:
                print(f"Ollama ready after {i+1}s")
                return proc
        except Exception:
            pass
        time.sleep(1)

    print("WARNING: Ollama may not be ready after 60s")
    return proc


# ---------------------------------------------------------------------------
# Main serving function: Ollama + Gradio on one GPU container
# ---------------------------------------------------------------------------

@app.function(
    gpu="T4",
    timeout=30 * MINUTES,
    scaledown_window=10 * MINUTES,
    volumes={
        "/root/.ollama": ollama_models_vol,
        "/app/data/chroma_db": chroma_vol,
    },
)
@modal.concurrent(max_inputs=10)
@modal.web_server(port=GRADIO_PORT, startup_timeout=10 * MINUTES)
def serve():
    """Start Ollama, pull model if needed, then launch Gradio."""
    import os
    import sys

    # Add src to path so navigator package is importable
    sys.path.insert(0, "/app/src")

    # Set environment for ChromaDB
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

    # Override config paths for Modal container layout
    os.environ["NAVIGATOR_DATA_DIR"] = "/app/data"

    # Start Ollama
    _start_ollama()

    # Pull model if not already cached in volume
    print(f"Ensuring model {OLLAMA_MODEL} is available...")
    result = subprocess.run(
        ["ollama", "pull", OLLAMA_MODEL],
        capture_output=True,
        text=True,
        timeout=600,
    )
    print(f"Model pull: {result.stdout}")
    if result.returncode != 0:
        print(f"Model pull error: {result.stderr}")

    # Commit volume so model persists across restarts
    ollama_models_vol.commit()

    # Launch Gradio
    print("Starting Gradio UI...")
    from app import demo
    demo.launch(
        server_name="0.0.0.0",
        server_port=GRADIO_PORT,
        share=False,
        theme="soft",
    )


# ---------------------------------------------------------------------------
# Utility: pre-pull model into volume (run once)
# ---------------------------------------------------------------------------

@app.function(
    gpu="T4",
    timeout=15 * MINUTES,
    volumes={"/root/.ollama": ollama_models_vol},
)
def pull_model(model_name: str = OLLAMA_MODEL):
    """Pull a model into the persistent volume. Run with:
        modal run deploy/modal_app.py::pull_model
    """
    proc = _start_ollama()

    print(f"Pulling {model_name}...")
    result = subprocess.run(
        ["ollama", "pull", model_name],
        capture_output=True,
        text=True,
        timeout=600,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise RuntimeError(f"Failed to pull {model_name}")

    ollama_models_vol.commit()
    print(f"Model {model_name} cached in volume.")
    proc.terminate()


# ---------------------------------------------------------------------------
# Utility: upload ChromaDB to volume (run once after local ingestion)
# ---------------------------------------------------------------------------

chroma_upload_image = (
    modal.Image.debian_slim(python_version="3.13")
    .add_local_dir("data/chroma_db", remote_path="/tmp/local_chroma", copy=True)
)


@app.function(
    image=chroma_upload_image,
    timeout=5 * MINUTES,
    volumes={"/app/data/chroma_db": chroma_vol},
)
def upload_chroma():
    """Upload local ChromaDB to Modal volume. Run with:
        modal run deploy/modal_app.py::upload_chroma
    """
    import os
    import shutil

    print("Copying local ChromaDB to Modal volume...")
    src = "/tmp/local_chroma"
    dst = "/app/data/chroma_db"

    # Clear existing contents and copy fresh
    for item in os.listdir(dst):
        path = os.path.join(dst, item)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    # Copy contents into the volume mount point
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    chroma_vol.commit()
    print("ChromaDB uploaded to Modal volume.")


@app.local_entrypoint()
def main():
    """Quick test: pull model + upload chroma, then print URL."""
    print("Step 1: Pulling model into volume...")
    pull_model.remote()
    print("Step 2: Uploading ChromaDB...")
    upload_chroma.remote()
    print("Done! Deploy with: modal deploy deploy/modal_app.py")
