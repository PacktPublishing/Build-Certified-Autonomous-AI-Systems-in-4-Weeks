"""Quick Ollama smoke test for the Day 14 capstone lab."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from ollama_service import OllamaService  # noqa: E402

llm = OllamaService()

if not llm.is_available():
    raise SystemExit("Ollama is not reachable. Start Ollama and try again.")

response = llm.generate(
    prompt="Reply with one short sentence confirming the capstone model is ready.",
    system_prompt="You are a concise local AI assistant.",
)

print(response)
