ROUTER_SYSTEM_PROMPT = """
You are a workflow router for a local automation agent.
Choose exactly one action for the event.

Allowed actions:
- summary
- task_list
- escalation

Return only one word: summary, task_list, or escalation.
""".strip()

SUMMARY_SYSTEM_PROMPT = """
You are a business assistant.
Create a clear, beginner-friendly summary of the event.
Use short sections and simple language.
""".strip()

TASK_LIST_SYSTEM_PROMPT = """
You are a project assistant.
Turn the event into a practical task list.
Include owners if the event mentions them.
Use checkboxes.
""".strip()

ESCALATION_SYSTEM_PROMPT = """
You are an operations assistant.
Create an escalation note for a human team.
Explain the issue, urgency, recommended next step, and who should review it.
""".strip()


def build_router_prompt(event: dict) -> str:
    return f"""
Event source: {event.get("source", "unknown")}
Subject: {event.get("subject", "")}
Priority: {event.get("priority", "normal")}
Message: {event.get("message", "")}

Which action should handle this event?
""".strip()


def build_summary_prompt(event: dict) -> str:
    return f"""
Create a summary for this event.

Subject: {event.get("subject", "")}
Message: {event.get("message", "")}
Priority: {event.get("priority", "normal")}
""".strip()


def build_task_list_prompt(event: dict) -> str:
    return f"""
Create a task list from this event.

Subject: {event.get("subject", "")}
Message: {event.get("message", "")}
Priority: {event.get("priority", "normal")}
""".strip()


def build_escalation_prompt(event: dict) -> str:
    return f"""
Create an escalation note for this event.

Source: {event.get("source", "unknown")}
Subject: {event.get("subject", "")}
Message: {event.get("message", "")}
Priority: {event.get("priority", "normal")}
""".strip()
