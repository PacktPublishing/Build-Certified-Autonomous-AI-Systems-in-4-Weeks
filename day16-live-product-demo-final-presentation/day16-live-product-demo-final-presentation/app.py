"""Streamlit app for Day 16: Live Product Demo and Final Presentation.

The app uses Ollama as a local demo coach. Learners describe their final product,
then generate four Markdown assets for their final presentation.
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from file_writer import OUTPUT_FILENAMES, save_assets
from ollama_service import OllamaService
from presentation_pipeline import ProductDemoContext, generate_presentation_assets


load_dotenv()

PROJECT_DIR = Path(__file__).parent
SAMPLE_BRIEF_PATH = PROJECT_DIR / "samples" / "sample_product_brief.md"
OUTPUT_DIR = PROJECT_DIR / "outputs"


st.set_page_config(
    page_title="Day 16 Final Demo Coach",
    page_icon="🎤",
    layout="wide",
)


@st.cache_data
def load_sample_brief() -> str:
    """Load the sample product brief shown in the text area."""
    return SAMPLE_BRIEF_PATH.read_text(encoding="utf-8")


def build_context_from_form() -> ProductDemoContext:
    """Collect form values and turn them into a pipeline context."""
    return ProductDemoContext(
        product_name=st.session_state.product_name,
        one_line_idea=st.session_state.one_line_idea,
        target_user=st.session_state.target_user,
        problem=st.session_state.problem,
        built_features=st.session_state.built_features,
        demo_flow=st.session_state.demo_flow,
        strongest_demo_moment=st.session_state.strongest_demo_moment,
        known_weak_spots=st.session_state.known_weak_spots,
        launch_goal=st.session_state.launch_goal,
        extra_notes=st.session_state.extra_notes,
    )


def render_asset_tabs(assets: dict[str, str]) -> None:
    """Show generated assets in tabs with download buttons."""
    tab_labels = [
        "Final Demo Script",
        "Judge Rubric",
        "Launch Post",
        "Improvement Plan",
    ]
    asset_keys = list(OUTPUT_FILENAMES.keys())
    tabs = st.tabs(tab_labels)

    for tab, asset_key in zip(tabs, asset_keys):
        filename = OUTPUT_FILENAMES[asset_key]
        content = assets[asset_key]
        with tab:
            st.download_button(
                label=f"Download {filename}",
                data=content,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True,
            )
            st.markdown(content)


st.title("🎤 Day 16 Lab: Live Product Demo and Final Presentation")
st.caption("Use Ollama as a local demo coach to prepare the final presentation assets.")

with st.sidebar:
    st.header("Ollama Settings")
    model = st.text_input("Model", value=os.getenv("OLLAMA_MODEL", "llama3.2"))
    base_url = st.text_input(
        "Base URL",
        value=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )

    if st.button("Check Ollama", use_container_width=True):
        try:
            service = OllamaService(model=model, base_url=base_url)
            st.success(service.health_check())
        except RuntimeError as error:
            st.error(str(error))

st.markdown(
    """
This final lab helps you prepare the assets you need for a confident product demo:

- `final_demo_script.md`
- `judge_rubric.md`
- `launch_post.md`
- `improvement_plan.md`
"""
)

with st.form("demo_context_form"):
    col_left, col_right = st.columns(2)

    with col_left:
        st.text_input(
            "Product name",
            value="StudySprint AI",
            key="product_name",
        )
        st.text_area(
            "One-line idea",
            value="An AI study coach that turns one topic into a study plan, quiz, and improvement checklist.",
            key="one_line_idea",
            height=90,
        )
        st.text_area(
            "Target user",
            value="Busy beginners who want a focused way to study one topic at a time.",
            key="target_user",
            height=90,
        )
        st.text_area(
            "Problem",
            value="Learners often do not know where to start, what to practice, or how to judge whether they understood the topic.",
            key="problem",
            height=120,
        )

    with col_right:
        st.text_area(
            "Core features built",
            value="- Topic input\n- Study plan generator\n- Quiz generator\n- Feedback and next-step suggestions\n- Markdown export",
            key="built_features",
            height=120,
        )
        st.text_area(
            "Demo flow",
            value="1. Open the app.\n2. Enter a topic.\n3. Generate a study plan.\n4. Generate quiz questions.\n5. Review the improvement checklist.\n6. Export the final study guide.",
            key="demo_flow",
            height=140,
        )
        st.text_area(
            "Strongest demo moment",
            value="The app turns one small topic into a complete learning package in seconds.",
            key="strongest_demo_moment",
            height=90,
        )
        st.text_area(
            "Known weak spots",
            value="The first version does not track long-term progress yet, and the quiz difficulty is basic.",
            key="known_weak_spots",
            height=90,
        )

    st.text_area(
        "Launch goal",
        value="Share the app with early learners, collect feedback, and decide what to improve in the next version.",
        key="launch_goal",
        height=90,
    )
    st.text_area(
        "Extra notes or pasted product brief",
        value=load_sample_brief(),
        key="extra_notes",
        height=220,
    )

    submitted = st.form_submit_button("Generate Final Presentation Assets", use_container_width=True)

if submitted:
    ollama = OllamaService(model=model, base_url=base_url)
    context = build_context_from_form()

    try:
        with st.spinner("Ollama is coaching the final demo and writing the Markdown assets..."):
            assets = generate_presentation_assets(context=context, ollama=ollama)
            saved_files = save_assets(assets, output_dir=OUTPUT_DIR)

        st.success("Generated and saved all final presentation assets.")
        st.write("Saved files:")
        for asset_key, path in saved_files.items():
            st.code(str(path), language="text")

        render_asset_tabs(assets)
    except RuntimeError as error:
        st.error(str(error))
        st.info("Make sure Ollama is running and the selected model is available locally.")
else:
    st.info("Fill in the product details, then generate the final demo package.")
