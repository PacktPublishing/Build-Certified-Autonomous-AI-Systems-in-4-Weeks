import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
PROFILE_FILE = DATA_DIR / "profile.json"
TASKS_FILE = DATA_DIR / "tasks.json"
NOTES_FILE = DATA_DIR / "notes.json"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_profile() -> dict[str, Any]:
    return read_json(PROFILE_FILE, {})


def save_profile(profile: dict[str, Any]) -> None:
    write_json(PROFILE_FILE, profile)


def update_profile_field(field: str, value: str) -> dict[str, Any]:
    profile = load_profile()

    if field in {"goals", "preferences"}:
        current_values = profile.get(field, [])
        if not isinstance(current_values, list):
            current_values = []
        current_values.append(value)
        profile[field] = current_values
    else:
        profile[field] = value

    save_profile(profile)
    return profile


def load_tasks() -> list[dict[str, Any]]:
    return read_json(TASKS_FILE, [])


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    write_json(TASKS_FILE, tasks)


def add_task(title: str) -> dict[str, Any]:
    tasks = load_tasks()
    next_id = max([task.get("id", 0) for task in tasks], default=0) + 1
    task = {"id": next_id, "title": title, "status": "open"}
    tasks.append(task)
    save_tasks(tasks)
    return task


def complete_task(task_id: int) -> bool:
    tasks = load_tasks()

    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = "done"
            save_tasks(tasks)
            return True

    return False


def load_notes() -> list[dict[str, Any]]:
    return read_json(NOTES_FILE, [])


def save_notes(notes: list[dict[str, Any]]) -> None:
    write_json(NOTES_FILE, notes)


def add_note(title: str, content: str) -> dict[str, Any]:
    notes = load_notes()
    next_id = max([note.get("id", 0) for note in notes], default=0) + 1
    note = {"id": next_id, "title": title, "content": content}
    notes.append(note)
    save_notes(notes)
    return note


def build_memory_context() -> str:
    profile = load_profile()
    tasks = load_tasks()
    notes = load_notes()

    return f"""
PROFILE MEMORY:
{json.dumps(profile, indent=2)}

TASK MEMORY:
{json.dumps(tasks, indent=2)}

NOTES MEMORY:
{json.dumps(notes, indent=2)}
""".strip()
