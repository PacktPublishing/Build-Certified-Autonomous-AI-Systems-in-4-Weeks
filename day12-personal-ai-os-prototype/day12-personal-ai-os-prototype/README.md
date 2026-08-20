# Day 12 Lab - Personal AI OS Prototype with Ollama

## Goal

Build a local command-line Personal AI OS prototype with memory, tasks, notes, and small specialist agents.

## What you will build

- Command-line AI OS
- Persistent profile memory
- Task memory
- Notes memory
- Planner agent
- Writer agent
- Reviewer agent

## Local model

This lab uses Ollama locally with llama3.2:1b.

No paid API key is required.

## Architecture

```text
User in terminal
  -> AI OS menu
  -> JSON memory files in data/
  -> Specialist agent
  -> Ollama local model
  -> Response in terminal
```

## Project structure

```text
day12-personal-ai-os-prototype/
├── data/
│   ├── notes.json
│   ├── profile.json
│   └── tasks.json
├── scripts/
│   ├── reset_demo.sh
│   ├── run_app.sh
│   └── run_demo.sh
├── .env.example
├── .gitignore
├── agents.py
├── cli_helpers.py
├── main.py
├── memory_store.py
├── ollama_service.py
├── prompt_templates.py
├── README.md
└── requirements.txt
```

## Setup

```bash
cd /Users/arjunvaid/Desktop/4_weeks/day12-personal-ai-os-prototype
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv
pip freeze > requirements.txt
cp .env.example .env
ollama pull llama3.2:1b
```

Start Ollama in another terminal if needed:

```bash
ollama serve
```

## Run the app

```bash
python main.py
```

Or:

```bash
./scripts/run_app.sh
```

## Run demo mode

```bash
python main.py --demo
```

Or:

```bash
bash scripts/run_demo.sh
```

## Reset starter memory

```bash
./scripts/reset_demo.sh
```

## Menu options

```text
1. View profile memory
2. Update profile memory
3. Add task
4. View tasks
5. Mark task as done
6. Add note
7. View notes
8. Run Planner Agent
9. Run Writer Agent
10. Run Reviewer Agent
11. Exit
```

## Beginner explanation

The app works like a small local workspace for an AI assistant.

Profile memory stores who the user is.
Task memory stores what needs to be done.
Notes memory stores useful information.
The specialist agents use that memory to plan, write, or review.

## Suggested demo prompts

Planner Agent:

```text
Create a simple plan for finishing this AI OS lab today.
```

Writer Agent:

```text
Write a short friendly note explaining what this Personal AI OS does.
```

Reviewer Agent:

```text
This app stores memory and has agents. It is useful.
```
