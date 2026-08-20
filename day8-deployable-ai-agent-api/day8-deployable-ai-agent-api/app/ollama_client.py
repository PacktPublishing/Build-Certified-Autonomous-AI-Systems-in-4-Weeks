import httpx

from app.config import settings


class OllamaError(RuntimeError):
    pass


async def ask_ollama(message: str, system_prompt: str | None = None, model: str | None = None) -> str:
    selected_model = model or settings.ollama_model

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": message})

    payload = {
        "model": selected_model,
        "messages": messages,
        "stream": False,
    }

    url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"

    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
    except httpx.ConnectError as exc:
        raise OllamaError(
            "Could not connect to Ollama. Make sure Ollama is running and OLLAMA_BASE_URL is correct."
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise OllamaError(f"Ollama returned an error: {exc.response.text}") from exc
    except httpx.TimeoutException as exc:
        raise OllamaError("Ollama took too long to respond. Try a smaller model or retry the request.") from exc

    data = response.json()
    return data.get("message", {}).get("content", "")
