"""File helpers for saving the generated final presentation assets."""

from __future__ import annotations

from pathlib import Path


OUTPUT_FILENAMES = {
    "final_demo_script": "final_demo_script.md",
    "judge_rubric": "judge_rubric.md",
    "launch_post": "launch_post.md",
    "improvement_plan": "improvement_plan.md",
}


def save_assets(assets: dict[str, str], output_dir: str | Path = "outputs") -> dict[str, Path]:
    """Save generated Markdown assets and return their file paths."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    saved_files: dict[str, Path] = {}

    for asset_key, content in assets.items():
        filename = OUTPUT_FILENAMES[asset_key]
        file_path = output_path / filename
        file_path.write_text(content.strip() + "\n", encoding="utf-8")
        saved_files[asset_key] = file_path

    return saved_files


def reset_outputs(output_dir: str | Path = "outputs") -> None:
    """Remove previously generated Markdown files from the output folder."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for filename in OUTPUT_FILENAMES.values():
        file_path = output_path / filename
        if file_path.exists():
            file_path.unlink()


def read_text_file(path: str | Path) -> str:
    """Read a text file using UTF-8."""
    return Path(path).read_text(encoding="utf-8")
