# Day 7 Lab - Streamlit AI Copilot with Ollama and Human Approval

## Hands-On Project

Voice-Enabled AI Copilot

## Goal

Build a simple web interface for an AI copilot.

The copilot will:

- Run with Streamlit
- Use Ollama as the local LLM provider
- Let the user generate a draft
- Require human approval before saving the output
- Optionally read the approved output aloud using local text-to-speech

## What learners will learn

- How to build a simple AI interface
- How chat messages are stored in Streamlit session state
- How human approval protects the workflow
- How a backend LLM becomes a user-facing app

## Final architecture

```text
User
  -> Streamlit UI
  -> Ollama local model
  -> Draft output
  -> Human approves or rejects
  -> approved_outputs.md
```

## Project structure

```text
day7-ai-copilot-interface/
├── app.py
├── llm_service.py
├── approval_service.py
├── tts_service.py
├── approved_outputs.md
├── requirements.txt
├── .gitignore
└── README.md
```

## File overview

### app.py

The main Streamlit interface. It collects the user's request, calls the local model, stores chat-style messages in session state, and shows the approval buttons.

### llm_service.py

The Ollama integration layer. It checks whether Ollama is reachable and sends the user's request to the local model.

### approval_service.py

The human approval layer. It only writes output to `approved_outputs.md` after the user clicks **Approve and Save**.

### tts_service.py

The optional local text-to-speech layer. On macOS it uses the built-in `say` command when available.

### approved_outputs.md

The final saved Markdown file. Approved AI drafts are appended here.

## Setup

Create and activate a virtual environment:

```bash
python3.12 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running:

```bash
ollama serve
```

Pull a local model if needed:

```bash
ollama pull llama3.2:3b
```

Run the app:

```bash
streamlit run app.py
```

## Demo prompts

Try these prompts in the app:

```text
Write a beginner-friendly summary of what we built in this AI bootcamp.
```

```text
Create a short LinkedIn post about building local AI apps with Ollama and Streamlit.
```

```text
Draft a simple course completion message for learners who finished the 7-day bootcamp.
```

## Human approval workflow

1. The user enters a request.
2. The AI copilot generates a draft.
3. The draft appears in the review area.
4. The human can edit the draft.
5. The human clicks **Approve and Save**.
6. The app appends the approved draft to `approved_outputs.md`.
7. The human can optionally read the approved output aloud.

## Why this approval step matters

AI output should not automatically become final output. The approval step gives the human a chance to review, edit, reject, or approve the generated content before it is saved.
