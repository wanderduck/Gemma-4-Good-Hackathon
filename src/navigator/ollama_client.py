"""Ollama API client wrapper for Gemma 4 inference."""

import json
import logging
from collections.abc import Generator

import ollama

from navigator.config import OLLAMA_BASE_URL, OLLAMA_MODEL

logger = logging.getLogger(__name__)


class OllamaClient:
    """Wrapper around the ollama Python client for Navigator use."""

    def __init__(
        self,
        model: str = OLLAMA_MODEL,
        base_url: str = OLLAMA_BASE_URL,
    ):
        self.model = model
        self.base_url = base_url
        self._client = ollama.Client(host=base_url)

    def _build_messages(
        self,
        user_message: str,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
    ) -> list[dict]:
        """Build the messages list for the chat API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})
        return messages

    def chat(
        self,
        user_message: str,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
        temperature: float = 1.0,
        top_p: float = 0.95,
        top_k: int = 64,
    ) -> str:
        """Send a chat message and return the response text."""
        messages = self._build_messages(user_message, system_prompt, history)
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
            },
        )
        return response["message"]["content"]

    def chat_json(
        self,
        user_message: str,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
    ) -> dict:
        """Send a chat message and parse the response as JSON."""
        json_instruction = (
            "\n\nRespond ONLY with valid JSON. No markdown, no explanation, "
            "no code fences. Just the JSON object."
        )
        full_prompt = (system_prompt or "") + json_instruction

        text = self.chat(user_message, system_prompt=full_prompt, history=history)

        # Strip markdown code fences if present
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1]) if len(lines) > 2 else text

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse JSON response: %s\nRaw: %s", e, text)
            raise ValueError(f"Model did not return valid JSON: {e}") from e

    def chat_stream(
        self,
        user_message: str,
        system_prompt: str | None = None,
        history: list[dict] | None = None,
    ) -> Generator[str, None, None]:
        """Stream a chat response token by token."""
        messages = self._build_messages(user_message, system_prompt, history)
        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True,
            options={
                "temperature": 1.0,
                "top_p": 0.95,
                "top_k": 64,
            },
        )
        for chunk in stream:
            token = chunk["message"]["content"]
            if token:
                yield token
