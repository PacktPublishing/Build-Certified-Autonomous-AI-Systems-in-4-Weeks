"""Deterministic guardrails for the Day 11 approval lab.

These checks are intentionally simple and readable for learners.
In production, each rule would be tested, versioned, monitored, and reviewed.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass


SECRET_PATTERNS = {
    "possible API key": r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*[a-z0-9_\-]{12,}",
    "possible private key": r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----",
    "possible credit card number": r"\b(?:\d[ -]*?){13,16}\b",
    "possible SSN": r"\b\d{3}-\d{2}-\d{4}\b",
}

HIGH_RISK_KEYWORDS = {
    "delete user data",
    "delete records",
    "production database",
    "password",
    "private key",
    "api key",
    "access token",
    "credit card",
    "ssn",
    "social security",
    "bank account",
    "lawsuit",
    "legal advice",
    "medical advice",
    "diagnosis",
    "investment advice",
    "fire employee",
    "terminate employee",
    "security vulnerability",
    "bypass",
    "disable logging",
}

MEDIUM_RISK_KEYWORDS = {
    "refund",
    "discount",
    "complaint",
    "angry customer",
    "contract",
    "invoice",
    "pricing",
    "policy exception",
    "sensitive",
    "customer data",
    "personal data",
    "approval",
    "manager",
    "escalate",
}

BLOCKED_OUTPUT_PHRASES = {
    "your password is",
    "send me your password",
    "share your password",
    "guaranteed result",
    "100% guaranteed",
    "i have deleted",
    "i have approved",
    "i have transferred",
    "ignore the policy",
    "bypass approval",
}


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]
    warnings: list[str]
    detected_sensitive_items: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RiskAssessment:
    risk_level: str
    score: int
    reasons: list[str]
    matched_terms: list[str]
    recommended_action: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OutputCheckResult:
    passed: bool
    issues: list[str]
    warnings: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def find_sensitive_items(text: str) -> list[str]:
    """Detect obvious secrets or regulated identifiers in plain text."""
    matches: list[str] = []
    for label, pattern in SECRET_PATTERNS.items():
        if re.search(pattern, text):
            matches.append(label)
    return matches


def validate_request(request_text: str, audience: str, channel: str) -> ValidationResult:
    """Validate user input before the LLM sees it."""
    errors: list[str] = []
    warnings: list[str] = []

    cleaned_request = request_text.strip()
    cleaned_audience = audience.strip()
    cleaned_channel = channel.strip()

    if not cleaned_request:
        errors.append("Request text is required.")
    elif len(cleaned_request) < 10:
        errors.append("Request text is too short. Add enough context for a safe draft.")

    if len(cleaned_request) > 2500:
        errors.append("Request text is too long for this beginner lab. Keep it under 2,500 characters.")

    if not cleaned_audience:
        errors.append("Audience is required.")

    if not cleaned_channel:
        errors.append("Channel is required.")

    sensitive_items = find_sensitive_items(cleaned_request)
    if sensitive_items:
        warnings.append("The request appears to include sensitive data. Review carefully before sending to the model.")

    if "urgent" in cleaned_request.lower() or "immediately" in cleaned_request.lower():
        warnings.append("Urgency language detected. Do not skip approval just because the request sounds urgent.")

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=warnings,
        detected_sensitive_items=sensitive_items,
    )


def _matched_keywords(text: str, keywords: set[str]) -> list[str]:
    lower_text = text.lower()
    return sorted(keyword for keyword in keywords if keyword in lower_text)


def classify_risk(request_text: str) -> RiskAssessment:
    """Classify request risk using transparent rules."""
    high_matches = _matched_keywords(request_text, HIGH_RISK_KEYWORDS)
    medium_matches = _matched_keywords(request_text, MEDIUM_RISK_KEYWORDS)
    sensitive_items = find_sensitive_items(request_text)

    score = 0
    reasons: list[str] = []
    matched_terms: list[str] = []

    if high_matches:
        score += 70
        matched_terms.extend(high_matches)
        reasons.append("High-risk keyword or workflow detected.")

    if medium_matches:
        score += 30
        matched_terms.extend(medium_matches)
        reasons.append("Medium-risk business or customer-impact keyword detected.")

    if sensitive_items:
        score += 80
        matched_terms.extend(sensitive_items)
        reasons.append("Possible secret, payment detail, or regulated identifier detected.")

    score = min(score, 100)

    if score >= 70:
        risk_level = "HIGH"
        recommended_action = "Escalate to a human owner before sending or taking action. Draft may only acknowledge and route the request."
    elif score >= 30:
        risk_level = "MEDIUM"
        recommended_action = "Create a cautious draft and require human approval before sending."
    else:
        risk_level = "LOW"
        recommended_action = "Create a draft, run output checks, and still capture approval for the audit trail."

    if not reasons:
        reasons.append("No obvious sensitive or high-impact terms were detected by the beginner guardrail rules.")

    return RiskAssessment(
        risk_level=risk_level,
        score=score,
        reasons=reasons,
        matched_terms=matched_terms,
        recommended_action=recommended_action,
    )


def check_output(draft: str, risk: RiskAssessment) -> OutputCheckResult:
    """Run safety checks on the model draft before human approval."""
    issues: list[str] = []
    warnings: list[str] = []
    lower_draft = draft.lower()

    if not draft.strip():
        issues.append("Draft is empty.")

    if len(draft) > 2200:
        warnings.append("Draft is long. A reviewer may want a shorter response.")

    blocked = sorted(phrase for phrase in BLOCKED_OUTPUT_PHRASES if phrase in lower_draft)
    for phrase in blocked:
        issues.append(f"Draft contains blocked phrase: {phrase}")

    leaked_sensitive_items = find_sensitive_items(draft)
    for item in leaked_sensitive_items:
        issues.append(f"Draft may contain sensitive data: {item}")

    if risk.risk_level == "HIGH":
        escalation_words = ["review", "approve", "approval", "escalate", "human"]
        if not any(word in lower_draft for word in escalation_words):
            issues.append("High-risk draft must clearly mention human review or approval.")

    if risk.risk_level == "MEDIUM" and "approval" not in lower_draft and "review" not in lower_draft:
        warnings.append("Medium-risk draft should usually mention review or approval.")

    return OutputCheckResult(passed=not issues, issues=issues, warnings=warnings)
