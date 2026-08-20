"""Orchestrates the Planner, Builder, and Reviewer agents."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from agents import BuilderAgent, PlannerAgent, ReviewerAgent
from audit_logger import AuditLogger
from ollama_service import OllamaService
from validators import clean_product_idea, validate_product_idea


@dataclass
class CapstoneResult:
    """Final output of one complete multi-agent run."""

    product_idea: str
    model: str
    planner_output: str
    builder_output: str
    reviewer_output: str
    audit_event_id: str = ""
    report_path: str = ""


class CapstonePipeline:
    """Runs the production-style multi-agent capstone workflow."""

    def __init__(self, llm: OllamaService | None = None, audit_logger: AuditLogger | None = None):
        self.llm = llm or OllamaService()
        self.audit_logger = audit_logger or AuditLogger()
        self.planner = PlannerAgent(self.llm)
        self.builder = BuilderAgent(self.llm)
        self.reviewer = ReviewerAgent(self.llm)

    def run(self, product_idea: str, save_report: bool = True) -> CapstoneResult:
        """Validate input, run all agents in order, and write an audit record."""
        cleaned_idea = clean_product_idea(product_idea)
        is_valid, issues = validate_product_idea(cleaned_idea)
        if not is_valid:
            raise ValueError(" ".join(issues))

        planner_result = self.planner.run(cleaned_idea)
        builder_result = self.builder.run(cleaned_idea, planner_result.output)
        reviewer_result = self.reviewer.run(
            cleaned_idea,
            planner_result.output,
            builder_result.output,
        )

        result = CapstoneResult(
            product_idea=cleaned_idea,
            model=self.llm.model,
            planner_output=planner_result.output,
            builder_output=builder_result.output,
            reviewer_output=reviewer_result.output,
        )

        run_data = asdict(result)
        audit_event_id = self.audit_logger.record_run(run_data)
        result.audit_event_id = audit_event_id

        if save_report:
            report_path = self.audit_logger.save_markdown_report(asdict(result), audit_event_id)
            result.report_path = report_path

        return result
