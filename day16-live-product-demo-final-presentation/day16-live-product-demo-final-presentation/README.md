# Day 16 Lab — Live Product Demo and Final Presentation with Ollama

## Hands-On Project

**Live Product Demo and Final Presentation**

In this final lab, you will use Ollama as a local demo coach. Instead of asking the model to build another feature, you will ask it to help you prepare the final presentation for the product you built.

The app generates four Markdown files:

- `final_demo_script.md`
- `judge_rubric.md`
- `launch_post.md`
- `improvement_plan.md`

These files are saved inside the `outputs/` folder.

---

## What learners build

Learners build a small Streamlit application that collects final product details and sends them to a local Ollama model.

The model acts like a presentation coach and creates:

1. A spoken final demo script.
2. A judging rubric for the presentation.
3. A launch post for sharing the project.
4. A practical improvement plan for the next version.

This is a useful final capstone lab because it teaches learners that AI can help not only with code, but also with communication, product thinking, and launch preparation.

---

## Project structure

```text
day16-live-product-demo-final-presentation/
├── app.py
├── main.py
├── ollama_service.py
├── prompt_templates.py
├── presentation_pipeline.py
├── file_writer.py
├── requirements.txt
├── README.md
├── samples/
│   └── sample_product_brief.md
├── outputs/
│   └── .gitkeep
└── scripts/
    ├── run_app.sh
    ├── run_demo.sh
    ├── reset_outputs.sh
    └── smoke_llm.py
```

---

## Step 1 — Start Ollama

Open a terminal and run:

```bash
ollama serve
```

If Ollama is already running, you may see a message saying the port is already in use. That is okay.

---

## Step 2 — Pull a local model

In another terminal, run:

```bash
ollama pull llama3.2
```

The default model for this lab is `llama3.2`.

You can change it in the app sidebar or by setting `OLLAMA_MODEL` in a `.env` file.

---

## Step 3 — Create and activate a virtual environment

From this project folder:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5 — Run the Streamlit app

```bash
streamlit run app.py
```

Or use the helper script:

```bash
bash scripts/run_app.sh
```

Then open the local Streamlit URL shown in the terminal.

---

## Step 6 — Generate the final assets

Inside the app:

1. Fill in the product name.
2. Describe the one-line idea.
3. Explain the target user and problem.
4. Add the features that were built.
5. Add the demo flow.
6. Mention the strongest demo moment.
7. Mention honest weak spots.
8. Click **Generate Final Presentation Assets**.

The app saves the generated files here:

```text
outputs/final_demo_script.md
outputs/judge_rubric.md
outputs/launch_post.md
outputs/improvement_plan.md
```

---

## Optional CLI demo

You can also generate the files from the terminal:

```bash
python main.py
```

Or:

```bash
bash scripts/run_demo.sh
```

---

## Optional Ollama smoke test

Use this to confirm that Ollama is reachable:

```bash
python scripts/smoke_llm.py
```

---

## Teaching sequence for the lab

A clean teaching order is:

1. `README.md` — explain the goal and final outputs.
2. `ollama_service.py` — show how the app talks to local Ollama.
3. `prompt_templates.py` — show how each final asset gets its own focused prompt.
4. `presentation_pipeline.py` — show how the product context becomes four generated files.
5. `file_writer.py` — show how Markdown outputs are saved.
6. `app.py` — connect everything to a beginner-friendly UI.
7. `main.py` — show the same workflow from the command line.

---

## Lab wrap-up

By the end of this lab, learners have a final presentation package that helps them explain the product, evaluate it, share it publicly, and plan improvements after the demo.
