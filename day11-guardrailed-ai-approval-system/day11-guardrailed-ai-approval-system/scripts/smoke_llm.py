"""Ollama-backed smoke test for the Day 11 lab."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline import run_pipeline  # noqa: E402


result = run_pipeline(
    request_text="Write a friendly response to a customer asking when our onboarding webinar starts.",
    audience="Customer",
    channel="Email",
    use_llm=True,
)

print(result.llm_status)
print(result.risk.risk_level if result.risk else "NO_RISK")
print(result.output_checks.passed if result.output_checks else "NO_CHECKS")
print(result.draft[:300])
