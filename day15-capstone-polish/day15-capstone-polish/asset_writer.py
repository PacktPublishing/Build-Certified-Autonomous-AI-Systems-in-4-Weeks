import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OUTPUTS_DIR = Path(os.getenv("OUTPUTS_DIR", "outputs"))


def ensure_outputs_dir() -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)


def write_markdown_asset(file_name: str, content: str) -> Path:
    ensure_outputs_dir()
    output_path = OUTPUTS_DIR / file_name
    output_path.write_text(content.strip() + "\n", encoding="utf-8")
    return output_path


def list_expected_assets() -> list[str]:
    return [
        "readiness_checklist.md",
        "README_draft.md",
        "demo_script.md",
        "qa_prep.md",
    ]
