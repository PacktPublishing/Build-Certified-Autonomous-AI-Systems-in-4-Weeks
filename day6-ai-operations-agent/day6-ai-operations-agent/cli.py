"""Command-line entry point for the Day 6 AI Operations Agent lab."""

from __future__ import annotations

import argparse
import json

from agent import run_operations_agent
from llm_service import OllamaError


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AI Operations Agent from the terminal.")
    parser.add_argument("request", nargs="*", help="The operations request to process.")
    args = parser.parse_args()

    user_request = " ".join(args.request).strip()
    if not user_request:
        user_request = input("What do you want the operations agent to do? ").strip()

    try:
        response = run_operations_agent(user_request)
    except OllamaError as exc:
        print(f"Ollama error: {exc}")
        return

    print("\nFinal answer")
    print("------------")
    print(response.final_answer)

    print("\nTool decision")
    print("-------------")
    print(json.dumps(response.decision, indent=2))

    print("\nTool result")
    print("-----------")
    print(json.dumps(response.tool_result, indent=2))


if __name__ == "__main__":
    main()
