# Day 13 Lab — Viral AI Product Prototype with Ollama

## Hands-On Project

Build a local AI product idea generator that helps learners turn a messy idea into a clear product brief.

## Goal

The app asks for a target user, a painful workflow, and the final output the user wants. Then it uses a local Ollama model to generate 3 product ideas, score each idea, save the best idea to `product_ideas.json`, and create a `product_brief.md` file for the final capstone.

## Local LLM Provider

This lab uses Ollama locally. The default model is:

```bash
llama3.2:1b
```

## What the App Does

- Ask for a target user
- Ask for a painful workflow
- Ask what output the user wants
- Use Ollama as the local LLM provider
- Generate 3 product ideas
- Score each idea
- Save the best idea to `product_ideas.json`
- Create a `product_brief.md` file for the final capstone

## Project Structure

```text
day13-viral-ai-product-prototype/
├── app.py                 # Streamlit UI
├── idea_pipeline.py       # Validates input, calls Ollama, scores ideas, saves outputs
├── ollama_service.py      # Local Ollama HTTP client
├── prompt_templates.py    # Prompt templates and deterministic fallback ideas
├── scoring.py             # Transparent product scoring rules
├── file_service.py        # Saves product_ideas.json and product_brief.md
├── main.py                # CLI smoke demo without Ollama
├── product_ideas.json     # Saved best idea and all scored ideas
├── product_brief.md       # Final capstone product brief
├── samples/
│   └── sample_inputs.md   # Demo inputs
├── scripts/
│   ├── run_demo.sh        # Setup and run Streamlit
│   ├── reset_demo.sh      # Reset generated outputs
│   └── smoke_llm.py       # Ollama-backed smoke test
├── .env.example
├── .gitignore
└── requirements.txt
```

## Setup

From the project folder:

```bash
cd /Users/arjunvaid/Desktop/4_weeks/day13-viral-ai-product-prototype
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Start Ollama

In another terminal, make sure Ollama is running:

```bash
ollama serve
```

Then make sure the model exists:

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

Run the pipeline without Ollama:

```bash
python main.py
```

Run the pipeline with Ollama:

```bash
python scripts/smoke_llm.py
```

## Demo Flow for the Instructor

### 1. Explain the messy idea problem

Most product ideas start messy. A learner may know the user and the pain, but they may not know how to turn that into a product brief.

This lab teaches a simple product-thinking pipeline:

```text
Target User
   ↓
Painful Workflow
   ↓
Desired Output
   ↓
AI Product Ideas
   ↓
Scoring
   ↓
Best Idea
   ↓
Capstone Brief
```

### 2. Enter the three inputs

Use the sample course creator inputs:

```text
Target user:
Busy course creators who need to turn rough lesson ideas into polished lab plans

Painful workflow:
They have messy notes, scattered feature ideas, and no clear structure for what the student should build in the lab.

Desired output:
A clear product brief with product name, target user, painful workflow, features, score, and capstone-ready plan.
```

### 3. Generate 3 product ideas

The app asks Ollama to return structured JSON. The pipeline then normalizes the ideas so the rest of the app has a predictable format.

### 4. Score each idea

Each idea receives scores for:

- Clarity
- Pain strength
- Shareability
- Capstone buildability
- Total score

The top-scoring idea becomes the recommended capstone direction.

### 5. Save the final outputs

The app saves:

```text
product_ideas.json
product_brief.md
```

The markdown brief is the file learners can use as the starting point for the final capstone.

## Reset the Demo

To reset generated files:

```bash
bash scripts/reset_demo.sh
```

## Environment Variables

Copy `.env.example` to `.env` if you want to customize the local model settings:

```bash
cp .env.example .env
```

Available settings:

```text
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
OLLAMA_TEMPERATURE=0.4
OLLAMA_NUM_PREDICT=800
```
