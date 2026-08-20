"""Small service layer for talking to Ollama locally."""

from __future__ import annotations

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
DEFAULT_MODEL = "llama3.2:3b"


class OllamaError(Exception):
    """Raised when the local Ollama request fails."""


def check_ollama_health() -> tuple[bool, str]:
    """Return whether Ollama is reachable on this machine."""
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=3)
        response.raise_for_status()
        models = response.json().get("models", [])
        if not models:
            return True, "Ollama is running, but no local models were listed."
        model_names = ", ".join(model.get("name", "unknown") for model in models[:5])
        return True, f"Ollama is running. Available models: {model_names}"
    except requests.RequestException as exc:
        return False, f"Ollama is not reachable yet: {exc}"


def build_prompt(user_request: str) -> str:
    """Build a beginner-friendly content prompt for the AI copilot."""
    return f"""
You are a helpful AI copilot for a beginner-friendly practical AI course.

Create a polished draft for the user's request.
Keep the response clear, structured, and practical.
Use short sections and simple language.
Do not claim that the draft is approved or saved.

User request:
{user_request}
""".strip()


def generate_draft(user_request: str, model: str = DEFAULT_MODEL) -> str:
    """Send the prompt to Ollama and return the generated draft text."""
    if not user_request.strip():
        raise ValueError("The user request cannot be empty.")

    payload = {
        "model": model,
        "prompt": build_prompt(user_request),
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaError(f"Could not get a response from Ollama: {exc}") from exc

    data = response.json()
    draft = data.get("response", "").strip()

    if not draft:
        raise OllamaError("Ollama returned an empty response.")

    return draft
