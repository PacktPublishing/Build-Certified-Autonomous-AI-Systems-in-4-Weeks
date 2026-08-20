import argparse
import os
import time

from dotenv import load_dotenv

from action_handlers import run_action_handler
from event_loader import EventLoadError, load_inbox_events
from ollama_service import OLLAMA_MODEL, OllamaServiceError
from state_service import get_processed_event_ids, mark_event_processed
from workflow_router import route_event

load_dotenv()

WATCH_INTERVAL_SECONDS = int(os.getenv("WATCH_INTERVAL_SECONDS", "5"))


def process_inbox_once() -> int:
    processed_ids = get_processed_event_ids()
    events = load_inbox_events()
    new_events = [event for event in events if event.get("event_id") not in processed_ids]

    if not new_events:
        print("No new events found.")
        return 0

    print(f"Found {len(new_events)} new event(s).")

    for event in new_events:
        event_id = event.get("event_id", "unknown")
        subject = event.get("subject", "No subject")

        print("\n" + "=" * 80)
        print(f"Processing event: {event_id}")
        print(f"Subject: {subject}")

        action = route_event(event)
        print(f"Router selected action: {action}")

        output_file = run_action_handler(event, action)
        mark_event_processed(event, action, output_file)

        print(f"Output created: {output_file}")
        print(f"State updated for event: {event_id}")

    return len(new_events)


def watch_inbox() -> None:
    print("End-to-End AI Automation Workflow with Ollama")
    print(f"Using local Ollama model: {OLLAMA_MODEL}")
    print("Watching the inbox folder for JSON events.")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            process_inbox_once()
            print(f"\nWaiting {WATCH_INTERVAL_SECONDS} seconds before checking again...")
            time.sleep(WATCH_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\nWorkflow stopped by user.")
            break
        except EventLoadError as exc:
            print(f"\nEvent error: {exc}")
            time.sleep(WATCH_INTERVAL_SECONDS)
        except OllamaServiceError as exc:
            print(f"\nOllama error: {exc}")
            print("Troubleshooting:")
            print("1. Start Ollama: ollama serve")
            print("2. Pull the model: ollama pull llama3.2:1b")
            print("3. Run the workflow again: python main.py --once")
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Local event-driven AI workflow agent")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Process current inbox events once and then stop.",
    )
    args = parser.parse_args()

    if args.once:
        print("Running one inbox scan...")
        try:
            process_inbox_once()
        except (EventLoadError, OllamaServiceError) as exc:
            print(f"Error: {exc}")
        return

    watch_inbox()


if __name__ == "__main__":
    main()
