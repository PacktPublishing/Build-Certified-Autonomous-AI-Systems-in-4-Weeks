"""Validation helpers for the capstone lab."""

from __future__ import annotations


def clean_product_idea(product_idea: str) -> str:
    """Normalize user input before it reaches the agents."""
    return " ".join(product_idea.strip().split())


def validate_product_idea(product_idea: str) -> tuple[bool, list[str]]:
    """Validate the product idea and return a friendly list of issues."""
    issues: list[str] = []
    cleaned = clean_product_idea(product_idea)

    if not cleaned:
        issues.append("Enter a product idea before running the agents.")

    if cleaned and len(cleaned) < 20:
        issues.append("The product idea is too short. Add the target user and the problem it solves.")

    if len(cleaned) > 4000:
        issues.append("The product idea is too long. Keep it under 4,000 characters for this local demo.")

    return len(issues) == 0, issues
