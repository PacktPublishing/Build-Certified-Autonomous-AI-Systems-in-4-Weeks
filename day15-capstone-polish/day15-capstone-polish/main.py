from asset_writer import list_expected_assets, write_markdown_asset
from ollama_service import OLLAMA_MODEL, OllamaServiceError, call_ollama
from project_context import ProjectContextError, format_profile_for_prompt, load_capstone_profile
from prompt_templates import (
    ASSET_SYSTEM_PROMPT,
    build_demo_script_prompt,
    build_qa_prep_prompt,
    build_readiness_checklist_prompt,
    build_readme_draft_prompt,
)


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def generate_asset(file_name: str, prompt: str) -> str:
    print(f"Generating {file_name}...")
    content = call_ollama(prompt=prompt, system_prompt=ASSET_SYSTEM_PROMPT)
    output_path = write_markdown_asset(file_name, content)
    print(f"Created: {output_path}")
    return str(output_path)


def generate_all_assets() -> list[str]:
    profile = load_capstone_profile()
    profile_text = format_profile_for_prompt(profile)

    jobs = [
        ("readiness_checklist.md", build_readiness_checklist_prompt(profile_text)),
        ("README_draft.md", build_readme_draft_prompt(profile_text)),
        ("demo_script.md", build_demo_script_prompt(profile_text)),
        ("qa_prep.md", build_qa_prep_prompt(profile_text)),
    ]

    created_files = []
    for file_name, prompt in jobs:
        created_files.append(generate_asset(file_name, prompt))

    return created_files


def main() -> None:
    print_header("Day 15 Capstone Deployment and Portfolio Polish")
    print(f"Using local Ollama model: {OLLAMA_MODEL}")
    print("This app generates production-readiness assets for the final capstone.")

    print_header("Expected Outputs")
    for asset in list_expected_assets():
        print(f"- outputs/{asset}")

    try:
        created_files = generate_all_assets()
    except ProjectContextError as exc:
        print(f"\nProject context error: {exc}")
        print("Check capstone_profile.json and run again.")
        return
    except OllamaServiceError as exc:
        print(f"\nOllama error: {exc}")
        print("Troubleshooting:")
        print("1. Start Ollama: ollama serve")
        print("2. Pull the model: ollama pull llama3.2:1b")
        print("3. Run again: python main.py")
        return

    print_header("Done")
    print("Generated files:")
    for file_path in created_files:
        print(f"- {file_path}")

    print("\nNext step: open the Markdown files, review them, and customize details before using them in a portfolio.")


if __name__ == "__main__":
    main()
