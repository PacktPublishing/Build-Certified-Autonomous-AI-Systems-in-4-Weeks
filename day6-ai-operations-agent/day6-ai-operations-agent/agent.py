"""Agent orchestration for the Day 6 AI Operations Agent lab."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from llm_service import decide_tool, write_final_answer
from tools import run_tool, tool_catalog


@dataclass
class AgentResponse:
    """The full trace of one agent run."""

    user_request: str
    decision: dict[str, Any]
    tool_result: dict[str, Any]
    final_answer: str


def run_operations_agent(user_request: str) -> AgentResponse:
    """Run the full agent flow from user request to final answer."""

    tools = tool_catalog()

    decision = decide_tool(user_request=user_request, tools=tools)
    tool_name = decision["tool_name"]
    arguments = decision["arguments"]

    tool_result = run_tool(tool_name=tool_name, arguments=arguments)
    final_answer = write_final_answer(user_request=user_request, tool_result=tool_result)

    return AgentResponse(
        user_request=user_request,
        decision=decision,
        tool_result=tool_result,
        final_answer=final_answer,
    )
