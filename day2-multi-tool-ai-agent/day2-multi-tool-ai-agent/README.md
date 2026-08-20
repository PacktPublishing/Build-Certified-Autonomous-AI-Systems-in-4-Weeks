# Day 2 Multi-Tool AI Agent with Ollama

## What the Agent Does

This project is a local terminal-based multi-tool AI agent. It accepts a user request, asks a local Ollama model what to do next, validates the model's JSON decision, runs approved Python tools, observes the tool result, and returns a final user-friendly answer.

The agent can:

- Answer terminal prompts
- Use a safe calculator tool
- Read local text files from the data folder
- Search local notes for matching lines
- Stop safely after a maximum number of tool steps

## Architecture Diagram

```text
User
  ↓
Python app.py
  ↓
Ollama local LLM
  ↓
Tool decision as JSON
  ↓
Python executes selected tool
  ↓
Tool observation
  ↓
Ollama creates final answer
  ↓
User sees response
```

## Tools Included

### calculator

Solves safe math expressions such as `25 * 18 + 40`.

### file_reader

Reads a specific `.txt` file from the local `data/` folder.

### notes_search

Searches all `.txt` notes in the local `data/` folder and returns matching lines.

## Setup Instructions

Start Ollama in one terminal:

```bash
ollama serve
```

Open a second terminal and install the recommended model:

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

Run the agent:

```bash
python app.py
```

## Demo Prompts

Try these prompts after the app starts:

```text
What is 25 * 18 + 40?
```

```text
Search my notes for agent loop.
```

```text
Read the file ai_agents.txt and summarize it.
```

```text
What does week 3 focus on in my bootcamp plan?
```

## Screenshots

Add screenshots here showing:

- The startup screen
- A calculator tool run
- A file reader tool run
- A notes search tool run

## Short Demo Video Link

Add your demo video link here after recording the project walkthrough.
