# Day 5 Lab - Multi-Agent Content Pipeline with Ollama

## What this lab builds

This lab builds a small local AI team that creates a polished piece of content from one topic.

The app runs from the command line and uses Ollama as the local LLM provider.

## Final architecture

```text
User topic
  -> Planner Agent
  -> Writer Agent
  -> Reviewer Agent
  -> Final Writer Pass
  -> final_output.md
```

## Agents

### Planner Agent

Creates a content plan before the draft is written.

### Writer Agent

Uses the plan to write the first draft.

### Reviewer Agent

Critiques the first draft and asks for specific improvements.

### Final Writer Pass

Uses the original plan, the first draft, and the review notes to create the polished final content.

## Project structure

```text
day5-multi-agent-content-pipeline/
├── app.py
├── agents.py
├── llm_service.py
├── prompts.py
├── requirements.txt
├── .env.example
├── .gitignore
├── outputs/
└── README.md
```

## File responsibilities

- `app.py` is the command-line entry point.
- `agents.py` defines the agent object, shared workspace, pipeline flow, dry-run pipeline, and Markdown report builder.
- `llm_service.py` contains the small Ollama client.
- `prompts.py` stores the system prompts and task prompts for each agent step.
- `final_output.md` is created when the app runs.

## Setup

Create and activate a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Copy the example environment file if you want to customize the model.

```bash
cp .env.example .env
```

## Ollama setup

Start Ollama.

```bash
ollama serve
```

In another terminal, pull a local model.

```bash
ollama pull llama3.2:3b
```

You can also use another installed Ollama model by setting `OLLAMA_MODEL` in `.env` or passing `--model` when running the app.

## Run the app

Run with a topic.

```bash
python app.py --topic "How small businesses can use AI agents"
```

Or run interactively.

```bash
python app.py
```

The app saves the full result to:

```text
final_output.md
```

## Dry run mode

Use dry-run mode to test the full pipeline without calling Ollama.

```bash
python app.py --topic "AI agents for content creation" --dry-run
```

This is useful when you want to verify the file flow, shared workspace, and output generation before using a local model.

## Demo prompts

Try these topics:

```text
How beginners can learn prompt engineering
How AI agents help with research
Why local LLMs are useful for learning
How small teams can use AI automation
```

## Teaching notes

This lab introduces learners to a simple multi-agent pattern:

1. Keep each agent focused on one responsibility.
2. Store shared state in a workspace dictionary.
3. Pass each agent output into the next step.
4. Save the final result so the pipeline produces a real artifact.
