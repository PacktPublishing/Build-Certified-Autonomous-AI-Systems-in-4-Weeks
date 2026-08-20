import json
from datetime import datetime
from pathlib import Path
from typing import Any

HISTORY_FILE = Path("run_history.json")


def load_history() -> list[dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []

    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_run(
    user_question: str,
    draft_answer: str,
    critique: str,
    revised_answer: str,
    quality_score: str,
) -> None:
    history = load_history()

    run_record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user_question": user_question,
        "draft_answer": draft_answer,
        "critique": critique,
        "revised_answer": revised_answer,
        "quality_score": quality_score,
    }

    history.append(run_record)
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")
