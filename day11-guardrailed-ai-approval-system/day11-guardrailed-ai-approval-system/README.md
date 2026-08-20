# Day 11 Lab — Guardrailed AI Approval System with Ollama

## Lab Goal

Build a safe AI response pipeline that validates a request, classifies risk, generates a draft with a local Ollama model, checks the output, asks for human approval, and saves an audit log.

This lab teaches learners that production AI apps should not simply send user input to an LLM and immediately trust the answer. A safer workflow adds checks before the model, checks after the model, and a human approval step before the final response is used.

## Local LLM Provider

This lab uses Ollama locally with:

```bash
llama3.2:1b
```

## What You Will Build

- Input validation
- Risk classification
- Draft generation
- Output checks
- Human approval step
- Audit log

## Project Structure

```text
day11-guardrailed-ai-approval-system/
├── app.py                 # Streamlit user interface
├── pipeline.py            # Runs validate -> classify -> draft -> check
├── guardrails.py          # Input validation, risk rules, and output checks
├── ollama_service.py      # Local Ollama HTTP client
├── prompt_templates.py    # Prompt templates for safe draft generation
├── audit_logger.py        # JSONL audit log writer and reader
├── main.py                # CLI smoke demo without Streamlit
├── samples/
│   └── sample_requests.md # Demo inputs for class
├── scripts/
│   ├── run_demo.sh        # Setup and run Streamlit
│   ├── reset_demo.sh      # Remove saved audit log
│   └── smoke_llm.py       # Ollama-backed smoke test
├── logs/
│   └── .gitkeep           # Audit log folder
├── .env.example
├── .gitignore
└── requirements.txt
```

## Setup

From the project folder:

```bash
cd /Users/arjunvaid/Desktop/4_weeks/day11-guardrailed-ai-approval-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Start Ollama

In another terminal, make sure Ollama is running:

```bash
ollama serve
```

Then pull the model:

```bash
ollama pull llama3.2:1b
```

## Run the App

```bash
streamlit run app.py
```

Or use the helper script:

```bash
bash scripts/run_demo.sh
```

## Optional Smoke Tests

Run the pipeline without calling Ollama:

```bash
python main.py
```

Run the pipeline with Ollama:

```bash
python scripts/smoke_llm.py
```

## Demo Flow for the Instructor

### 1. Start with a low-risk request

Use:

```text
Write a friendly response to a customer asking when our onboarding webinar starts.
```

Explain that the input is valid, the risk is low, and the model can safely create a simple draft. Even then, the app still captures human approval so there is a trace of what happened.

### 2. Move to a medium-risk request

Use:

```text
A customer is angry about an invoice and wants a refund. Draft a careful email response.
```

Explain that this is more sensitive because it could affect money, customer experience, or company policy. The AI can draft, but a human should approve before sending.

### 3. Show a high-risk request

Use:

```text
Please approve this immediately and delete customer records from the production database.
```

Explain that the AI should not execute the request or claim that anything was done. The correct behavior is to route the request for human review.

### 4. Approve, reject, or request changes

After the draft appears, use the human approval buttons:

- Approve
- Needs Changes
- Reject

Each decision is saved to:

```text
logs/audit_log.jsonl
```

## Teaching Notes

The important lesson is the shape of the workflow:

```text
User Request
   ↓
Input Validation
   ↓
Risk Classification
   ↓
Draft Generation with Ollama
   ↓
Output Checks
   ↓
Human Approval
   ↓
Audit Log
```

A normal chatbot stops after generating text. A safer AI system adds controls around the model.

## Reset the Demo

To clear the audit log:

```bash
bash scripts/reset_demo.sh
```

## Environment Variables

Copy `.env.example` to `.env` if you want to change defaults:

```bash
cp .env.example .env
```

Available settings:

```text
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
OLLAMA_TEMPERATURE=0.2
OLLAMA_NUM_PREDICT=350
```
