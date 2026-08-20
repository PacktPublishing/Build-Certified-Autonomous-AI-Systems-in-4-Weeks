"""Command-line smoke demo for the Day 11 lab.

This lets learners test the pipeline without opening Streamlit.
"""

from __future__ import annotations

import json

from pipeline import run_pipeline


DEMO_REQUEST = "A customer is angry about an invoice and wants a refund. Draft a careful email response."


def main() -> None:
    result = run_pipeline(
        request_text=DEMO_REQUEST,
        audience="Customer",
        channel="Email",
        use_llm=False,
    )
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
