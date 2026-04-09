"""Deploy Navigator with Ollama on RunPod Flash.

Runs Ollama inside a Flash endpoint with Gemma 4 E4B GGUF model.
The Navigator app connects by setting OLLAMA_BASE_URL to the endpoint URL.

Usage:
    flash run deploy/flash_navigator.py          # Local dev (hot reload)
    flash deploy deploy/flash_navigator.py       # Deploy to RunPod

    # Upload GGUF to network volume first:
    #   1. Create volume in RunPod console named "navigator-models"
    #   2. Upload your fine-tuned GGUF + Modelfile to the volume root
    #   OR use the upload_model() helper below

Prerequisites:
    pip install runpod-flash
    flash login
"""

from runpod_flash import Endpoint, GpuGroup, NetworkVolume
import asyncio

# Persistent storage for model weights — survives across cold starts
model_volume = NetworkVolume(name="navigator-models")

OLLAMA_MODEL_NAME = "navigator"
GGUF_PATH = "/runpod-volume/model-q4_k_m.gguf"
MODELFILE_PATH = "/runpod-volume/Modelfile"


@Endpoint(
    name="navigator-ollama",
    gpu=GpuGroup.AMPERE_48,  # A40/A6000 48GB — plenty for 9.6GB q4_k_m GGUF
    workers=(0, 2),  # Scale to zero when idle, max 2 for burst
    dependencies=[
        "ollama",
        "httpx",
    ],
    system_dependencies=[
        "curl",
    ],
    volume=model_volume,
    env={
        "OLLAMA_HOST": "0.0.0.0:11434",
        "OLLAMA_MODELS": "/runpod-volume/ollama-models",
    },
    idle_timeout=120,  # Keep warm 2 min after last request
)
async def chat(data: dict) -> dict:
    """Handle chat requests by proxying to local Ollama.

    Input format:
        {
            "messages": [{"role": "user", "content": "..."}],
            "model": "navigator",        # optional, defaults to navigator
            "temperature": 1.0,           # optional
            "top_p": 0.95,                # optional
            "top_k": 64,                  # optional
            "stream": false               # optional, streaming not supported via Flash queue
        }

    Returns:
        {"message": {"role": "assistant", "content": "..."}, "model": "navigator"}
    """
    import subprocess
    import time
    import httpx
    import os

    ollama_url = "http://localhost:11434"

    # --- Start Ollama server if not running ---
    try:
        httpx.get(f"{ollama_url}/api/tags", timeout=2)
    except (httpx.ConnectError, httpx.ReadTimeout):
        # Install Ollama if not present
        if not os.path.exists("/usr/local/bin/ollama"):
            subprocess.run(
                ["bash", "-c", "curl -fsSL https://ollama.com/install.sh | sh"],
                check=True,
                capture_output=True,
            )

        # Start Ollama server in background
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Wait for server to be ready
        for _ in range(30):
            try:
                httpx.get(f"{ollama_url}/api/tags", timeout=2)
                break
            except (httpx.ConnectError, httpx.ReadTimeout):
                time.sleep(1)
        else:
            return {"error": "Ollama server failed to start after 30s"}

    # --- Create model from GGUF if not already loaded ---
    tags_resp = httpx.get(f"{ollama_url}/api/tags", timeout=10)
    models = [m["name"] for m in tags_resp.json().get("models", [])]

    model_name = data.get("model", OLLAMA_MODEL_NAME)

    if model_name not in models and f"{model_name}:latest" not in models:
        modelfile_path = MODELFILE_PATH
        if os.path.exists(modelfile_path):
            # Create model from Modelfile pointing to GGUF on volume
            resp = httpx.post(
                f"{ollama_url}/api/create",
                json={"name": model_name, "modelfile": open(modelfile_path).read()},
                timeout=300,
            )
            if resp.status_code != 200:
                return {"error": f"Failed to create model: {resp.text}"}
        else:
            # Fallback: pull pre-built model from Ollama registry
            resp = httpx.post(
                f"{ollama_url}/api/pull",
                json={"name": "gemma4:e4b"},
                timeout=600,
            )
            model_name = "gemma4:e4b"

    # --- Run inference ---
    messages = data.get("messages", [])
    if not messages:
        return {"error": "No messages provided"}

    chat_resp = httpx.post(
        f"{ollama_url}/api/chat",
        json={
            "model": model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": data.get("temperature", 1.1),
                "top_p": data.get("top_p", 0.95),
                "top_k": data.get("top_k", 64),
            },
        },
        timeout=120,
    )

    if chat_resp.status_code != 200:
        return {"error": f"Ollama chat failed: {chat_resp.text}"}

    result = chat_resp.json()
    return {
        "message": result.get("message", {}),
        "model": model_name,
        "eval_count": result.get("eval_count"),
        "eval_duration": result.get("eval_duration"),
    }


# --- Load-balanced HTTP API (alternative deployment) ---

api = Endpoint(
    name="navigator-api",
    gpu=GpuGroup.AMPERE_48,
    workers=(1, 3),  # Keep 1 warm for demo responsiveness
    dependencies=["ollama", "httpx"],
    system_dependencies=["curl"],
    volume=model_volume,
    env={
        "OLLAMA_HOST": "0.0.0.0:11434",
        "OLLAMA_MODELS": "/runpod-volume/ollama-models",
    },
    idle_timeout=300,
)


@api.post("/v1/chat")
async def api_chat(data: dict) -> dict:
    """OpenAI-ish chat endpoint for direct HTTP access."""
    return await chat(data)


@api.get("/health")
async def health() -> dict:
    """Health check."""
    return {"status": "ok", "model": OLLAMA_MODEL_NAME}


# --- Utility: test locally ---

async def main():
    """Test the endpoint locally."""
    result = await chat({
        "messages": [
            {"role": "user", "content":
             "I'm a single mom with two kids in Hennepin County. "
             "I just lost my job. What help is available?"}
        ],
    })
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Model: {result['model']}")
        print(f"Response: {result['message']['content'][:500]}")


if __name__ == "__main__":
    asyncio.run(main())
