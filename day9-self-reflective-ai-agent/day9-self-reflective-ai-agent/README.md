# Day 9 Lab — Self-Reflective AI Agent with Ollama

## Goal

In this lab, we build a local AI agent that improves its own answer before showing the final result.

The agent follows this loop:

```text
User question
  -> Draft answer
  -> Critique draft
  -> Revise answer
  -> Score final answer
  -> Save run to run_history.json
```

## What learners will build

- A terminal-based reflective AI agent
- A draft step
- A critique step
- A revision step
- A quality score step
- A local `run_history.json` file

## Local LLM provider

This lab uses Ollama locally.

No paid API key is required.

## Project structure

```text
day9-self-reflective-ai-agent/
├── scripts/
│   └── run_demo.sh
├── .env.example
├── .gitignore
├── history_service.py
├── main.py
├── ollama_service.py
├── prompt_templates.py
├── README.md
├── requirements.txt
└── run_history.json
```

## File overview

### `main.py`

This is the entry point of the app.
It controls the full reflective loop:

1. Ask the user for a question
2. Generate a draft answer
3. Critique the draft
4. Revise the answer
5. Score the final answer
6. Save the run history

### `ollama_service.py`

This file talks to the local Ollama server.
It sends prompts to Ollama's `/api/chat` endpoint and returns the model response.

### `prompt_templates.py`

This file stores the instructions for each agent step.
Keeping prompts in a separate file makes the project easier to understand and modify.

### `history_service.py`

This file saves each run to `run_history.json`.
That lets learners see how the agent's draft, critique, revision, and score were recorded.

### `run_history.json`

This file starts as an empty list.
After each run, the app adds a new record.

## Setup

### 1. Go to the project folder

```bash
cd /Users/arjunvaid/Desktop/4_weeks/day9-self-reflective-ai-agent
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

### 7. Pull the local model

```bash
ollama pull llama3.2:1b
```

### 8. Run the app

```bash
python main.py
```

Or use the helper script:

```bash
./scripts/run_demo.sh
```

## Example question

When the app asks for a question, try:

```text
How can small businesses use AI for customer support?
```

The app will show:

1. Draft answer
2. Critique
3. Revised answer
4. Quality score

Then it saves the full run to `run_history.json`.

## Beginner explanation

A normal AI assistant usually gives one answer immediately.

A self-reflective AI agent adds a review step before finalizing the response.

Instead of saying:

```text
Question -> Answer
```

This lab shows:

```text
Question -> Draft -> Critique -> Revision -> Score
```

This makes the agent feel more thoughtful because it checks and improves its own work.

## Troubleshooting

### Error: Could not connect to Ollama

Make sure Ollama is running:

```bash
ollama serve
```

### Error: Model not found

Pull the model:

```bash
ollama pull llama3.2:1b
```

### The first response is slow

That is normal. Local models can take time to load the first time.
