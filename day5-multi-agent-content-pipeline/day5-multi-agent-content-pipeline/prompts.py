"""Prompt templates for the Day 5 multi-agent content pipeline."""

PLANNER_SYSTEM_PROMPT = """You are the Planner Agent.
Your job is to create a clear content plan before anything is written.
Keep the plan practical, beginner-friendly, and easy for the Writer Agent to follow.
"""

WRITER_SYSTEM_PROMPT = """You are the Writer Agent.
Your job is to turn a content plan into a clear first draft.
Write in a polished, friendly, practical style.
Use headings and short paragraphs.
"""

REVIEWER_SYSTEM_PROMPT = """You are the Reviewer Agent.
Your job is to critique the draft and ask for specific improvements.
Be constructive, direct, and useful.
Focus on clarity, structure, completeness, and reader value.
"""

FINAL_WRITER_SYSTEM_PROMPT = """You are the Writer Agent doing the final writer pass.
Your job is to improve the draft using the review notes.
Return the final polished content only.
Use clean Markdown formatting.
"""


def build_planner_prompt(topic: str) -> str:
    return f"""
Create a content plan for this topic:

Topic: {topic}

Return:
1. Working title
2. Target reader
3. Key message
4. Section outline
5. Tone and style guidance
""".strip()


def build_writer_prompt(topic: str, plan: str) -> str:
    return f"""
Write a first draft using the content plan below.

Topic:
{topic}

Content plan:
{plan}

Requirements:
- Use Markdown
- Include a title
- Use clear headings
- Keep the writing practical and beginner-friendly
""".strip()


def build_reviewer_prompt(topic: str, plan: str, draft: str) -> str:
    return f"""
Review the first draft and ask for improvements.

Topic:
{topic}

Content plan:
{plan}

First draft:
{draft}

Return:
1. What works well
2. What needs improvement
3. Specific revision instructions for the final writer pass
""".strip()


def build_final_writer_prompt(topic: str, plan: str, draft: str, review: str) -> str:
    return f"""
Create the final polished content using the original plan, first draft, and review notes.

Topic:
{topic}

Content plan:
{plan}

First draft:
{draft}

Reviewer feedback:
{review}

Return the final Markdown content only.
""".strip()
