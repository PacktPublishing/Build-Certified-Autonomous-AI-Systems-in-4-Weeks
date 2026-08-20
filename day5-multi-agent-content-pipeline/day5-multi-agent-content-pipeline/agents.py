"""Agent definitions and pipeline orchestration for the Day 5 lab."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from llm_service import OllamaClient
from prompts import (
    FINAL_WRITER_SYSTEM_PROMPT,
    PLANNER_SYSTEM_PROMPT,
    REVIEWER_SYSTEM_PROMPT,
    WRITER_SYSTEM_PROMPT,
    build_final_writer_prompt,
    build_planner_prompt,
    build_reviewer_prompt,
    build_writer_prompt,
)


@dataclass
class Agent:
    """A specialized AI worker with one clear responsibility."""

    name: str
    system_prompt: str
    client: OllamaClient

    def run(self, prompt: str, temperature: float = 0.7) -> str:
        print(f"\n--- {self.name} is working ---")
        return self.client.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=temperature,
        )


def run_content_pipeline(topic: str, client: OllamaClient, dry_run: bool = False) -> dict[str, str]:
    """Run planner, writer, reviewer, and final writer pass using one shared workspace."""
    workspace: dict[str, str] = {
        "topic": topic,
    }

    if dry_run:
        return run_dry_pipeline(workspace)

    planner = Agent(
        name="Planner Agent",
        system_prompt=PLANNER_SYSTEM_PROMPT,
        client=client,
    )
    writer = Agent(
        name="Writer Agent",
        system_prompt=WRITER_SYSTEM_PROMPT,
        client=client,
    )
    reviewer = Agent(
        name="Reviewer Agent",
        system_prompt=REVIEWER_SYSTEM_PROMPT,
        client=client,
    )
    final_writer = Agent(
        name="Final Writer Pass",
        system_prompt=FINAL_WRITER_SYSTEM_PROMPT,
        client=client,
    )

    workspace["plan"] = planner.run(build_planner_prompt(topic), temperature=0.4)
    workspace["draft"] = writer.run(
        build_writer_prompt(topic, workspace["plan"]),
        temperature=0.7,
    )
    workspace["review"] = reviewer.run(
        build_reviewer_prompt(topic, workspace["plan"], workspace["draft"]),
        temperature=0.3,
    )
    workspace["final_content"] = final_writer.run(
        build_final_writer_prompt(
            topic,
            workspace["plan"],
            workspace["draft"],
            workspace["review"],
        ),
        temperature=0.6,
    )

    return workspace


def run_dry_pipeline(workspace: dict[str, str]) -> dict[str, str]:
    """Create sample outputs without calling Ollama, useful for testing the app flow."""
    topic = workspace["topic"]
    print("\n--- Dry run mode: skipping Ollama calls ---")

    workspace["plan"] = f"""# Content Plan

1. Working title: A Beginner Guide to {topic}
2. Target reader: A learner who is new to the topic
3. Key message: Explain the idea clearly and make it feel practical
4. Section outline:
   - What {topic} means
   - Why it matters
   - A simple example
   - Common mistakes
   - Next steps
5. Tone: Friendly, clear, and beginner-focused
""".strip()

    workspace["draft"] = f"""# A Beginner Guide to {topic}

{topic} can feel complex at first, but it becomes easier when we break it into small parts.

## Why It Matters

This topic matters because it helps learners connect theory with practical implementation.

## Simple Example

Imagine a small project where each step has one clear responsibility. That makes the whole system easier to understand.
""".strip()

    workspace["review"] = """# Review Notes

What works well:
- The draft is beginner-friendly.
- The structure is easy to follow.

What needs improvement:
- Add a stronger introduction.
- Add more practical detail.
- End with clear next steps.
""".strip()

    workspace["final_content"] = f"""# A Beginner Guide to {topic}

When you are learning {topic}, the most important thing is to start with a simple mental model.
A good mental model helps you understand what each part does and why it belongs in the system.

## What It Means

{topic} is easier to understand when we split it into smaller responsibilities.
Each part should have a clear job, and each step should pass useful information to the next step.

## Why It Matters

This matters because real applications are rarely one single action.
They are usually a sequence of smaller decisions, checks, and improvements.
When we organize those steps clearly, the application becomes easier to build, test, and explain.

## A Simple Example

In this lab, the Planner Agent creates the direction, the Writer Agent creates the first version, and the Reviewer Agent improves the quality by giving feedback.
Then the final writer pass uses that feedback to produce a polished result.

## Next Steps

Try changing the topic, then compare the plan, draft, review, and final output.
That will help you see how each agent contributes to the final result.
""".strip()

    return workspace


def build_markdown_report(workspace: dict[str, str]) -> str:
    """Format the full shared workspace into a Markdown report."""
    sections: list[tuple[str, Callable[[], str]]] = [
        ("Topic", lambda: workspace["topic"]),
        ("Planner Agent Output", lambda: workspace["plan"]),
        ("Writer Agent First Draft", lambda: workspace["draft"]),
        ("Reviewer Agent Critique", lambda: workspace["review"]),
        ("Final Writer Pass", lambda: workspace["final_content"]),
    ]

    report = ["# Multi-Agent Content Pipeline Output"]

    for title, get_content in sections:
        report.append(f"\n## {title}\n")
        report.append(get_content().strip())

    report.append("")
    return "\n".join(report)
