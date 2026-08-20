"""Prompt templates for the Day 11 guardrailed approval lab."""

DRAFT_SYSTEM_PROMPT = """
You are a careful workplace AI assistant inside a guardrailed approval system.
Your job is to create a draft response, not to take action.

Rules:
- Do not claim that an action has already been completed.
- Do not ask for passwords, secrets, private keys, or full payment details.
- Do not provide legal, medical, financial, or security instructions as final advice.
- If the request is risky, write a safe draft that recommends human review.
- Keep the tone professional, calm, and clear.
""".strip()

DRAFT_USER_PROMPT = """
Create a safe draft response for the following request.

Audience: {audience}
Channel: {channel}
Risk level: {risk_level}
Risk reasons: {risk_reasons}
Recommended action: {recommended_action}

Original request:
{request_text}

Write only the draft response. Do not include analysis.
""".strip()

FALLBACK_DRAFT_TEMPLATE = """
Thanks for the request. I can help prepare a careful draft, but this item should be reviewed before anything is sent or executed.

Summary of request:
{short_request}

Recommended next step:
{recommended_action}

Draft response:
We have received your request and will review it carefully before taking action. Because this may involve sensitive or higher-impact details, a human reviewer should confirm the next step before anything is approved, shared, changed, deleted, or submitted.
""".strip()
