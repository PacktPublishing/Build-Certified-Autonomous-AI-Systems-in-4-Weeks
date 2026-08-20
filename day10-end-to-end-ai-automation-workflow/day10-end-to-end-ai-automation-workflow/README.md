# Day 10 Lab — End-to-End AI Automation Workflow with Ollama

## Goal

In this lab, we build a local event-driven workflow agent.

The agent watches an inbox folder, reads JSON events, decides what to do, creates output files, and remembers which events were already processed.

## What learners will build

- A local event inbox
- A workflow router powered by Ollama
- Action handlers for summary, task list, and escalation
- Output files
- State tracking so events are not repeated

## Local LLM provider

This lab uses Ollama locally with:

```text
llama3.2:1b
```

No paid API key is required.

## Final workflow

```text
JSON event appears in inbox/
  -> Python loads the event
  -> State service checks if it was already processed
  -> Ollama router chooses an action
  -> Action handler creates an output file
  -> State file remembers the processed event
```

## Project structure

```text
day10-end-to-end-ai-automation-workflow/
├── inbox/
│   ├── event_001_summary.json
│   ├── event_002_task_list.json
│   └── event_003_escalation.json
├── outputs/
│   └── .gitkeep
├── scripts/
│   ├── reset_demo.sh
│   └── run_demo.sh
├── state/
│   └── processed_events.json
├── .env.example
├── .gitignore
├── action_handlers.py
├── event_loader.py
├── main.py
├── ollama_service.py
├── prompt_templates.py
├── README.md
├── requirements.txt
├── state_service.py
└── workflow_router.py
```

## File overview

### `README.md`

Explains the lab goal, setup steps, run commands, and project architecture.

### `requirements.txt`

Lists the Python packages needed for the project.

### `.env.example`

Shows the environment variables used by the workflow.

### `inbox/`

This folder acts like a local event inbox.

Each JSON file is one event waiting to be processed.

### `event_loader.py`

Loads JSON files from the inbox folder and turns them into Python dictionaries.

### `state_service.py`

Keeps track of processed events in `state/processed_events.json`.

This prevents the same event from being processed again and again.

### `prompt_templates.py`

Stores the prompts for the router and action handlers.

### `ollama_service.py`

Connects Python to the local Ollama model.

### `workflow_router.py`

Asks Ollama which action should handle the event.

Allowed actions are:

```text
summary
task_list
escalation
```

### `action_handlers.py`

Runs the selected action and creates a Markdown output file.

### `main.py`

Coordinates the full workflow.

It can run once or keep watching the inbox folder.

### `outputs/`

Generated Markdown files are written here.

### `scripts/run_demo.sh`

Runs the workflow once.

### `scripts/reset_demo.sh`

Clears generated outputs and resets the processed-event state.

## Setup

### 1. Go to the project folder

```bash
cd /Users/arjunvaid/Desktop/4_weeks/day10-end-to-end-ai-automation-workflow
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

On Mac:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install requests python-dotenv
```

Optional, after installing:

```bash
pip freeze > requirements.txt
```

### 5. Copy the environment file

```bash
cp .env.example .env
```

### 6. Start Ollama

In another terminal:

```bash
ollama serve
```

If Ollama is already running, you may see a message that the port is already in use. That is okay.

### 7. Pull the model

```bash
ollama pull llama3.2:1b
```

## Run the workflow once

This is best for a beginner demo.

```bash
python main.py --once
```

Or:

```bash
./scripts/run_demo.sh
```

The app will:

1. Read events from `inbox/`
2. Skip events already listed in `state/processed_events.json`
3. Ask Ollama to choose the right action
4. Create output files in `outputs/`
5. Update the processed-event state

## Watch the inbox continuously

```bash
python main.py
```

This keeps checking the inbox folder every few seconds.

Stop it with:

```text
Ctrl+C
```

## Reset the demo

If you want to rerun the same sample events:

```bash
./scripts/reset_demo.sh
```

This clears generated output files and resets `state/processed_events.json`.

## Sample event shape

```json
{
  "event_id": "event_001_summary",
  "source": "customer_email",
  "subject": "Customer feedback about onboarding",
  "message": "A customer said the onboarding steps are confusing.",
  "priority": "normal",
  "created_at": "2026-06-24T09:00:00"
}
```

## Beginner explanation

Think of this project like a small office assistant.

New messages arrive in the inbox.
The assistant reads each message, decides what kind of work is needed, performs that work, saves the result, and marks the message as done.

That is the core idea behind many real automation systems.

## Troubleshooting

### Error: Could not connect to Ollama

Start Ollama:

```bash
ollama serve
```

### Error: Model not found

Pull the model:

```bash
ollama pull llama3.2:1b
```

### Nothing happens when I run the workflow

Check `state/processed_events.json`.

If the events are already marked as processed, reset the demo:

```bash
./scripts/reset_demo.sh
```

Then run again:

```bash
python main.py --once
```
