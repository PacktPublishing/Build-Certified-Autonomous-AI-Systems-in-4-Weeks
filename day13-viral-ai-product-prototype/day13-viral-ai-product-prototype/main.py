"""Command-line smoke demo for Day 13."""

from __future__ import annotations

import json

from idea_pipeline import generate_product_ideas


def main() -> None:
    result = generate_product_ideas(
        target_user="Busy course creators who need to turn rough lesson ideas into polished lab plans",
        painful_workflow="They have messy notes, scattered feature ideas, and no clear structure for what the student should build in the lab.",
        desired_output="A clear product brief with product name, target user, painful workflow, features, score, and capstone-ready plan.",
        use_llm=False,
        save_outputs=True,
    )
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
