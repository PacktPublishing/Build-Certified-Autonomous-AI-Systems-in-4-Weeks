"""Ollama-backed smoke test for Day 13."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from idea_pipeline import generate_product_ideas  # noqa: E402


result = generate_product_ideas(
    target_user="Busy course creators who need to turn rough lesson ideas into polished lab plans",
    painful_workflow="They have messy notes, scattered feature ideas, and no clear structure for what the student should build in the lab.",
    desired_output="A clear product brief with product name, target user, painful workflow, features, score, and capstone-ready plan.",
    use_llm=True,
    save_outputs=True,
)

print(result.llm_status)
print(f"ideas={len(result.ideas)}")
print(f"best={result.best_idea.get('name') if result.best_idea else 'None'}")
print(f"saved={', '.join(result.saved_files)}")
