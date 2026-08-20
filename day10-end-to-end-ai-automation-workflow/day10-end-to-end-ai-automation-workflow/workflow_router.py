from ollama_service import call_ollama
from prompt_templates import ROUTER_SYSTEM_PROMPT, build_router_prompt

ALLOWED_ACTIONS = {"summary", "task_list", "escalation"}


def normalize_action(raw_action: str) -> str:
    action = raw_action.strip().lower()

    if "task" in action:
        return "task_list"
    if "escalation" in action or "urgent" in action:
        return "escalation"
    if "summary" in action or "summarize" in action:
        return "summary"

    return "summary"


def route_event(event: dict) -> str:
    raw_action = call_ollama(
        prompt=build_router_prompt(event),
        system_prompt=ROUTER_SYSTEM_PROMPT,
    )

    action = normalize_action(raw_action)

    if action not in ALLOWED_ACTIONS:
        return "summary"

    return action
