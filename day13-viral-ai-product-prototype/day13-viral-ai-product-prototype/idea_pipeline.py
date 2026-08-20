"""Product idea generation pipeline for Day 13."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from typing import Any

import requests

from file_service import save_best_idea, save_product_brief
from ollama_service import OllamaClient
from prompt_templates import FALLBACK_IDEA_TEMPLATE, PRODUCT_IDEA_SYSTEM_PROMPT, PRODUCT_IDEA_USER_PROMPT
from scoring import score_ideas


@dataclass
class PipelineResult:
    is_valid: bool
    errors: list[str]
    inputs: dict[str, str]
    ideas: list[dict[str, Any]]
    best_idea: dict[str, Any] | None
    product_brief: str
    llm_status: str
    saved_files: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_inputs(target_user: str, painful_workflow: str, desired_output: str) -> tuple[bool, list[str]]:
    """Validate the three required product discovery inputs."""
    errors: list[str] = []

    if not target_user.strip():
        errors.append("Target user is required.")
    if not painful_workflow.strip():
        errors.append("Painful workflow is required.")
    if not desired_output.strip():
        errors.append("Desired output is required.")

    if target_user.strip() and len(target_user.strip()) < 4:
        errors.append("Target user is too short. Add a clearer user group.")
    if painful_workflow.strip() and len(painful_workflow.strip()) < 15:
        errors.append("Painful workflow is too short. Describe the painful task in more detail.")
    if desired_output.strip() and len(desired_output.strip()) < 8:
        errors.append("Desired output is too short. Describe the final output the user wants.")

    return not errors, errors


def build_prompt(target_user: str, painful_workflow: str, desired_output: str) -> str:
    """Create the user prompt sent to Ollama."""
    return PRODUCT_IDEA_USER_PROMPT.format(
        target_user=target_user.strip(),
        painful_workflow=painful_workflow.strip(),
        desired_output=desired_output.strip(),
    )


def _extract_json_object(text: str) -> dict[str, Any]:
    """Extract the first JSON object from an LLM response."""
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned.strip(), flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned.strip()).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(cleaned[start : end + 1])


def _fallback_ideas(target_user: str, painful_workflow: str, desired_output: str) -> list[dict[str, Any]]:
    raw_ideas = FALLBACK_IDEA_TEMPLATE["ideas"]
    ideas: list[dict[str, Any]] = []
    for idea in raw_ideas:
        idea_text = json.dumps(idea)
        idea_text = idea_text.replace("{target_user}", target_user.strip())
        idea_text = idea_text.replace("{painful_workflow}", painful_workflow.strip())
        idea_text = idea_text.replace("{desired_output}", desired_output.strip())
        ideas.append(json.loads(idea_text))
    return ideas


def _normalize_ideas(raw_data: dict[str, Any]) -> list[dict[str, Any]]:
    ideas = raw_data.get("ideas", [])
    if not isinstance(ideas, list):
        return []

    normalized: list[dict[str, Any]] = []
    for index, idea in enumerate(ideas[:3], start=1):
        if not isinstance(idea, dict):
            continue
        normalized.append(
            {
                "name": str(idea.get("name") or f"Product Idea {index}"),
                "one_liner": str(idea.get("one_liner") or "A focused AI product idea for the selected workflow."),
                "target_user": str(idea.get("target_user") or ""),
                "painful_workflow": str(idea.get("painful_workflow") or ""),
                "main_output": str(idea.get("main_output") or ""),
                "why_it_could_spread": str(idea.get("why_it_could_spread") or ""),
                "prototype_features": idea.get("prototype_features") if isinstance(idea.get("prototype_features"), list) else [],
                "capstone_fit": str(idea.get("capstone_fit") or ""),
            }
        )
    return normalized


def generate_product_ideas(
    target_user: str,
    painful_workflow: str,
    desired_output: str,
    client: OllamaClient | None = None,
    use_llm: bool = True,
    save_outputs: bool = True,
) -> PipelineResult:
    """Run the full product idea pipeline."""
    inputs = {
        "target_user": target_user.strip(),
        "painful_workflow": painful_workflow.strip(),
        "desired_output": desired_output.strip(),
    }

    is_valid, errors = validate_inputs(target_user, painful_workflow, desired_output)
    if not is_valid:
        return PipelineResult(
            is_valid=False,
            errors=errors,
            inputs=inputs,
            ideas=[],
            best_idea=None,
            product_brief="",
            llm_status="Skipped because validation failed.",
            saved_files=[],
        )

    llm_status = ""
    raw_ideas: list[dict[str, Any]] = []

    if use_llm:
        try:
            ollama_client = client or OllamaClient()
            prompt = build_prompt(target_user, painful_workflow, desired_output)
            response_text = ollama_client.generate(prompt=prompt, system_prompt=PRODUCT_IDEA_SYSTEM_PROMPT)
            parsed = _extract_json_object(response_text)
            raw_ideas = _normalize_ideas(parsed)
            if len(raw_ideas) != 3:
                raise ValueError("The model did not return exactly 3 usable ideas.")
            llm_status = "Generated 3 product ideas with local Ollama."
        except (requests.RequestException, json.JSONDecodeError, ValueError) as exc:
            raw_ideas = _fallback_ideas(target_user, painful_workflow, desired_output)
            llm_status = f"Ollama output could not be used, so deterministic fallback ideas were used. Details: {exc}"
    else:
        raw_ideas = _fallback_ideas(target_user, painful_workflow, desired_output)
        llm_status = "LLM disabled. Deterministic fallback ideas were used."

    scored_ideas = score_ideas(raw_ideas)
    best_idea = scored_ideas[0]
    product_brief = ""
    saved_files: list[str] = []

    if save_outputs:
        save_best_idea(best_idea=best_idea, all_ideas=scored_ideas, inputs=inputs)
        product_brief = save_product_brief(best_idea=best_idea, inputs=inputs)
        saved_files = ["product_ideas.json", "product_brief.md"]
    else:
        from file_service import create_product_brief

        product_brief = create_product_brief(best_idea=best_idea, inputs=inputs)

    return PipelineResult(
        is_valid=True,
        errors=[],
        inputs=inputs,
        ideas=scored_ideas,
        best_idea=best_idea,
        product_brief=product_brief,
        llm_status=llm_status,
        saved_files=saved_files,
    )
