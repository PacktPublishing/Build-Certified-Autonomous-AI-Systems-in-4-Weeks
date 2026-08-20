"""Prompt templates for the Day 14 multi-agent capstone lab."""

PLANNER_SYSTEM_PROMPT = """
You are the Planner Agent in a production-style multi-agent AI system.
Your job is to break a product idea into a clear, practical execution plan.
Be specific, beginner-friendly, and realistic.
""".strip()

BUILDER_SYSTEM_PROMPT = """
You are the Builder Agent in a production-style multi-agent AI system.
Your job is to turn the planner's steps into a first implementation plan.
Focus on files, components, data flow, and a sensible build order.
""".strip()

REVIEWER_SYSTEM_PROMPT = """
You are the Reviewer Agent in a production-style multi-agent AI system.
Your job is to review the implementation plan before a human uses it.
Look for missing safety checks, unclear steps, unrealistic assumptions, and beginner confusion.
Suggest concrete fixes.
""".strip()


def build_planner_prompt(product_idea: str) -> str:
    """Create the prompt for the Planner Agent."""
    return f"""
Product idea:
{product_idea}

Create a planning response with these sections:

## Goal
Explain the product in one simple paragraph.

## User Workflow
List the steps a user would follow.

## System Steps
Break the product into 5 to 8 technical steps.

## Risks And Guardrails
List practical risks and how the app should handle them.

## Definition Of Done
List what must work for the first version to be considered complete.
""".strip()


def build_builder_prompt(product_idea: str, planner_output: str) -> str:
    """Create the prompt for the Builder Agent."""
    return f"""
Product idea:
{product_idea}

Planner Agent output:
{planner_output}

Create a first implementation plan with these sections:

## Recommended Project Structure
Show the key files and folders.

## Build Order
Explain which files should be built first, second, third, and why.

## Core Functions
List the main functions or classes each file should contain.

## Data Flow
Explain how input moves through the system.

## Demo Script
Give a simple demo flow a learner can record.
""".strip()


def build_reviewer_prompt(product_idea: str, planner_output: str, builder_output: str) -> str:
    """Create the prompt for the Reviewer Agent."""
    return f"""
Product idea:
{product_idea}

Planner Agent output:
{planner_output}

Builder Agent output:
{builder_output}

Review the plan with these sections:

## Overall Verdict
Say whether this is ready, almost ready, or needs changes.

## What Works Well
List the strongest parts of the plan.

## Gaps Or Risks
List anything missing, unclear, unsafe, or too advanced.

## Required Fixes
Give concrete fixes before implementation.

## Final Recommendation
Give the next best action for the human builder.
""".strip()
