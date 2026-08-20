from memory_store import build_memory_context
from ollama_service import call_ollama
from prompt_templates import (
    PLANNER_SYSTEM_PROMPT,
    REVIEWER_SYSTEM_PROMPT,
    WRITER_SYSTEM_PROMPT,
    build_planner_prompt,
    build_reviewer_prompt,
    build_writer_prompt,
)


def run_planner_agent(user_request: str) -> str:
    memory_context = build_memory_context()
    return call_ollama(
        prompt=build_planner_prompt(memory_context, user_request),
        system_prompt=PLANNER_SYSTEM_PROMPT,
    )


def run_writer_agent(user_request: str) -> str:
    memory_context = build_memory_context()
    return call_ollama(
        prompt=build_writer_prompt(memory_context, user_request),
        system_prompt=WRITER_SYSTEM_PROMPT,
    )


def run_reviewer_agent(content_to_review: str) -> str:
    memory_context = build_memory_context()
    return call_ollama(
        prompt=build_reviewer_prompt(memory_context, content_to_review),
        system_prompt=REVIEWER_SYSTEM_PROMPT,
    )
