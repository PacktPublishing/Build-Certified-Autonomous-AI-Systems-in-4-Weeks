"""Small Ollama wrapper for the Day 13 lab."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class OllamaSettings:
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model: str = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
    temperature: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.4"))
    num_predict: int = int(os.getenv("OLLAMA_NUM_PREDICT", "800"))


class OllamaClient:
    """Client for local text generation with Ollama."""

    def __init__(self, settings: OllamaSettings | None = None) -> None:
        self.settings = settings or OllamaSettings()
        self.base_url = self.settings.base_url.rstrip("/")

    def health_check(self) -> tuple[bool, str]:
        """Return whether Ollama is reachable and the configured model exists."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            models: list[dict[str, Any]] = response.json().get("models", [])
            model_names = {model.get("name", "") for model in models}

            if self.settings.model in model_names:
                return True, f"Ollama is ready with model {self.settings.model}."

            return False, f"Ollama is running, but {self.settings.model} was not found. Run: ollama pull {self.settings.model}"
        except requests.RequestException as exc:
            return False, f"Could not reach Ollama at {self.base_url}. Start it with: ollama serve. Details: {exc}"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate a response from Ollama."""
        payload: dict[str, Any] = {
            "model": self.settings.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": self.settings.temperature,
                "num_predict": self.settings.num_predict,
            },
        }

        response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()
        return str(data.get("response", "")).strip()
