"""Transparent scoring rules for product ideas.

The scoring is intentionally simple so learners can understand and modify it.
"""

from __future__ import annotations

from typing import Any

VIRAL_WORDS = {
    "share",
    "shareable",
    "team",
    "teammates",
    "manager",
    "customer",
    "clients",
    "report",
    "brief",
    "summary",
    "snapshot",
    "template",
    "download",
    "before-and-after",
    "recommend",
}

CLARITY_WORDS = {
    "brief",
    "summary",
    "checklist",
    "plan",
    "draft",
    "report",
    "score",
    "recommendation",
    "output",
    "workflow",
}

CAPSTONE_WORDS = {
    "streamlit",
    "ollama",
    "local",
    "markdown",
    "form",
    "file",
    "export",
    "prototype",
    "mvp",
    "student",
    "capstone",
}


def _combined_text(idea: dict[str, Any]) -> str:
    values: list[str] = []
    for value in idea.values():
        if isinstance(value, list):
            values.extend(str(item) for item in value)
        else:
            values.append(str(value))
    return " ".join(values).lower()


def _keyword_score(text: str, keywords: set[str], max_points: int) -> int:
    matches = [word for word in keywords if word in text]
    if not matches:
        return 0
    return min(max_points, len(matches) * 5)


def score_idea(idea: dict[str, Any]) -> dict[str, Any]:
    """Add practical scores to one idea."""
    text = _combined_text(idea)

    clarity_score = 40
    clarity_score += _keyword_score(text, CLARITY_WORDS, 20)
    if len(str(idea.get("one_liner", ""))) >= 45:
        clarity_score += 10
    if idea.get("main_output"):
        clarity_score += 10
    clarity_score = min(100, clarity_score)

    pain_score = 45
    if idea.get("painful_workflow"):
        pain_score += 20
    if any(word in text for word in ["pain", "manual", "messy", "slow", "confusing", "repetitive"]):
        pain_score += 15
    pain_score = min(100, pain_score)

    viral_score = 35
    viral_score += _keyword_score(text, VIRAL_WORDS, 35)
    if idea.get("why_it_could_spread"):
        viral_score += 15
    viral_score = min(100, viral_score)

    build_score = 40
    build_score += _keyword_score(text, CAPSTONE_WORDS, 35)
    features = idea.get("prototype_features", [])
    if isinstance(features, list) and len(features) >= 3:
        build_score += 15
    build_score = min(100, build_score)

    total_score = round(
        clarity_score * 0.25
        + pain_score * 0.25
        + viral_score * 0.25
        + build_score * 0.25
    )

    scored = dict(idea)
    scored["scores"] = {
        "clarity": clarity_score,
        "pain_strength": pain_score,
        "shareability": viral_score,
        "capstone_buildability": build_score,
        "total": total_score,
    }
    return scored


def score_ideas(ideas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Score and sort ideas from best to weakest."""
    scored_ideas = [score_idea(idea) for idea in ideas]
    return sorted(scored_ideas, key=lambda item: item["scores"]["total"], reverse=True)
