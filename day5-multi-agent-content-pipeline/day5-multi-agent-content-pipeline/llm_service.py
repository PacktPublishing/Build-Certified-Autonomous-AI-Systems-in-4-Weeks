"""Small Ollama client used by the content agents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class OllamaClient:
    """Thin wrapper around Ollama's local generate API."""

    model: str = "llama3.2:3b"
    base_url: str = "http://localhost:11434"
    timeout: int = 120

    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.7) -> str:
        """Send one prompt to Ollama and return the response text."""
        url = f"{self.base_url.rstrip('/')}/api/generate"
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError(
                "Could not connect to Ollama. Start it with `ollama serve` and try again."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise RuntimeError(
                "Ollama took too long to respond. Try a smaller model or a shorter topic."
            ) from exc
        except requests.exceptions.HTTPError as exc:
            details = response.text.strip()
            raise RuntimeError(f"Ollama returned an error: {details}") from exc

        data = response.json()
        text = data.get("response", "").strip()

        if not text:
            raise RuntimeError("Ollama returned an empty response.")

        return text
