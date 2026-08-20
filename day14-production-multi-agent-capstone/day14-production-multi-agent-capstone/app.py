"""Streamlit UI for the Day 14 production multi-agent capstone."""

from __future__ import annotations

import streamlit as st

from capstone_pipeline import CapstonePipeline
from validators import validate_product_idea

SAMPLE_IDEA = """
An AI study planner for busy working professionals. The user enters their goal,
available time, and deadline. The app creates a weekly study plan, identifies
risks, and recommends a realistic first milestone.
""".strip()


st.set_page_config(page_title="Production Multi-Agent Capstone", page_icon="🤖", layout="wide")

st.title("Production Multi-Agent Capstone")
st.caption("Day 14 Lab — Planner Agent, Builder Agent, Reviewer Agent, and local Ollama")

with st.sidebar:
    st.header("Agent Flow")
    st.write("1. Planner Agent breaks the product idea into steps.")
    st.write("2. Builder Agent creates the first implementation plan.")
    st.write("3. Reviewer Agent reviews the plan and suggests fixes.")
    st.divider()
    st.write("Local model: `llama3.2:1b` through Ollama")

product_idea = st.text_area(
    "Product idea",
    value=SAMPLE_IDEA,
    height=180,
    help="Describe the product, target user, and problem it solves.",
)

run_button = st.button("Run Multi-Agent Capstone", type="primary")

if run_button:
    is_valid, issues = validate_product_idea(product_idea)
    if not is_valid:
        for issue in issues:
            st.error(issue)
    else:
        with st.spinner("Running Planner, Builder, and Reviewer agents..."):
            try:
                pipeline = CapstonePipeline()
                result = pipeline.run(product_idea)
                st.session_state["capstone_result"] = result
            except Exception as exc:  # noqa: BLE001 - friendly UI message for lab learners
                st.error(str(exc))

result = st.session_state.get("capstone_result")

if result:
    st.success(f"Run complete. Audit event: {result.audit_event_id}")
    if result.report_path:
        st.info(f"Markdown report saved to: {result.report_path}")

    planner_tab, builder_tab, reviewer_tab = st.tabs(
        ["Planner Agent", "Builder Agent", "Reviewer Agent"]
    )

    with planner_tab:
        st.markdown(result.planner_output)

    with builder_tab:
        st.markdown(result.builder_output)

    with reviewer_tab:
        st.markdown(result.reviewer_output)

else:
    st.info("Enter a product idea and run the agents to generate the capstone plan.")
