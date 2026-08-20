"""Small Ollama smoke test for the Day 16 lab."""

from __future__ import annotations

import os

from dotenv import load_dotenv

from ollama_service import OllamaService


load_dotenv()


if __name__ == "__main__":
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    service = OllamaService(model=model, base_url=base_url, timeout_seconds=60)
    print(service.health_check())
    print("\nTest generation:")
    print(service.generate("Write one friendly sentence for a final AI product demo."))
