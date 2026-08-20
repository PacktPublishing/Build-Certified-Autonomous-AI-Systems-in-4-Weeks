"""Prompt templates for Day 13: Viral AI Product Prototype."""

PRODUCT_IDEA_SYSTEM_PROMPT = """
You are a practical AI product strategist helping beginners turn messy ideas into clear product concepts.
Your ideas should be realistic, simple enough for a student capstone, and focused on a painful workflow.

Rules:
- Generate exactly 3 product ideas.
- Each idea should solve the painful workflow for the target user.
- Avoid vague ideas like "AI assistant" unless the specific workflow is clear.
- Prefer products that can be prototyped with a local LLM and a simple web app.
- Return JSON only. Do not include markdown.
""".strip()

PRODUCT_IDEA_USER_PROMPT = """
Turn this messy product direction into 3 clear AI product ideas.

Target user:
{target_user}

Painful workflow:
{painful_workflow}

Desired output:
{desired_output}

Return JSON only in this exact structure:
{{
  "ideas": [
    {{
      "name": "short product name",
      "one_liner": "one sentence explanation",
      "target_user": "who this is for",
      "painful_workflow": "workflow being improved",
      "main_output": "what the product produces",
      "why_it_could_spread": "why someone would share or recommend it",
      "prototype_features": ["feature 1", "feature 2", "feature 3"],
      "capstone_fit": "why this is realistic for the final capstone"
    }}
  ]
}}
""".strip()

FALLBACK_IDEA_TEMPLATE = {
    "ideas": [
        {
            "name": "Workflow Brief Builder",
            "one_liner": "Turns a messy workflow problem into a structured action brief that is easy to share.",
            "target_user": "{target_user}",
            "painful_workflow": "{painful_workflow}",
            "main_output": "{desired_output}",
            "why_it_could_spread": "People share it because it converts confusing work into a clean document they can reuse with teammates.",
            "prototype_features": [
                "Guided input form",
                "AI-generated structured brief",
                "Downloadable markdown output",
            ],
            "capstone_fit": "This is realistic because students can build it with Streamlit, Ollama, prompt templates, scoring, and file export.",
        },
        {
            "name": "Pain Point to Prototype Planner",
            "one_liner": "Helps a user turn one painful task into a simple AI product plan.",
            "target_user": "{target_user}",
            "painful_workflow": "{painful_workflow}",
            "main_output": "{desired_output}",
            "why_it_could_spread": "It gives users a fast before-and-after story they can show to others who have the same problem.",
            "prototype_features": [
                "Pain workflow summary",
                "Product idea generation",
                "Simple scoring and recommendation",
            ],
            "capstone_fit": "This fits the capstone because it combines form input, local AI generation, ranking, and saved output files.",
        },
        {
            "name": "Shareable AI Solution Snapshot",
            "one_liner": "Creates a quick product snapshot that explains the user, pain, output, and MVP features.",
            "target_user": "{target_user}",
            "painful_workflow": "{painful_workflow}",
            "main_output": "{desired_output}",
            "why_it_could_spread": "It is easy to share because the output reads like a mini product pitch.",
            "prototype_features": [
                "Idea cards",
                "Virality explanation",
                "Product brief export",
            ],
            "capstone_fit": "This is a strong capstone candidate because it is focused, demonstrable, and understandable to beginners.",
        },
    ]
}
