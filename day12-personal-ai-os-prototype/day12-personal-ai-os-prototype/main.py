import argparse

from agents import run_planner_agent, run_reviewer_agent, run_writer_agent
from cli_helpers import ask_required, print_header, print_json, print_menu
from memory_store import (
    add_note,
    add_task,
    complete_task,
    load_notes,
    load_profile,
    load_tasks,
    update_profile_field,
)
from ollama_service import OLLAMA_MODEL, OllamaServiceError


def view_profile() -> None:
    print_header("Profile Memory")
    print_json(load_profile())


def update_profile() -> None:
    print_header("Update Profile Memory")
    print("Fields you can update: name, role, goals, preferences")
    field = ask_required("Field name: ")
    value = ask_required("Value to save: ")
    profile = update_profile_field(field, value)
    print("\nProfile updated.")
    print_json(profile)


def add_new_task() -> None:
    print_header("Add Task")
    title = ask_required("Task title: ")
    task = add_task(title)
    print("\nTask added.")
    print_json(task)


def view_tasks() -> None:
    print_header("Task Memory")
    tasks = load_tasks()
    if not tasks:
        print("No tasks saved yet.")
        return
    print_json(tasks)


def mark_task_done() -> None:
    print_header("Mark Task as Done")
    view_tasks()
    raw_task_id = ask_required("Task ID to mark done: ")

    try:
        task_id = int(raw_task_id)
    except ValueError:
        print("Please enter a valid number.")
        return

    if complete_task(task_id):
        print("Task marked as done.")
    else:
        print("Task not found.")


def add_new_note() -> None:
    print_header("Add Note")
    title = ask_required("Note title: ")
    content = ask_required("Note content: ")
    note = add_note(title, content)
    print("\nNote added.")
    print_json(note)


def view_notes() -> None:
    print_header("Notes Memory")
    notes = load_notes()
    if not notes:
        print("No notes saved yet.")
        return
    print_json(notes)


def planner_agent_flow() -> None:
    print_header("Planner Agent")
    request = ask_required("What should the planner help with? ")
    result = run_planner_agent(request)
    print_header("Planner Agent Result")
    print(result)


def writer_agent_flow() -> None:
    print_header("Writer Agent")
    request = ask_required("What should the writer draft? ")
    result = run_writer_agent(request)
    print_header("Writer Agent Result")
    print(result)


def reviewer_agent_flow() -> None:
    print_header("Reviewer Agent")
    content = ask_required("Paste the content to review: ")
    result = run_reviewer_agent(content)
    print_header("Reviewer Agent Result")
    print(result)


def run_demo() -> None:
    print_header("Demo Mode")
    print(f"Using local Ollama model: {OLLAMA_MODEL}")

    planner_request = "Create a simple plan for finishing this AI OS lab today."
    writer_request = "Write a short friendly note explaining what this Personal AI OS does."
    review_content = "This app stores memory and has agents. It is useful."

    print_header("Planner Demo")
    print(run_planner_agent(planner_request))

    print_header("Writer Demo")
    print(run_writer_agent(writer_request))

    print_header("Reviewer Demo")
    print(run_reviewer_agent(review_content))


def run_menu() -> None:
    print(f"Using local Ollama model: {OLLAMA_MODEL}")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                view_profile()
            elif choice == "2":
                update_profile()
            elif choice == "3":
                add_new_task()
            elif choice == "4":
                view_tasks()
            elif choice == "5":
                mark_task_done()
            elif choice == "6":
                add_new_note()
            elif choice == "7":
                view_notes()
            elif choice == "8":
                planner_agent_flow()
            elif choice == "9":
                writer_agent_flow()
            elif choice == "10":
                reviewer_agent_flow()
            elif choice == "11":
                print("Goodbye.")
                break
            else:
                print("Please choose a valid option.")
        except OllamaServiceError as exc:
            print(f"\nOllama error: {exc}")
            print("Troubleshooting:")
            print("1. Start Ollama: ollama serve")
            print("2. Pull the model: ollama pull llama3.2:1b")
            print("3. Try the menu option again.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local Personal AI OS prototype")
    parser.add_argument("--demo", action="store_true", help="Run a short non-interactive demo.")
    args = parser.parse_args()

    if args.demo:
        try:
            run_demo()
        except OllamaServiceError as exc:
            print(f"Ollama error: {exc}")
        return

    run_menu()


if __name__ == "__main__":
    main()
