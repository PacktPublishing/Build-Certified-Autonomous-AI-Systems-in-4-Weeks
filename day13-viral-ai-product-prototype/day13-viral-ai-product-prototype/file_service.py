"""File saving helpers for Day 13."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PRODUCT_IDEAS_PATH = Path("product_ideas.json")
PRODUCT_BRIEF_PATH = Path("product_brief.md")


def save_best_idea(
    best_idea: dict[str, Any],
    all_ideas: list[dict[str, Any]],
    inputs: dict[str, str],
    path: Path = PRODUCT_IDEAS_PATH,
) -> dict[str, Any]:
    """Save the best idea plus context to product_ideas.json."""
    payload = {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "inputs": inputs,
        "best_idea": best_idea,
        "all_ideas": all_ideas,
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    return payload


def create_product_brief(best_idea: dict[str, Any], inputs: dict[str, str]) -> str:
    """Create a markdown product brief for the final capstone."""
    scores = best_idea.get("scores", {})
    features = best_idea.get("prototype_features", [])
    feature_lines = "\n".join(f"- {feature}" for feature in features)

    return f"""# Product Brief: {best_idea.get('name', 'Untitled Product')}

## 1. Product Summary

{best_idea.get('one_liner', '')}

## 2. Target User

{best_idea.get('target_user') or inputs.get('target_user', '')}

## 3. Painful Workflow

{best_idea.get('painful_workflow') or inputs.get('painful_workflow', '')}

## 4. Desired Output

{best_idea.get('main_output') or inputs.get('desired_output', '')}

## 5. Why This Could Spread

{best_idea.get('why_it_could_spread', '')}

## 6. Prototype Features

{feature_lines}

## 7. Capstone Fit

{best_idea.get('capstone_fit', '')}

## 8. Product Scores

- Clarity: {scores.get('clarity', 'N/A')}
- Pain Strength: {scores.get('pain_strength', 'N/A')}
- Shareability: {scores.get('shareability', 'N/A')}
- Capstone Buildability: {scores.get('capstone_buildability', 'N/A')}
- Total Score: {scores.get('total', 'N/A')}

## 9. Original Inputs

**Target user:** {inputs.get('target_user', '')}

**Painful workflow:** {inputs.get('painful_workflow', '')}

**Desired output:** {inputs.get('desired_output', '')}
""".strip() + "\n"


def save_product_brief(
    best_idea: dict[str, Any],
    inputs: dict[str, str],
    path: Path = PRODUCT_BRIEF_PATH,
) -> str:
    """Write product_brief.md and return its markdown content."""
    brief = create_product_brief(best_idea, inputs)
    with path.open("w", encoding="utf-8") as file:
        file.write(brief)
    return brief


def load_saved_outputs() -> tuple[dict[str, Any] | None, str]:
    """Load saved JSON and markdown output if they exist."""
    ideas_payload: dict[str, Any] | None = None
    brief = ""

    if PRODUCT_IDEAS_PATH.exists():
        try:
            ideas_payload = json.loads(PRODUCT_IDEAS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            ideas_payload = None

    if PRODUCT_BRIEF_PATH.exists():
        brief = PRODUCT_BRIEF_PATH.read_text(encoding="utf-8")

    return ideas_payload, brief
