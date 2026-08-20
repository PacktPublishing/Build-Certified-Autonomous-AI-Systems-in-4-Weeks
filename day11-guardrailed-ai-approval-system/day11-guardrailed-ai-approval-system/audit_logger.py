"""JSONL audit log for approval decisions."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AUDIT_LOG_PATH = Path("logs/audit_log.jsonl")


def save_audit_event(
    pipeline_result: dict[str, Any],
    decision: str,
    reviewer_name: str,
    reviewer_notes: str,
    log_path: Path = AUDIT_LOG_PATH,
) -> dict[str, Any]:
    """Append one approval decision to the audit log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "reviewer_name": reviewer_name.strip() or "Anonymous reviewer",
        "reviewer_notes": reviewer_notes.strip(),
        "pipeline_result": pipeline_result,
    }

    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")

    return event


def load_audit_events(log_path: Path = AUDIT_LOG_PATH, limit: int = 20) -> list[dict[str, Any]]:
    """Read recent audit events for display in the app."""
    if not log_path.exists():
        return []

    events: list[dict[str, Any]] = []
    with log_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return events[-limit:]
