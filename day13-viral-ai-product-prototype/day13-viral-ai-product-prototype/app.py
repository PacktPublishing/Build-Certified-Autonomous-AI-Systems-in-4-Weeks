"""Streamlit app for Day 13: Viral AI Product Prototype."""

from __future__ import annotations

import json

import streamlit as st

from file_service import load_saved_outputs
from idea_pipeline import generate_product_ideas
from ollama_service import OllamaClient

SAMPLE_TARGET_USER = "Busy course creators who need to turn rough lesson ideas into polished lab plans"
SAMPLE_PAINFUL_WORKFLOW = "They have messy notes, scattered feature ideas, and no clear structure for what the student should build in the lab."
SAMPLE_DESIRED_OUTPUT = "A clear product brief with product name, target user, painful workflow, features, score, and capstone-ready plan."


def render_idea_card(idea: dict, rank: int) -> None:
    scores = idea.get("scores", {})
    with st.container(border=True):
        st.subheader(f"#{rank}: {idea.get('name', 'Untitled Idea')}")
        st.write(idea.get("one_liner", ""))

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total", scores.get("total", "N/A"))
        col2.metric("Clarity", scores.get("clarity", "N/A"))
        col3.metric("Pain", scores.get("pain_strength", "N/A"))
        col4.metric("Share", scores.get("shareability", "N/A"))
        col5.metric("Build", scores.get("capstone_buildability", "N/A"))

        st.write("**Target user**")
        st.write(idea.get("target_user", ""))

        st.write("**Painful workflow**")
        st.write(idea.get("painful_workflow", ""))

        st.write("**Main output**")
        st.write(idea.get("main_output", ""))

        st.write("**Why it could spread**")
        st.write(idea.get("why_it_could_spread", ""))

        st.write("**Prototype features**")
        for feature in idea.get("prototype_features", []):
            st.write(f"- {feature}")

        st.write("**Capstone fit**")
        st.write(idea.get("capstone_fit", ""))


def main() -> None:
    st.set_page_config(page_title="Day 13 Viral AI Product Prototype", layout="wide")

    if "target_user" not in st.session_state:
        st.session_state.target_user = SAMPLE_TARGET_USER
    if "painful_workflow" not in st.session_state:
        st.session_state.painful_workflow = SAMPLE_PAINFUL_WORKFLOW
    if "desired_output" not in st.session_state:
        st.session_state.desired_output = SAMPLE_DESIRED_OUTPUT

    st.title("Day 13 Lab: Viral AI Product Prototype")
    st.caption("Turn a messy idea into 3 scored product ideas, then save the best one as a capstone-ready product brief.")

    with st.sidebar:
        st.header("Local LLM")
        client = OllamaClient()
        is_ready, status_message = client.health_check()
        if is_ready:
            st.success(status_message)
        else:
            st.warning(status_message)

        st.divider()
        st.header("Demo Controls")
        if st.button("Load course creator sample"):
            st.session_state.target_user = SAMPLE_TARGET_USER
            st.session_state.painful_workflow = SAMPLE_PAINFUL_WORKFLOW
            st.session_state.desired_output = SAMPLE_DESIRED_OUTPUT

        st.write("Generated files:")
        st.code("product_ideas.json\nproduct_brief.md")

    with st.form("idea_form"):
        target_user = st.text_input("Target user", key="target_user")
        painful_workflow = st.text_area("Painful workflow", key="painful_workflow", height=130)
        desired_output = st.text_area("What output should the user get?", key="desired_output", height=110)

        col1, col2 = st.columns([1, 1])
        with col1:
            use_llm = st.checkbox("Use local Ollama", value=True)
        with col2:
            save_outputs = st.checkbox("Save best idea and product brief", value=True)

        submitted = st.form_submit_button("Generate Product Ideas", type="primary")

    if submitted:
        result = generate_product_ideas(
            target_user=target_user,
            painful_workflow=painful_workflow,
            desired_output=desired_output,
            client=client,
            use_llm=use_llm,
            save_outputs=save_outputs,
        )
        st.session_state.result = result.to_dict()

    result = st.session_state.get("result")
    if not result:
        st.info("Fill in the three inputs and generate product ideas to begin.")
    else:
        st.divider()
        if not result["is_valid"]:
            st.error("Please fix the input errors before generating ideas.")
            for error in result["errors"]:
                st.write(f"- {error}")
            return

        st.success(result["llm_status"])
        if result["saved_files"]:
            st.write("Saved files: " + ", ".join(result["saved_files"]))

        st.header("Generated Product Ideas")
        for index, idea in enumerate(result["ideas"], start=1):
            render_idea_card(idea, index)

        st.header("Best Idea for Final Capstone")
        best_idea = result.get("best_idea") or {}
        st.success(f"Recommended: {best_idea.get('name', 'Untitled Idea')}")

        st.subheader("Generated product_brief.md")
        st.download_button(
            label="Download product_brief.md",
            data=result["product_brief"],
            file_name="product_brief.md",
            mime="text/markdown",
        )
        st.code(result["product_brief"], language="markdown")

    st.divider()
    st.header("Saved Output Preview")
    ideas_payload, brief = load_saved_outputs()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("product_ideas.json")
        if ideas_payload:
            st.code(json.dumps(ideas_payload, indent=2), language="json")
        else:
            st.info("No product ideas saved yet.")
    with col2:
        st.subheader("product_brief.md")
        if brief.strip():
            st.code(brief, language="markdown")
        else:
            st.info("No product brief saved yet.")


if __name__ == "__main__":
    main()
