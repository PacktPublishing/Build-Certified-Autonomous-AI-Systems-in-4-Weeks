DRAFT_SYSTEM_PROMPT = """
You are a helpful AI assistant.
Your job is to write a clear first draft answer for a beginner.
Keep the answer practical, structured, and easy to understand.
""".strip()

CRITIQUE_SYSTEM_PROMPT = """
You are a careful reviewer.
Your job is to critique the draft answer.
Look for missing details, unclear wording, weak structure, and anything that may confuse a beginner.
Do not rewrite the answer yet. Only provide critique.
""".strip()

REVISION_SYSTEM_PROMPT = """
You are a helpful AI editor.
Your job is to revise the draft using the critique.
Make the final answer clearer, more complete, and easier for a beginner to understand.
""".strip()

SCORE_SYSTEM_PROMPT = """
You are a quality evaluator.
Score the final answer from 1 to 10.
Then give a short reason for the score.
Use this format:
Score: X/10
Reason: your reason here
""".strip()


def build_draft_prompt(user_question: str) -> str:
    return f"Write a helpful answer to this question:\n\n{user_question}"


def build_critique_prompt(user_question: str, draft_answer: str) -> str:
    return f"""
Original question:
{user_question}

Draft answer:
{draft_answer}

Critique the draft answer.
""".strip()


def build_revision_prompt(user_question: str, draft_answer: str, critique: str) -> str:
    return f"""
Original question:
{user_question}

Draft answer:
{draft_answer}

Critique:
{critique}

Rewrite the answer using the critique.
""".strip()


def build_score_prompt(user_question: str, final_answer: str) -> str:
    return f"""
Original question:
{user_question}

Final answer:
{final_answer}

Score the final answer.
""".strip()
