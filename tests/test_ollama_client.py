"""Tests for the Ollama client wrapper.

These tests mock the ollama library so they run without a running Ollama server.
Tests that require a live Ollama server are marked with @pytest.mark.ollama.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from navigator.ollama_client import OllamaClient


@pytest.fixture
def client():
    return OllamaClient(model="gemma4:4b-it-q4_0")


def test_client_init(client):
    assert client.model == "gemma4:4b-it-q4_0"


def test_build_messages_with_system(client):
    messages = client._build_messages(
        user_message="Hello",
        system_prompt="You are a helpful assistant.",
    )
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are a helpful assistant."
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "Hello"


def test_build_messages_with_history(client):
    history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"},
    ]
    messages = client._build_messages(
        user_message="What programs?",
        system_prompt="System",
        history=history,
    )
    assert len(messages) == 4  # system + 2 history + new user
    assert messages[3]["role"] == "user"
    assert messages[3]["content"] == "What programs?"


@patch("navigator.ollama_client.ollama")
def test_chat_returns_response(mock_ollama, client):
    mock_ollama.chat.return_value = {
        "message": {"role": "assistant", "content": "Here are some programs."},
    }
    result = client.chat("What programs am I eligible for?")
    assert result == "Here are some programs."
    mock_ollama.chat.assert_called_once()


@patch("navigator.ollama_client.ollama")
def test_chat_with_json_output(mock_ollama, client):
    mock_ollama.chat.return_value = {
        "message": {
            "role": "assistant",
            "content": '{"income": 32000, "household_size": 3}',
        },
    }
    result = client.chat_json("Extract the profile")
    assert result["income"] == 32000
    assert result["household_size"] == 3
