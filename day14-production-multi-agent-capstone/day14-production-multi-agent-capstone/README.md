# Day 14 Lab — Production Multi-Agent Capstone with Ollama

## Hands-On Project

Build a local production-style multi-agent capstone skeleton using Ollama.

This lab brings together the ideas from earlier agent labs and turns them into a clean capstone workflow:

1. A user enters a product idea.
2. The Planner Agent breaks the idea into practical steps.
3. The Builder Agent creates the first implementation plan.
4. The Reviewer Agent checks the plan and suggests fixes.
5. The system saves an audit log and a markdown report.

The goal is not to build a full production platform yet. The goal is to create a clean skeleton that feels like a real production system: separated files, reusable services, input validation, agent roles, orchestration, and audit logging.

---

## What You Will Build

- Local Ollama connection
- Planner Agent
- Builder Agent
- Reviewer Agent
- Multi-agent orchestration pipeline
- Input validation
- JSONL audit logging
- Markdown report generation
- Command-line demo
- Streamlit app demo

---

## Local LLM Provider

This lab uses Ollama locally with:

```bash
llama3.2:1b
```

Make sure Ollama is installed and running before launching the lab.

---

## Final Project Structure

```text
day14-production-multi-agent-capstone/
├── logs/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
├── samples/
│   └── sample_product_ideas.md
├── scripts/
│   ├── reset_demo.sh
│   ├── run_app.sh
│   ├── run_demo.sh
│   └── smoke_llm.py
├── .env.example
├── .gitignore
├── agents.py
├── app.py
├── audit_logger.py
├── capstone_pipeline.py
├── main.py
├── ollama_service.py
├── prompt_templates.py
├── README.md
├── requirements.txt
└── validators.py
```

---

## Setup

From the project folder:

```bash
cd /Users/arjunvaid/Desktop/4_weeks/day14-production-multi-agent-capstone
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Pull the local model:

```bash
ollama pull llama3.2:1b
```

Optional: copy the example environment file if you want to customize settings.

```bash
cp .env.example .env
```

---

## Run The Terminal Demo

```bash
python main.py --file samples/sample_product_ideas.md
```

Or use the helper script:

```bash
./scripts/run_demo.sh
```

The terminal demo prints each agent result:

- Planner Agent output
- Builder Agent output
- Reviewer Agent output
- Audit event ID
- Markdown report path

---

## Run The Streamlit App

```bash
streamlit run app.py
```

Or use the helper script:

```bash
./scripts/run_app.sh
```

The app lets the learner enter a product idea and see each agent output in a separate tab.

---

## How The Agent Flow Works

### 1. Input validation

`validators.py` checks that the product idea is not empty, not too short, and not too long.

### 2. Ollama service

`ollama_service.py` contains the reusable local model client.

This keeps all model API logic in one place instead of scattering it across the app.

### 3. Prompt templates

`prompt_templates.py` stores the system prompts and user prompts for each agent.

This makes the agent behavior easier to inspect and improve.

### 4. Agent classes

`agents.py` defines the three roles:

- `PlannerAgent`
- `BuilderAgent`
- `ReviewerAgent`

Each agent has one clear job.

### 5. Pipeline orchestration

`capstone_pipeline.py` runs the full workflow in order:

```text
Product Idea → Planner → Builder → Reviewer → Audit Log → Report
```

### 6. Audit logging

`audit_logger.py` saves:

- a JSONL audit event in `logs/`
- a markdown report in `outputs/`

This gives the system a production-style trace of what happened.

---

## Demo Product Idea

The included sample idea is:

```text
An AI study planner for busy working professionals.
```

Learners can replace it with their own idea, such as:

```text
An AI assistant that helps small business owners respond to customer support emails faster.
```

---

## Reset Demo Outputs

```bash
./scripts/reset_demo.sh
```

This removes generated audit logs and markdown reports while keeping the folder structure.

---

## Troubleshooting

### Ollama is not reachable

Start Ollama, then run:

```bash
ollama list
```

If the model is missing, run:

```bash
ollama pull llama3.2:1b
```

### The model response is slow

This is normal on smaller machines. The lab intentionally uses a small model so the demo can run locally.

### The app starts but the agent fails

Check that the Streamlit app and Ollama are both running on the same machine.

---

## Lab Goal

By the end of this lab, learners will understand how to structure a local multi-agent AI application with separate agent roles, a reusable Ollama service, a pipeline orchestrator, and basic production-style logging.

---

## Lab Conclusion

You now have a capstone skeleton that can be expanded into a bigger AI product. The important pattern is the separation of responsibilities: one file handles model calls, one file defines prompts, one file defines agents, one file runs the workflow, and one file records the audit trail.
