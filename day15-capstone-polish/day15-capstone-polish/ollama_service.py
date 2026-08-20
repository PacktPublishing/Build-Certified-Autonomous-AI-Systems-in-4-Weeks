import os

import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "180"))


class OllamaServiceError(Exception):
    pass


def call_ollama(prompt: str, system_prompt: str, model: str | None = None) -> str:
    selected_model = model or OLLAMA_MODEL
    url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat"

    payload = {
        "model": selected_model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }

    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise OllamaServiceError(
            "Could not connect to Ollama. Start Ollama with: ollama serve"
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise OllamaServiceError(
            "Ollama took too long to respond. Try again or use a smaller local model."
        ) from exc
    except requests.exceptions.HTTPError as exc:
        raise OllamaServiceError(f"Ollama returned an error: {response.text}") from exc

    data = response.json()
    return data.get("message", {}).get("content", "").strip()
