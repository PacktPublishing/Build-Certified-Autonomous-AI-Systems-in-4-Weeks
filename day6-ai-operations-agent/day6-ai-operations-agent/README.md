# Day 6 Lab — AI Operations Agent with Ollama and Tools

## Goal

Build an AI operations agent that can choose and run simple tools.

The agent uses Ollama locally to decide what the user wants. Python then executes the correct tool and sends the tool result back to Ollama so the model can write a final user-friendly answer.

## Final architecture

```text
User request
  -> Ollama decides the tool
  -> Python runs the tool
  -> Tool result goes back to Ollama
  -> Final user-friendly answer
```

## Tools in this lab

1. Calculator tool
2. Ticket lookup tool
3. System status tool
4. Summary writer tool

## What learners will learn

- How to represent tools as Python functions
- How to ask Ollama for structured JSON
- How to route a request to the correct tool
- How to combine tool results into a final answer

## Project files

```text
app.py           Streamlit user interface
cli.py           Terminal version of the lab
agent.py         Main orchestration flow
llm_service.py   Ollama chat and JSON decision logic
tools.py         Calculator, ticket lookup, system status, and summary tools
tests/           Simple tests for the Python tools
.env.example     Environment variable template
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the environment template:

```bash
cp .env.example .env
```

## Ollama setup

Make sure Ollama is running:

```bash
ollama serve
```

Pull the default model used by the lab:

```bash
ollama pull llama3.2:3b
```

You can change the model in `.env`:

```bash
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

## Run the Streamlit app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Run from the terminal

```bash
python cli.py "Look up ticket INC1002"
python cli.py "What is 42 * 8 + 17?"
python cli.py "Check the status of the payment service"
```

## Example requests

```text
What is 42 * 8 + 17?
Look up ticket INC1002.
Check the status of the payment service.
Summarize this: The payment service had high latency this morning. The team increased the database connection pool. Monitoring is now stable.
```

## Teaching sequence

1. Start with `tools.py` and show that tools are normal Python functions.
2. Open `llm_service.py` and explain that Ollama returns structured JSON.
3. Open `agent.py` and show the routing flow.
4. Run `cli.py` to test the logic quickly.
5. Run `app.py` to demo the full learner-facing experience.

## Important teaching point

The model does not directly run code. It only returns a decision like this:

```json
{
  "tool_name": "ticket_lookup",
  "arguments": {
    "ticket_id": "INC1002"
  }
}
```

Python receives that JSON, checks the tool name, and calls one safe function.
