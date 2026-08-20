# Day 15 Lab - Capstone Deployment and Portfolio Polish with Ollama

## Goal

Use Ollama to generate production-readiness assets for the final capstone.

The app creates:

- `readiness_checklist.md`
- `README_draft.md`
- `demo_script.md`
- `qa_prep.md`

The generated files are saved inside the `outputs/` folder.

## Local model

This lab uses Ollama locally with:

```text
llama3.2:1b
```

No paid API key is required.

## Final workflow

```text
capstone_profile.json
  -> Python app
  -> Ollama local model
  -> Markdown portfolio assets in outputs/
```

## Project structure

```text
day15-capstone-polish/
├── outputs/
│   └── .gitkeep
├── scripts/
│   ├── reset_outputs.sh
│   └── run_app.sh
├── .env.example
├── .gitignore
├── asset_writer.py
├── capstone_profile.json
├── main.py
├── ollama_service.py
├── project_context.py
├── prompt_templates.py
├── README.md
└── requirements.txt
```

## File overview

### `capstone_profile.json`

This file describes the learner's final capstone project.

Learners should customize this file before generating the portfolio assets.

### `project_context.py`

Loads the capstone profile and prepares it for prompts.

### `prompt_templates.py`

Stores the prompts for each generated asset.

### `ollama_service.py`

Connects the Python app to Ollama.

### `asset_writer.py`

Writes generated Markdown content into the `outputs/` folder.

### `main.py`

Coordinates the full generation workflow.

## Setup

```bash
cd /Users/arjunvaid/Desktop/4_weeks/day15-capstone-polish
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv
pip freeze > requirements.txt
cp .env.example .env
ollama pull llama3.2:1b
```

Start Ollama if needed:

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

## Reset generated outputs

```bash
./scripts/reset_outputs.sh
```

## Beginner explanation

This lab is about taking a working capstone and polishing it for presentation.

A real project is not finished when the code runs.
It also needs documentation, a demo script, readiness checks, and answers to likely questions.

This app uses a local Ollama model to help generate those assets.
Learners still review and edit the final Markdown files before putting them in a portfolio.
