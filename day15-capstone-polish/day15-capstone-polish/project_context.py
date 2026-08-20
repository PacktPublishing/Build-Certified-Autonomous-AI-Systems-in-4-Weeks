import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

PROFILE_FILE = Path(os.getenv("CAPSTONE_PROFILE_FILE", "capstone_profile.json"))


class ProjectContextError(Exception):
    pass


def load_capstone_profile() -> dict[str, Any]:
    if not PROFILE_FILE.exists():
        raise ProjectContextError(f"Missing profile file: {PROFILE_FILE}")

    try:
        return json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProjectContextError(f"Invalid JSON in profile file: {PROFILE_FILE}") from exc


def format_profile_for_prompt(profile: dict[str, Any]) -> str:
    return json.dumps(profile, indent=2)
