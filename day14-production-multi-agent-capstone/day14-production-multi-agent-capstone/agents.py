"""Agent classes for the Day 14 production multi-agent capstone."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from ollama_service import OllamaService
from prompt_templates import (
    BUILDER_SYSTEM_PROMPT,
    PLANNER_SYSTEM_PROMPT,
    REVIEWER_SYSTEM_PROMPT,
    build_builder_prompt,
    build_planner_prompt,
    build_reviewer_prompt,
)


@dataclass
class AgentResult:
    """Standard result returned by every agent."""

    agent_name: str
    role: str
    output: str


class BaseAgent:
    """Base class that keeps agent execution consistent."""

    def __init__(self, name: str, role: str, system_prompt: str, llm: OllamaService):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.llm = llm

    def run_prompt(self, prompt: str) -> AgentResult:
        """Run a prepared prompt through the local model."""
        output = self.llm.generate(prompt=prompt, system_prompt=self.system_prompt)
        return AgentResult(agent_name=self.name, role=self.role, output=output)


class PlannerAgent(BaseAgent):
    """Breaks the product idea into practical steps."""

    def __init__(self, llm: OllamaService):
        super().__init__(
            name="Planner Agent",
            role="Break the product idea into steps",
            system_prompt=PLANNER_SYSTEM_PROMPT,
            llm=llm,
        )

    def run(self, product_idea: str) -> AgentResult:
        prompt = build_planner_prompt(product_idea)
        return self.run_prompt(prompt)


class BuilderAgent(BaseAgent):
    """Creates the first implementation plan."""

    def __init__(self, llm: OllamaService):
        super().__init__(
            name="Builder Agent",
            role="Create the first implementation plan",
            system_prompt=BUILDER_SYSTEM_PROMPT,
            llm=llm,
        )

    def run(self, product_idea: str, planner_output: str) -> AgentResult:
        prompt = build_builder_prompt(product_idea, planner_output)
        return self.run_prompt(prompt)


class ReviewerAgent(BaseAgent):
    """Reviews the plan and suggests fixes."""

    def __init__(self, llm: OllamaService):
        super().__init__(
            name="Reviewer Agent",
            role="Review the plan and suggest fixes",
            system_prompt=REVIEWER_SYSTEM_PROMPT,
            llm=llm,
        )

    def run(self, product_idea: str, planner_output: str, builder_output: str) -> AgentResult:
        prompt = build_reviewer_prompt(product_idea, planner_output, builder_output)
        return self.run_prompt(prompt)
