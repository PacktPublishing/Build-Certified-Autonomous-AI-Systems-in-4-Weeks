# Autonomous Research Agent with Ollama

## What It Does

A local AI research agent that plans, searches local text files, reads evidence, writes, reviews, revises, and saves a Markdown research report.

The user enters one research topic. The agent then runs an autonomous workflow:

1. Creates a beginner-friendly research plan
2. Generates search queries
3. Searches local files in the data folder
4. Reads selected local research notes
5. Collects evidence
6. Writes a Markdown draft report
7. Reviews the draft
8. Revises the report
9. Saves the final report locally

## Architecture

```text
Topic
  ↓
Planner
  ↓
Local Search Tool over data/*.txt
  ↓
Evidence Store
  ↓
Report Writer
  ↓
Reviewer
  ↓
Final Report
```

## Tools Included

- Python command-line interface
- Ollama local LLM provider
- llama3.2 local model
- Local text-file search tool
- Local document reader tool
- Evidence formatter
- Markdown report writer
- Report reviewer
- Report reviser
- Local report saver

## Tech Stack

- Python
- Ollama
- llama3.2
- Local text files
- Markdown

## Setup Instructions

Start Ollama in one terminal:

```bash
ollama serve
```

Open a second terminal and pull the model:

```bash
ollama pull llama3.2:3b
```

Create and activate the Python environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

The app searches local files in `data/`.

Run the agent:

```bash
python app.py
```

## Demo Prompts

Try these research topics:

```text
AI agents in small businesses
```

```text
AI adoption in small businesses
```

```text
Benefits of AI agents for small business operations
```

```text
Benefits of AI agents for education
```

```text
How retrieval augmented generation works
```

```text
Autonomous vehicles and safety
```

```text
History of artificial intelligence
```

```text
AI in healthcare
```

```text
How retrieval augmented generation works
```

## Example Generated Report

The final report is saved in the `reports/` folder as a Markdown file. Evidence is loaded from local text files in the `data/` folder.

Example filename:

```text
20260115_143022_ai_agents_in_small_businesses.md
```

## Demo Screenshot

Add a screenshot showing the terminal workflow with local file search.

## Demo Video

Add a short demo video link here.
