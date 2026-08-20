from history_service import save_run
from ollama_service import OLLAMA_MODEL, OllamaServiceError, call_ollama
from prompt_templates import (
    CRITIQUE_SYSTEM_PROMPT,
    DRAFT_SYSTEM_PROMPT,
    REVISION_SYSTEM_PROMPT,
    SCORE_SYSTEM_PROMPT,
    build_critique_prompt,
    build_draft_prompt,
    build_revision_prompt,
    build_score_prompt,
)


def print_section(title: str, content: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(content)


def run_reflective_agent(user_question: str) -> None:
    print(f"\nUsing local Ollama model: {OLLAMA_MODEL}")

    print("\nStep 1: Drafting initial answer...")
    draft_answer = call_ollama(
        prompt=build_draft_prompt(user_question),
        system_prompt=DRAFT_SYSTEM_PROMPT,
    )
    print_section("DRAFT ANSWER", draft_answer)

    print("\nStep 2: Critiquing the draft...")
    critique = call_ollama(
        prompt=build_critique_prompt(user_question, draft_answer),
        system_prompt=CRITIQUE_SYSTEM_PROMPT,
    )
    print_section("CRITIQUE", critique)

    print("\nStep 3: Revising the answer...")
    revised_answer = call_ollama(
        prompt=build_revision_prompt(user_question, draft_answer, critique),
        system_prompt=REVISION_SYSTEM_PROMPT,
    )
    print_section("REVISED ANSWER", revised_answer)

    print("\nStep 4: Scoring the final answer...")
    quality_score = call_ollama(
        prompt=build_score_prompt(user_question, revised_answer),
        system_prompt=SCORE_SYSTEM_PROMPT,
    )
    print_section("QUALITY SCORE", quality_score)

    save_run(
        user_question=user_question,
        draft_answer=draft_answer,
        critique=critique,
        revised_answer=revised_answer,
        quality_score=quality_score,
    )

    print("\nRun saved to run_history.json")


def main() -> None:
    print("Self-Reflective AI Agent with Ollama")
    print("This agent drafts, critiques, revises, and scores its own answer.")

    user_question = input("\nEnter your question: ").strip()

    if not user_question:
        print("No question entered. Please run the app again and type a question.")
        return

    try:
        run_reflective_agent(user_question)
    except OllamaServiceError as exc:
        print(f"\nError: {exc}")
        print("\nTroubleshooting:")
        print("1. Start Ollama: ollama serve")
        print("2. Pull the model: ollama pull llama3.2:1b")
        print("3. Run the app again: python main.py")


if __name__ == "__main__":
    main()
