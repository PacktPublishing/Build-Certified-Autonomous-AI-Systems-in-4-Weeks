"""Small service layer for talking to a local Ollama model.

This file keeps all Ollama-specific code in one place so the rest of the app
can focus on the final presentation workflow.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import requests


@dataclass
class OllamaService:
    """Simple client for Ollama's local HTTP API."""

    model: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    timeout_seconds: int = 180

    def generate(self, prompt: str) -> str:
        """Send one prompt to Ollama and return the generated text."""
        url = f"{self.base_url.rstrip('/')}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "top_p": 0.9,
            },
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout_seconds)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError(
                "Could not connect to Ollama. Start it with `ollama serve`, "
                "then make sure your model is pulled."
            ) from exc
        except requests.exceptions.HTTPError as exc:
            raise RuntimeError(
                f"Ollama returned an HTTP error: {response.status_code} {response.text}"
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise RuntimeError(
                "Ollama took too long to respond. Try a smaller model or a shorter product brief."
            ) from exc

        data = response.json()
        generated_text = data.get("response", "").strip()

        if not generated_text:
            raise RuntimeError("Ollama returned an empty response.")

        return generated_text

    def health_check(self) -> str:
        """Return a friendly status message for the local Ollama server."""
        url = f"{self.base_url.rstrip('/')}/api/tags"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                "Ollama is not reachable yet. Start it with `ollama serve`."
            ) from exc

        models = response.json().get("models", [])
        model_names = [item.get("name", "") for item in models]

        if self.model not in model_names:
            return (
                f"Ollama is running, but `{self.model}` was not found locally. "
                f"Run: ollama pull {self.model}"
            )

        return f"Ollama is ready with model `{self.model}`."
