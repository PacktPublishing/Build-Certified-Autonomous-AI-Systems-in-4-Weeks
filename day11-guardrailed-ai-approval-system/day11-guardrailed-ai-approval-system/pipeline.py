"""Main safe response pipeline for the Day 11 lab."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from uuid import uuid4

import requests

from guardrails import OutputCheckResult, RiskAssessment, ValidationResult, check_output, classify_risk, validate_request
from ollama_service import OllamaClient
from prompt_templates import DRAFT_SYSTEM_PROMPT, DRAFT_USER_PROMPT, FALLBACK_DRAFT_TEMPLATE


@dataclass
class PipelineResult:
    request_id: str
    created_at: str
    request_text: str
    audience: str
    channel: str
    validation: ValidationResult
    risk: RiskAssessment | None
    draft: str
    output_checks: OutputCheckResult | None
    llm_status: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["validation"] = self.validation.to_dict()
        data["risk"] = self.risk.to_dict() if self.risk else None
        data["output_checks"] = self.output_checks.to_dict() if self.output_checks else None
        return data


def _shorten(text: str, limit: int = 280) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def build_draft_prompt(request_text: str, audience: str, channel: str, risk: RiskAssessment) -> str:
    return DRAFT_USER_PROMPT.format(
        audience=audience,
        channel=channel,
        risk_level=risk.risk_level,
        risk_reasons="; ".join(risk.reasons),
        recommended_action=risk.recommended_action,
        request_text=request_text,
    )


def fallback_draft(request_text: str, risk: RiskAssessment) -> str:
    """Fallback draft keeps the demo usable even if Ollama is not running."""
    return FALLBACK_DRAFT_TEMPLATE.format(
        short_request=_shorten(request_text),
        recommended_action=risk.recommended_action,
    )


def run_pipeline(
    request_text: str,
    audience: str,
    channel: str,
    client: OllamaClient | None = None,
    use_llm: bool = True,
) -> PipelineResult:
    """Run validate -> classify -> draft -> output checks."""
    request_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    validation = validate_request(request_text, audience, channel)
    if not validation.is_valid:
        return PipelineResult(
            request_id=request_id,
            created_at=created_at,
            request_text=request_text,
            audience=audience,
            channel=channel,
            validation=validation,
            risk=None,
            draft="",
            output_checks=None,
            llm_status="Skipped because validation failed.",
        )

    risk = classify_risk(request_text)
    draft = ""
    llm_status = ""

    if use_llm:
        try:
            ollama_client = client or OllamaClient()
            prompt = build_draft_prompt(request_text, audience, channel, risk)
            draft = ollama_client.generate(prompt=prompt, system_prompt=DRAFT_SYSTEM_PROMPT)
            llm_status = "Draft generated with local Ollama."
        except requests.RequestException as exc:
            draft = fallback_draft(request_text, risk)
            llm_status = f"Ollama call failed, so a deterministic fallback draft was used. Details: {exc}"
    else:
        draft = fallback_draft(request_text, risk)
        llm_status = "LLM disabled. Deterministic fallback draft was used."

    output_checks = check_output(draft, risk)

    return PipelineResult(
        request_id=request_id,
        created_at=created_at,
        request_text=request_text,
        audience=audience,
        channel=channel,
        validation=validation,
        risk=risk,
        draft=draft,
        output_checks=output_checks,
        llm_status=llm_status,
    )
