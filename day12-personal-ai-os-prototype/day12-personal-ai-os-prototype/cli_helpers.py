import json
from typing import Any


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2))


def print_menu() -> None:
    print_header("Personal AI OS Prototype")
    print("1. View profile memory")
    print("2. Update profile memory")
    print("3. Add task")
    print("4. View tasks")
    print("5. Mark task as done")
    print("6. Add note")
    print("7. View notes")
    print("8. Run Planner Agent")
    print("9. Run Writer Agent")
    print("10. Run Reviewer Agent")
    print("11. Exit")


def ask_required(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")
