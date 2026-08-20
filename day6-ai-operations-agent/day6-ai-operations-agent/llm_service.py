"""Ollama service functions for the Day 6 AI Operations Agent lab."""

from __future__ import annotations

import json
import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))


class OllamaError(RuntimeError):
    """Raised when Ollama cannot return the response this lab expects."""


def _chat(messages: list[dict[str, str]], *, format_json: bool = False) -> str:
    """Send a chat request to Ollama and return the assistant message content."""

    payload: dict[str, Any] = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }

    if format_json:
        payload["format"] = "json"

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaError(
            "Could not reach Ollama. Make sure Ollama is running and the model is pulled. "
            f"Current model: {OLLAMA_MODEL}. Original error: {exc}"
        ) from exc

    data = response.json()
    return data.get("message", {}).get("content", "")


def decide_tool(user_request: str, tools: list[dict[str, Any]]) -> dict[str, Any]:
    """Ask Ollama to choose exactly one tool and return structured JSON."""

    system_prompt = f"""
You are a tool-routing assistant for an AI operations agent.

Choose the best tool for the user's request.
Return ONLY valid JSON with this exact shape:
{{
  "tool_name": "calculator | ticket_lookup | system_status | summary_writer",
  "arguments": {{}}
}}

Available tools:
{json.dumps(tools, indent=2)}

Rules:
- Use calculator for arithmetic.
- Use ticket_lookup for incident or ticket IDs such as INC1001.
- Use system_status for health, uptime, service status, CPU, memory, or platform checks.
- Use summary_writer when the user asks to summarize, shorten, or create a brief.
- Do not invent tool names.
- Put only the arguments needed by the selected tool.
""".strip()

    content = _chat(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_request},
        ],
        format_json=True,
    )

    try:
        decision = json.loads(content)
    except json.JSONDecodeError as exc:
        raise OllamaError(f"Ollama did not return valid JSON: {content}") from exc

    if "tool_name" not in decision or "arguments" not in decision:
        raise OllamaError(f"Ollama returned JSON with the wrong shape: {decision}")

    if not isinstance(decision["arguments"], dict):
        raise OllamaError(f"Tool arguments must be a JSON object: {decision}")

    return decision


def write_final_answer(user_request: str, tool_result: dict[str, Any]) -> str:
    """Ask Ollama to turn a raw tool result into a friendly final answer."""

    system_prompt = """
You are a helpful AI operations assistant.
Explain the tool result in a clear, beginner-friendly way.
Keep the answer concise.
If the tool returned an error, explain what went wrong and how the user can fix it.
""".strip()

    user_prompt = f"""
Original user request:
{user_request}

Tool result JSON:
{json.dumps(tool_result, indent=2)}

Write the final answer for the user.
""".strip()

    return _chat(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        format_json=False,
    )
