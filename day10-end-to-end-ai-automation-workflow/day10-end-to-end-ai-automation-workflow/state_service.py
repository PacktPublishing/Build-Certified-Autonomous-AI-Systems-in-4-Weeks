import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

STATE_FILE = Path(os.getenv("STATE_FILE", "state/processed_events.json"))


def load_processed_events() -> list[dict[str, Any]]:
    if not STATE_FILE.exists():
        return []

    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def get_processed_event_ids() -> set[str]:
    return {record["event_id"] for record in load_processed_events() if record.get("event_id")}


def mark_event_processed(event: dict[str, Any], action: str, output_file: str) -> None:
    STATE_FILE.parent.mkdir(exist_ok=True)
    history = load_processed_events()

    history.append(
        {
            "event_id": event.get("event_id"),
            "file_name": event.get("_file_name"),
            "action": action,
            "output_file": output_file,
            "processed_at": datetime.now().isoformat(timespec="seconds"),
        }
    )

    STATE_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")
