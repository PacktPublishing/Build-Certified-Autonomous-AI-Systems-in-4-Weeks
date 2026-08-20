import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

INBOX_DIR = Path(os.getenv("INBOX_DIR", "inbox"))


class EventLoadError(Exception):
    pass


def load_event_file(path: Path) -> dict[str, Any]:
    try:
        event = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise EventLoadError(f"Invalid JSON in {path.name}") from exc

    if not event.get("event_id"):
        event["event_id"] = path.stem

    return event


def load_inbox_events() -> list[dict[str, Any]]:
    INBOX_DIR.mkdir(exist_ok=True)

    events = []
    for path in sorted(INBOX_DIR.glob("*.json")):
        event = load_event_file(path)
        event["_file_name"] = path.name
        events.append(event)

    return events
