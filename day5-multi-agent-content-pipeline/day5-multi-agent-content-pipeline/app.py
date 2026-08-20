"""Command-line app for the Day 5 multi-agent content pipeline."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from agents import build_markdown_report, run_content_pipeline
from llm_service import OllamaClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a multi-agent content pipeline with Ollama."
    )
    parser.add_argument(
        "--topic",
        help="Topic for the agent team to write about.",
    )
    parser.add_argument(
        "--model",
        help="Ollama model name. Defaults to OLLAMA_MODEL or llama3.2:3b.",
    )
    parser.add_argument(
        "--base-url",
        help="Ollama base URL. Defaults to OLLAMA_BASE_URL or http://localhost:11434.",
    )
    parser.add_argument(
        "--output",
        default="final_output.md",
        help="Markdown file where the final report will be saved.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the full app flow with sample content instead of calling Ollama.",
    )
    return parser.parse_args()


def get_topic(topic_arg: str | None) -> str:
    if topic_arg:
        return topic_arg.strip()

    topic = input("Enter a topic for the content team: ").strip()

    if not topic:
        raise ValueError("A topic is required to run the content pipeline.")

    return topic


def save_report(markdown: str, output_path: str) -> Path:
    path = Path(output_path)
    path.write_text(markdown, encoding="utf-8")
    return path


def main() -> None:
    load_dotenv()
    args = parse_args()

    topic = get_topic(args.topic)
    model = args.model or os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    base_url = args.base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    print("\nMulti-Agent Content Pipeline")
    print("=" * 36)
    print(f"Topic: {topic}")
    print(f"Model: {model}")

    client = OllamaClient(model=model, base_url=base_url)
    workspace = run_content_pipeline(topic=topic, client=client, dry_run=args.dry_run)

    markdown = build_markdown_report(workspace)
    saved_path = save_report(markdown, args.output)

    print("\nPipeline complete.")
    print(f"Saved output to: {saved_path.resolve()}")


if __name__ == "__main__":
    main()
