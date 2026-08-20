"""Streamlit UI for the Day 6 AI Operations Agent lab."""

from __future__ import annotations

import json

import streamlit as st

from agent import run_operations_agent
from llm_service import OLLAMA_BASE_URL, OLLAMA_MODEL, OllamaError
from tools import TICKETS, tool_catalog


st.set_page_config(
    page_title="Day 6 AI Operations Agent",
    page_icon="🛠️",
    layout="wide",
)

st.title("Day 6 Lab: AI Operations Agent")
st.caption("Ollama decides the tool. Python runs the tool. Ollama writes the final answer.")

with st.sidebar:
    st.header("Local Ollama")
    st.write(f"**Model:** `{OLLAMA_MODEL}`")
    st.write(f"**Base URL:** `{OLLAMA_BASE_URL}`")

    st.header("Available tools")
    for tool in tool_catalog():
        st.markdown(f"- **{tool['name']}** — {tool['description']}")

    st.header("Demo tickets")
    st.write(", ".join(TICKETS.keys()))

sample_requests = [
    "What is 42 * 8 + 17?",
    "Look up ticket INC1002.",
    "Check the status of the payment service.",
    "Summarize this: The payment service had high latency this morning. The team increased the database connection pool. Monitoring is now stable.",
]

selected_sample = st.selectbox("Try a sample request", sample_requests)
user_request = st.text_area(
    "User request",
    value=selected_sample,
    height=120,
    help="Ask for a calculation, ticket lookup, system status, or summary.",
)

run_button = st.button("Run AI Operations Agent", type="primary")

if run_button:
    if not user_request.strip():
        st.warning("Please enter a request first.")
    else:
        with st.spinner("Asking Ollama to choose a tool and write the final answer..."):
            try:
                response = run_operations_agent(user_request.strip())
            except OllamaError as exc:
                st.error(str(exc))
                st.info("Run `ollama serve` and `ollama pull llama3.2:3b`, or change OLLAMA_MODEL in your .env file.")
            except Exception as exc:  # A friendly guard for live demos.
                st.error(f"Something went wrong: {exc}")
            else:
                st.subheader("Final answer")
                st.success(response.final_answer)

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("1. Ollama tool decision")
                    st.code(json.dumps(response.decision, indent=2), language="json")

                with col2:
                    st.subheader("2. Python tool result")
                    st.code(json.dumps(response.tool_result, indent=2), language="json")

                with st.expander("Full architecture trace"):
                    st.markdown(
                        """
1. The user enters a request.
2. Ollama returns structured JSON with a tool name and arguments.
3. Python routes the request to one safe function.
4. The tool result is sent back to Ollama.
5. Ollama writes a user-friendly final answer.
"""
                    )
