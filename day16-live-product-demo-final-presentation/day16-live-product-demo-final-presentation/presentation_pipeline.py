"""Pipeline that turns one product brief into final presentation assets."""

from __future__ import annotations

from dataclasses import dataclass

from ollama_service import OllamaService
from prompt_templates import (
    final_demo_script_prompt,
    improvement_plan_prompt,
    judge_rubric_prompt,
    launch_post_prompt,
)


@dataclass
class ProductDemoContext:
    """Structured information about the product being presented."""

    product_name: str
    one_line_idea: str
    target_user: str
    problem: str
    built_features: str
    demo_flow: str
    strongest_demo_moment: str
    known_weak_spots: str
    launch_goal: str
    extra_notes: str = ""

    def to_markdown(self) -> str:
        """Convert the context into clean Markdown for the prompts."""
        return f"""
# Product Demo Context

## Product Name
{self.product_name}

## One-Line Idea
{self.one_line_idea}

## Target User
{self.target_user}

## Problem
{self.problem}

## Core Features Built
{self.built_features}

## Demo Flow
{self.demo_flow}

## Strongest Demo Moment
{self.strongest_demo_moment}

## Known Weak Spots
{self.known_weak_spots}

## Launch Goal
{self.launch_goal}

## Extra Notes
{self.extra_notes or "No extra notes provided."}
""".strip()


def build_default_context(product_brief: str) -> ProductDemoContext:
    """Create a useful context object from a free-form product brief."""
    return ProductDemoContext(
        product_name="Final Capstone Product",
        one_line_idea="An AI product prepared for a final live demo.",
        target_user="Early users and final presentation reviewers.",
        problem="The presenter needs a clear, confident way to explain the product and ask for feedback.",
        built_features="See the pasted product brief for project-specific features.",
        demo_flow="Walk through the main app flow from input, to AI processing, to final output.",
        strongest_demo_moment="The product turns a messy user need into a useful AI-generated result.",
        known_weak_spots="This is an early version and still needs real user feedback.",
        launch_goal="Present the product clearly, collect feedback, and plan the next improvement cycle.",
        extra_notes=product_brief,
    )


def generate_presentation_assets(
    context: ProductDemoContext,
    ollama: OllamaService,
) -> dict[str, str]:
    """Generate all four final Markdown assets with Ollama."""
    product_brief = context.to_markdown()

    return {
        "final_demo_script": ollama.generate(final_demo_script_prompt(product_brief)),
        "judge_rubric": ollama.generate(judge_rubric_prompt(product_brief)),
        "launch_post": ollama.generate(launch_post_prompt(product_brief)),
        "improvement_plan": ollama.generate(improvement_plan_prompt(product_brief)),
    }
