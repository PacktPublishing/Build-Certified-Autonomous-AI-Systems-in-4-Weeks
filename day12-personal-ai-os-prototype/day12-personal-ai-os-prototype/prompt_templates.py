PLANNER_SYSTEM_PROMPT = """
You are the Planner Agent inside a local Personal AI OS.
Use the user's profile, tasks, and notes to create a practical plan.
Keep the plan clear, realistic, and beginner-friendly.
""".strip()

WRITER_SYSTEM_PROMPT = """
You are the Writer Agent inside a local Personal AI OS.
Use the user's memory to draft clear written content.
Write in a simple, helpful, and polished style.
""".strip()

REVIEWER_SYSTEM_PROMPT = """
You are the Reviewer Agent inside a local Personal AI OS.
Review the user's content for clarity, completeness, tone, and next-step usefulness.
Give practical feedback and a short improved version when helpful.
""".strip()


def build_planner_prompt(memory_context: str, user_request: str) -> str:
    return f"""
Here is the user's saved memory:

{memory_context}

User request:
{user_request}

Create a practical plan using the saved memory.
""".strip()


def build_writer_prompt(memory_context: str, user_request: str) -> str:
    return f"""
Here is the user's saved memory:

{memory_context}

Writing request:
{user_request}

Draft the requested content.
""".strip()


def build_reviewer_prompt(memory_context: str, content_to_review: str) -> str:
    return f"""
Here is the user's saved memory:

{memory_context}

Content to review:
{content_to_review}

Review this content and suggest improvements.
""".strip()
