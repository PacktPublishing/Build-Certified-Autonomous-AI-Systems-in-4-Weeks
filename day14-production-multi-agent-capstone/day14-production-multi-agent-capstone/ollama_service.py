"""Small Ollama client used by the capstone agents."""

from __future__ import annotations

import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class OllamaService:
    """Wrapper around the local Ollama generate API."""

    model: str = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    timeout: int = 120

    def is_available(self) -> bool:
        """Return True when the local Ollama server is reachable."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.2) -> str:
        """Send one prompt to Ollama and return the model response text."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": 900,
            },
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(
                "Could not reach Ollama. Make sure Ollama is running and the model is available. "
                f"Try: ollama pull {self.model}"
            ) from exc

        data = response.json()
        return data.get("response", "").strip()
