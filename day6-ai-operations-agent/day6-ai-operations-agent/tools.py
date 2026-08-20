"""Tool functions for the Day 6 AI Operations Agent lab.

In this lab, tools are plain Python functions. The LLM does not execute code.
It only decides which tool should be used. Python stays in control and calls
one safe function from this file.
"""

from __future__ import annotations

import ast
import operator
import platform
from datetime import datetime
from typing import Any


# A small in-memory ticket database keeps the lab simple and repeatable.
TICKETS: dict[str, dict[str, str]] = {
    "INC1001": {
        "title": "Payment service latency",
        "status": "Open",
        "priority": "High",
        "owner": "Operations Team",
        "last_update": "Database connection pool is close to saturation.",
    },
    "INC1002": {
        "title": "Password reset emails delayed",
        "status": "In Progress",
        "priority": "Medium",
        "owner": "Identity Team",
        "last_update": "Email provider retry queue is draining slowly.",
    },
    "INC1003": {
        "title": "Dashboard page returning 500 errors",
        "status": "Resolved",
        "priority": "High",
        "owner": "Web Platform Team",
        "last_update": "Bad release was rolled back and monitoring is green.",
    },
}


ALLOWED_OPERATORS: dict[type[ast.operator], Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

ALLOWED_UNARY_OPERATORS: dict[type[ast.unaryop], Any] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_math_node(node: ast.AST) -> float:
    """Safely evaluate a basic arithmetic expression AST node."""

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
        left = _evaluate_math_node(node.left)
        right = _evaluate_math_node(node.right)
        return ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_UNARY_OPERATORS:
        operand = _evaluate_math_node(node.operand)
        return ALLOWED_UNARY_OPERATORS[type(node.op)](operand)

    raise ValueError("Only basic arithmetic is supported.")


def calculator_tool(expression: str) -> dict[str, Any]:
    """Evaluate a safe arithmetic expression such as '42 * 3 + 10'."""

    try:
        parsed = ast.parse(expression, mode="eval")
        result = _evaluate_math_node(parsed.body)
        return {
            "tool": "calculator",
            "expression": expression,
            "result": result,
        }
    except Exception as exc:
        return {
            "tool": "calculator",
            "expression": expression,
            "error": str(exc),
        }


def ticket_lookup_tool(ticket_id: str) -> dict[str, Any]:
    """Look up an operations ticket by ID."""

    normalized_ticket_id = ticket_id.strip().upper()
    ticket = TICKETS.get(normalized_ticket_id)

    if ticket is None:
        return {
            "tool": "ticket_lookup",
            "ticket_id": normalized_ticket_id,
            "error": "Ticket was not found. Try INC1001, INC1002, or INC1003.",
        }

    return {
        "tool": "ticket_lookup",
        "ticket_id": normalized_ticket_id,
        **ticket,
    }


def system_status_tool(service_name: str = "core platform") -> dict[str, Any]:
    """Return a simple mock system health report for a service."""

    service = service_name.strip() or "core platform"
    return {
        "tool": "system_status",
        "service_name": service,
        "overall_status": "Healthy",
        "cpu_usage": "31%",
        "memory_usage": "58%",
        "open_incidents": 1,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "machine": platform.system(),
        "note": "This is a safe mock status report for the course lab.",
    }


def summary_writer_tool(text: str) -> dict[str, Any]:
    """Create a short operational summary from the provided text."""

    cleaned_text = " ".join(text.split())
    sentences = [part.strip() for part in cleaned_text.replace("?", ".").replace("!", ".").split(".") if part.strip()]
    main_point = sentences[0] if sentences else cleaned_text[:160]

    return {
        "tool": "summary_writer",
        "original_length": len(text),
        "summary": main_point[:220],
        "bullet_points": sentences[:3],
    }


def run_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Route a tool name and JSON arguments to the correct Python function."""

    if tool_name == "calculator":
        return calculator_tool(str(arguments.get("expression", "")))

    if tool_name == "ticket_lookup":
        return ticket_lookup_tool(str(arguments.get("ticket_id", "")))

    if tool_name == "system_status":
        return system_status_tool(str(arguments.get("service_name", "core platform")))

    if tool_name == "summary_writer":
        return summary_writer_tool(str(arguments.get("text", "")))

    return {
        "tool": tool_name,
        "error": "Unknown tool. Allowed tools are calculator, ticket_lookup, system_status, and summary_writer.",
    }


def tool_catalog() -> list[dict[str, Any]]:
    """Describe the available tools for the LLM prompt."""

    return [
        {
            "name": "calculator",
            "description": "Use for arithmetic calculations.",
            "arguments": {"expression": "math expression as a string"},
        },
        {
            "name": "ticket_lookup",
            "description": "Use when the user asks about an operations ticket or incident ID.",
            "arguments": {"ticket_id": "ticket ID such as INC1001"},
        },
        {
            "name": "system_status",
            "description": "Use when the user asks for health or status of a service or system.",
            "arguments": {"service_name": "service or system name"},
        },
        {
            "name": "summary_writer",
            "description": "Use when the user asks to summarize text.",
            "arguments": {"text": "text to summarize"},
        },
    ]
