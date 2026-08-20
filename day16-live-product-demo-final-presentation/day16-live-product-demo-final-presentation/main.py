"""CLI entry point for generating the Day 16 final presentation assets."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from file_writer import save_assets
from ollama_service import OllamaService
from presentation_pipeline import ProductDemoContext, generate_presentation_assets


load_dotenv()

PROJECT_DIR = Path(__file__).parent
DEFAULT_SAMPLE_PATH = PROJECT_DIR / "samples" / "sample_product_brief.md"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "outputs"


def parse_args() -> argparse.Namespace:
    """Read command-line options for the demo generator."""
    parser = argparse.ArgumentParser(
        description="Generate final demo presentation assets with local Ollama."
    )
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "llama3.2"))
    parser.add_argument(
        "--base-url",
        default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )
    parser.add_argument("--product-name", default="StudySprint AI")
    parser.add_argument(
        "--one-line-idea",
        default="An AI study coach that turns one topic into a study plan, quiz, and improvement checklist.",
    )
    parser.add_argument(
        "--target-user",
        default="Busy beginners who want a focused way to study one topic at a time.",
    )
    parser.add_argument(
        "--problem",
        default="Learners often do not know where to start, what to practice, or how to judge whether they understood the topic.",
    )
    parser.add_argument(
        "--built-features",
        default="Topic input, study plan generator, quiz generator, feedback suggestions, and Markdown export.",
    )
    parser.add_argument(
        "--demo-flow",
        default="Open the app, enter a topic, generate a study plan, generate quiz questions, review feedback, and export the guide.",
    )
    parser.add_argument(
        "--strongest-demo-moment",
        default="The app turns one small topic into a complete learning package in seconds.",
    )
    parser.add_argument(
        "--known-weak-spots",
        default="The first version does not track long-term progress yet, and the quiz difficulty is basic.",
    )
    parser.add_argument(
        "--launch-goal",
        default="Share the app with early learners, collect feedback, and decide what to improve in the next version.",
    )
    parser.add_argument(
        "--brief-file",
        default=str(DEFAULT_SAMPLE_PATH),
        help="Optional Markdown file with extra product details.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Folder where the generated Markdown files should be saved.",
    )
    return parser.parse_args()


def main() -> None:
    """Generate the four final presentation files."""
    args = parse_args()
    brief_path = Path(args.brief_file)
    extra_notes = ""

    if brief_path.exists():
        extra_notes = brief_path.read_text(encoding="utf-8")

    context = ProductDemoContext(
        product_name=args.product_name,
        one_line_idea=args.one_line_idea,
        target_user=args.target_user,
        problem=args.problem,
        built_features=args.built_features,
        demo_flow=args.demo_flow,
        strongest_demo_moment=args.strongest_demo_moment,
        known_weak_spots=args.known_weak_spots,
        launch_goal=args.launch_goal,
        extra_notes=extra_notes,
    )

    ollama = OllamaService(model=args.model, base_url=args.base_url)

    print("Generating final presentation assets with Ollama...")
    assets = generate_presentation_assets(context=context, ollama=ollama)
    saved_files = save_assets(assets, output_dir=args.output_dir)

    print("\nDone. Files created:")
    for path in saved_files.values():
        print(f"- {path}")


if __name__ == "__main__":
    main()
