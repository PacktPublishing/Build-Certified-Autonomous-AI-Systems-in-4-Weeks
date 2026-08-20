import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from ollama import ResponseError, chat


# ---------------------------------------------------------
# App configuration
# ---------------------------------------------------------

MODEL_NAME = "llama3.2:3b"
DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
MAX_SEARCH_QUERIES = 4
MAX_RESULTS_PER_QUERY = 3
MAX_ARTICLE_CHARS = 2500


SYSTEM_PROMPT = """
You are a careful autonomous research assistant.
You help beginners understand topics clearly.
You must be practical, honest, and structured.
You should not invent facts.
If evidence is limited, say so clearly.
""".strip()


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def safe_filename(text: str) -> str:
    """Convert a topic into a safe filename."""

    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return cleaned[:60] or "research_report"


def print_step(title: str) -> None:
    """Print a clean progress heading."""

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def call_llm(messages: list[dict[str, str]], temperature: float = 0.2) -> str:
    """Call Ollama and return the assistant response."""

    response = chat(
        model=MODEL_NAME,
        messages=messages,
        options={
            "temperature": temperature,
        },
    )

    return response.message.content.strip()


def call_llm_json(messages: list[dict[str, str]]) -> dict[str, Any]:
    """Ask Ollama for JSON and safely parse the result."""

    response = chat(
        model=MODEL_NAME,
        messages=messages,
        format="json",
        options={
            "temperature": 0,
        },
    )

    raw_text = response.message.content.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        print("The model did not return clean JSON. Raw response:")
        print(raw_text)
        raise


# ---------------------------------------------------------
# Research planning
# ---------------------------------------------------------

def create_research_plan(topic: str) -> dict[str, Any]:
    """Create a short research plan and search queries."""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
Create a beginner-friendly research plan for this topic:

{topic}

Return only valid JSON with this structure:
{{
  "topic": "short topic name",
  "goal": "one sentence research goal",
  "questions": ["question 1", "question 2", "question 3"],
  "search_queries": ["query 1", "query 2", "query 3", "query 4"]
}}

Rules:
- Use at most 4 search queries.
- Keep questions simple.
- Do not include markdown.
""".strip(),
        },
    ]

    plan = call_llm_json(messages)

    queries = plan.get("search_queries", [])
    if not isinstance(queries, list) or not queries:
        plan["search_queries"] = [topic]

    plan["search_queries"] = plan["search_queries"][:MAX_SEARCH_QUERIES]

    return plan


# ---------------------------------------------------------
# Local research tools
# ---------------------------------------------------------

def extract_title(file_path: Path, content: str) -> str:
    """Extract a readable title from a local research file."""

    for line in content.splitlines():
        clean_line = line.strip()
        if clean_line.lower().startswith("title:"):
            return clean_line.split(":", 1)[1].strip()

    return file_path.stem.replace("_", " ").title()


def score_document(query: str, content: str) -> int:
    """Score a local document using simple keyword matching."""

    query_words = {
        word
        for word in re.findall(r"[a-zA-Z0-9]+", query.lower())
        if len(word) > 2
    }

    if not query_words:
        return 0

    lower_content = content.lower()
    return sum(lower_content.count(word) for word in query_words)


def search_local_documents(query: str) -> list[dict[str, str]]:
    """Search local text files and return matching documents."""

    if not DATA_DIR.exists():
        return []

    scored_results = []

    for file_path in DATA_DIR.glob("*.txt"):
        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError:
            continue

        score = score_document(query, content)

        if score > 0:
            scored_results.append(
                {
                    "title": extract_title(file_path, content),
                    "filename": file_path.name,
                    "score": str(score),
                }
            )

    scored_results.sort(key=lambda item: int(item["score"]), reverse=True)
    return scored_results[:MAX_RESULTS_PER_QUERY]


def read_local_document(filename: str) -> dict[str, str]:
    """Read a local text document from the data folder."""

    safe_name = Path(filename).name
    file_path = DATA_DIR / safe_name

    if not file_path.exists():
        return {
            "title": safe_name,
            "url": f"local://data/{safe_name}",
            "extract": "No local document found.",
        }

    content = file_path.read_text(encoding="utf-8").strip()

    return {
        "title": extract_title(file_path, content),
        "url": f"local://data/{safe_name}",
        "extract": content[:MAX_ARTICLE_CHARS],
    }


# ---------------------------------------------------------
# Evidence gathering
# ---------------------------------------------------------

def gather_evidence(plan: dict[str, Any]) -> list[dict[str, str]]:
    """Use local search and read tools to gather evidence."""

    evidence = []
    seen_files = set()

    search_queries = plan.get("search_queries", [])

    for query in search_queries:
        print(f"\nSearching local files: {query}")

        search_results = search_local_documents(query)

        if not search_results:
            print(f"No local files matched query: {query}")
            continue

        for result in search_results:
            filename = result["filename"]

            if filename in seen_files:
                continue

            seen_files.add(filename)
            print(f"Reading local file: {filename}")

            article = read_local_document(filename)
            evidence.append(article)

    return evidence


# ---------------------------------------------------------
# Report writing and reflection
# ---------------------------------------------------------

def format_evidence_for_prompt(evidence: list[dict[str, str]]) -> str:
    """Format evidence for the LLM prompt."""

    if not evidence:
        return "No evidence was collected."

    sections = []

    for index, item in enumerate(evidence, start=1):
        sections.append(
            f"""
SOURCE {index}
Title: {item['title']}
URL: {item['url']}
Extract:
{item['extract']}
""".strip()
        )

    return "\n\n".join(sections)


def write_report(topic: str, plan: dict[str, Any], evidence: list[dict[str, str]]) -> str:
    """Write the first draft of the research report."""

    evidence_text = format_evidence_for_prompt(evidence)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
Write a beginner-friendly research report about:

{topic}

Research plan:
{json.dumps(plan, indent=2)}

Evidence:
{evidence_text}

Report requirements:
- Use Markdown.
- Start with a clear title.
- Include an executive summary.
- Answer the main research questions.
- Include a section called Key Takeaways.
- Include a section called Limitations.
- Include a Sources section with the source titles and URLs.
- Do not invent facts outside the provided evidence.
""".strip(),
        },
    ]

    return call_llm(messages, temperature=0.2)


def review_report(topic: str, report: str) -> str:
    """Ask the LLM to critique the report."""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
Review this research report for a beginner audience.

Topic:
{topic}

Report:
{report}

Give concise feedback in this format:

Strengths:
- ...

Improvements Needed:
- ...

Final Verdict:
- Keep, revise, or rewrite
""".strip(),
        },
    ]

    return call_llm(messages, temperature=0.2)


def revise_report(topic: str, report: str, review: str) -> str:
    """Revise the report based on the review."""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
Revise the research report using the review feedback.

Topic:
{topic}

Original report:
{report}

Review feedback:
{review}

Return the final Markdown report only.
Keep it clear, practical, and beginner-friendly.
""".strip(),
        },
    ]

    return call_llm(messages, temperature=0.2)


def save_report(topic: str, report: str) -> Path:
    """Save the final report to the reports folder."""

    REPORTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{safe_filename(topic)}.md"
    path = REPORTS_DIR / filename

    path.write_text(report, encoding="utf-8")

    return path


# ---------------------------------------------------------
# Autonomous agent runner
# ---------------------------------------------------------

def run_research_agent(topic: str) -> None:
    """Run the full autonomous research workflow."""

    print_step("1. Creating research plan")
    plan = create_research_plan(topic)
    print(json.dumps(plan, indent=2))

    print_step("2. Gathering evidence")
    evidence = gather_evidence(plan)
    print(f"\nCollected {len(evidence)} evidence items.")

    if not evidence:
        print("No evidence was collected. Try a broader topic or add more .txt files to the data folder.")
        return

    print_step("3. Writing first draft")
    draft_report = write_report(topic, plan, evidence)
    print(draft_report[:1000])
    print("\n...draft preview trimmed...\n")

    print_step("4. Reviewing the draft")
    review = review_report(topic, draft_report)
    print(review)

    print_step("5. Revising the report")
    final_report = revise_report(topic, draft_report, review)
    print(final_report[:1000])
    print("\n...final report preview trimmed...\n")

    print_step("6. Saving the final report")
    path = save_report(topic, final_report)
    print(f"Saved report to: {path}")


# ---------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------

def main() -> None:
    """Start the command-line app."""

    print("=" * 70)
    print("AUTONOMOUS RESEARCH AGENT")
    print("Local evidence source: data/*.txt")
    print(f"Local LLM provider: Ollama")
    print(f"Model: {MODEL_NAME}")
    print("=" * 70)

    topic = input("\nEnter a research topic: ").strip()

    if not topic:
        print("Please enter a topic next time.")
        return

    try:
        run_research_agent(topic)
    except ResponseError as error:
        print(f"\nOllama error: {error}")
        print(f"Make sure the model is installed: ollama pull {MODEL_NAME}")
    except ConnectionError:
        print("\nCould not connect to Ollama.")
        print("Make sure Ollama is running with: ollama serve")
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")
    except Exception as error:
        print(f"\nSomething went wrong: {error}")


if __name__ == "__main__":
    main()
