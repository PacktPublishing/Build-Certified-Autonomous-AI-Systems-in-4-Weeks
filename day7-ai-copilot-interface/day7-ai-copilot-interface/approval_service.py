"""Helpers for saving human-approved copilot output."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path("approved_outputs.md")


def save_approved_output(user_request: str, approved_text: str) -> Path:
    """Append one approved AI draft to the Markdown output file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"""

---

## Approved Output - {timestamp}

### User Request

{user_request.strip()}

### Approved Draft

{approved_text.strip()}
"""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("a", encoding="utf-8") as file:
        file.write(entry)

    return OUTPUT_FILE
