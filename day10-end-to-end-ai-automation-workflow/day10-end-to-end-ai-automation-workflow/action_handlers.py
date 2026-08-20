import os
from pathlib import Path

from dotenv import load_dotenv

from ollama_service import call_ollama
from prompt_templates import (
    ESCALATION_SYSTEM_PROMPT,
    SUMMARY_SYSTEM_PROMPT,
    TASK_LIST_SYSTEM_PROMPT,
    build_escalation_prompt,
    build_summary_prompt,
    build_task_list_prompt,
)

load_dotenv()

OUTPUTS_DIR = Path(os.getenv("OUTPUTS_DIR", "outputs"))


def safe_file_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)


def write_output_file(event: dict, action: str, content: str) -> str:
    OUTPUTS_DIR.mkdir(exist_ok=True)

    event_id = safe_file_name(event.get("event_id", "event"))
    output_path = OUTPUTS_DIR / f"{event_id}_{action}.md"

    markdown = f"""# Workflow Output

## Event

- Event ID: {event.get("event_id", "unknown")}
- Source: {event.get("source", "unknown")}
- Subject: {event.get("subject", "")}
- Priority: {event.get("priority", "normal")}
- Action: {action}

## AI Output

{content}
"""

    output_path.write_text(markdown, encoding="utf-8")
    return str(output_path)


def handle_summary(event: dict) -> str:
    content = call_ollama(
        prompt=build_summary_prompt(event),
        system_prompt=SUMMARY_SYSTEM_PROMPT,
    )
    return write_output_file(event, "summary", content)


def handle_task_list(event: dict) -> str:
    content = call_ollama(
        prompt=build_task_list_prompt(event),
        system_prompt=TASK_LIST_SYSTEM_PROMPT,
    )
    return write_output_file(event, "task_list", content)


def handle_escalation(event: dict) -> str:
    content = call_ollama(
        prompt=build_escalation_prompt(event),
        system_prompt=ESCALATION_SYSTEM_PROMPT,
    )
    return write_output_file(event, "escalation", content)


def run_action_handler(event: dict, action: str) -> str:
    if action == "task_list":
        return handle_task_list(event)

    if action == "escalation":
        return handle_escalation(event)

    return handle_summary(event)
