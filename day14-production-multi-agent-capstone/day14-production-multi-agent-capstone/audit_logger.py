"""Audit logging for the multi-agent capstone."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def utc_timestamp() -> str:
    """Return a stable timestamp for logs and filenames."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_filename(text: str, fallback: str = "capstone_run") -> str:
    """Create a small filename-safe slug from user text."""
    allowed = []
    for character in text.lower():
        if character.isalnum():
            allowed.append(character)
        elif character in {" ", "-", "_"}:
            allowed.append("-")

    slug = "".join(allowed).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")

    return (slug or fallback)[:60]


class AuditLogger:
    """Writes JSONL audit events and markdown reports."""

    def __init__(self, log_path: str | None = None, output_dir: str | None = None):
        self.log_path = Path(log_path or os.getenv("AUDIT_LOG_PATH", "logs/capstone_audit.jsonl"))
        self.output_dir = Path(output_dir or os.getenv("OUTPUT_DIR", "outputs"))
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def record_run(self, run_data: dict) -> str:
        """Append one completed run to the JSONL audit log."""
        event_id = f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        audit_event = {
            "event_id": event_id,
            "created_at": utc_timestamp(),
            **run_data,
        }

        with self.log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(audit_event, ensure_ascii=False) + "\n")

        return event_id

    def save_markdown_report(self, run_data: dict, event_id: str) -> str:
        """Save a human-readable markdown report for the latest run."""
        product_idea = run_data.get("product_idea", "capstone run")
        filename = f"{event_id}_{safe_filename(product_idea)}.md"
        report_path = self.output_dir / filename

        markdown = f"""# Production Multi-Agent Capstone Report

**Event ID:** {event_id}  
**Created At:** {utc_timestamp()}  
**Model:** {run_data.get('model', 'unknown')}

## Product Idea

{product_idea}

## Planner Agent Output

{run_data.get('planner_output', '')}

## Builder Agent Output

{run_data.get('builder_output', '')}

## Reviewer Agent Output

{run_data.get('reviewer_output', '')}
"""

        report_path.write_text(markdown, encoding="utf-8")
        return str(report_path)
