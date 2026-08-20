"""Command-line entry point for the Day 14 capstone lab."""

from __future__ import annotations

import argparse
from pathlib import Path

from capstone_pipeline import CapstonePipeline

DEFAULT_IDEA = """
An AI study planner for busy working professionals. The user enters their goal,
available time, and deadline. The app creates a weekly study plan, identifies
risks, and recommends a realistic first milestone.
""".strip()


def load_product_idea(args: argparse.Namespace) -> str:
    """Load a product idea from an argument, a file, or the built-in sample."""
    if args.idea:
        return args.idea

    if args.file:
        return Path(args.file).read_text(encoding="utf-8")

    return DEFAULT_IDEA


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Day 14 multi-agent capstone.")
    parser.add_argument("--idea", help="Product idea to send through the agents.")
    parser.add_argument("--file", help="Path to a text file containing the product idea.")
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Run the agents without writing a markdown report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    product_idea = load_product_idea(args)

    pipeline = CapstonePipeline()
    result = pipeline.run(product_idea=product_idea, save_report=not args.no_report)

    print("\n=== Planner Agent ===\n")
    print(result.planner_output)

    print("\n=== Builder Agent ===\n")
    print(result.builder_output)

    print("\n=== Reviewer Agent ===\n")
    print(result.reviewer_output)

    print("\n=== Audit ===")
    print(f"Event ID: {result.audit_event_id}")
    if result.report_path:
        print(f"Report saved to: {result.report_path}")


if __name__ == "__main__":
    main()
