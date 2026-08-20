"""Streamlit AI Copilot with Ollama, human approval, voice input, and controllable voice playback."""

from __future__ import annotations

import streamlit as st

from approval_service import save_approved_output
from llm_service import DEFAULT_MODEL, OllamaError, check_ollama_health, generate_draft
from speech_service import SpeechToTextError, transcribe_audio_file
from tts_service import is_speaking, is_tts_available, speak_text, stop_speaking

st.set_page_config(
    page_title="Day 7 AI Copilot",
    page_icon="🤖",
    layout="centered",
)

EXAMPLE_PROMPT = "Write a beginner-friendly summary of what we built in this AI bootcamp."


def initialize_session_state() -> None:
    """Create the Streamlit session values used by the app."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_request" not in st.session_state:
        st.session_state.current_request = ""

    if "draft_output" not in st.session_state:
        st.session_state.draft_output = ""

    if "approval_status" not in st.session_state:
        st.session_state.approval_status = "waiting"

    if "voice_enabled" not in st.session_state:
        st.session_state.voice_enabled = True

    if "auto_read_after_generation" not in st.session_state:
        st.session_state.auto_read_after_generation = False

    if "auto_read_after_approval" not in st.session_state:
        st.session_state.auto_read_after_approval = False


def add_message(role: str, content: str) -> None:
    """Store one chat-style message in session state."""
    st.session_state.messages.append({"role": role, "content": content})


def reset_draft() -> None:
    """Clear the current draft and return to the waiting state."""
    st.session_state.current_request = ""
    st.session_state.draft_output = ""
    st.session_state.approval_status = "waiting"
    st.session_state.messages = []


def read_text_aloud(text: str) -> None:
    """Read text aloud when voice playback is enabled."""
    if not st.session_state.voice_enabled:
        st.warning("Voice playback is turned off. Enable it from the sidebar first.")
        return

    speech_message = speak_text(text)
    st.info(speech_message)


def stop_voice_playback() -> None:
    """Stop the local text-to-speech playback."""
    message = stop_speaking()
    st.info(message)


initialize_session_state()

st.title("🤖 Streamlit AI Copilot")
st.caption(
    "Speak or type a request, generate a draft with Ollama, approve it, and hear it aloud."
)

with st.sidebar:
    st.header("Copilot Settings")

    selected_model = st.text_input("Ollama model", value=DEFAULT_MODEL)

    ollama_is_ready, ollama_message = check_ollama_health()
    if ollama_is_ready:
        st.success(ollama_message)
    else:
        st.warning(ollama_message)
        st.info(
            "Start Ollama with `ollama serve`, then pull a model like "
            "`ollama pull llama3.2:3b`."
        )

    st.divider()

    st.header("Voice Features")
    st.caption("Voice input records your prompt. Voice playback reads AI output aloud.")

    voice_available = is_tts_available()

    if voice_available:
        st.session_state.voice_enabled = st.toggle(
            "Enable voice playback",
            value=st.session_state.voice_enabled,
            help="Uses local text-to-speech to read the AI output aloud.",
        )

        st.session_state.auto_read_after_generation = st.checkbox(
            "Automatically read draft after generation",
            value=st.session_state.auto_read_after_generation,
        )

        st.session_state.auto_read_after_approval = st.checkbox(
            "Automatically read approved output after saving",
            value=st.session_state.auto_read_after_approval,
        )

        st.success("Voice playback is available.")

        if st.button("⏹ Stop Reading Aloud", use_container_width=True):
            stop_voice_playback()

        if is_speaking():
            st.caption("Voice playback is currently running.")
    else:
        st.session_state.voice_enabled = False
        st.warning("Voice playback is not available on this machine.")
        st.caption("On macOS, this app uses the built-in `say` command.")

st.subheader("1. Speak or type your request")
st.info(
    "Use the microphone recorder to speak your prompt, or type directly in the text box."
)

audio_prompt = st.audio_input("Record your request")

if audio_prompt is not None:
    with st.spinner("Converting your voice input into text..."):
        try:
            transcript = transcribe_audio_file(audio_prompt)
        except SpeechToTextError as exc:
            st.error(str(exc))
        else:
            st.session_state.current_request = transcript
            st.success("Voice input converted to text.")
            st.write("Transcript:")
            st.info(transcript)

with st.form("draft_request_form", clear_on_submit=False):
    user_request = st.text_area(
        "Your input for the AI copilot",
        value=st.session_state.current_request,
        placeholder=f"Example: {EXAMPLE_PROMPT}",
        height=180,
    )

    st.caption(
        "You can edit the voice transcript before generating. "
        "The output is not saved until you approve it."
    )

    col_generate, col_clear = st.columns(2)

    with col_generate:
        generate_clicked = st.form_submit_button(
            "Generate Draft",
            type="primary",
            use_container_width=True,
        )

    with col_clear:
        clear_clicked = st.form_submit_button(
            "Clear Draft",
            use_container_width=True,
        )

if clear_clicked:
    reset_draft()
    stop_speaking()
    st.rerun()

if generate_clicked:
    if not user_request.strip():
        st.error("Please speak or type your request before generating a draft.")
    else:
        with st.spinner("Asking Ollama to create a draft..."):
            try:
                draft = generate_draft(user_request=user_request, model=selected_model)
            except ValueError as exc:
                st.error(str(exc))
            except OllamaError as exc:
                st.error(str(exc))
            else:
                st.session_state.current_request = user_request
                st.session_state.draft_output = draft
                st.session_state.approval_status = "needs_review"
                st.session_state.messages = []

                add_message("user", user_request)
                add_message("assistant", draft)

                if (
                    st.session_state.voice_enabled
                    and st.session_state.auto_read_after_generation
                ):
                    speak_text(draft)

                st.rerun()

if st.session_state.messages:
    st.subheader("2. Copilot conversation")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if st.session_state.draft_output:
    st.subheader("3. Voice playback for the draft")
    st.write("Use this when you want to hear the generated draft before approving it.")

    col_read_draft, col_stop_draft = st.columns(2)

    with col_read_draft:
        if st.button("🔊 Read Draft Aloud", use_container_width=True):
            read_text_aloud(st.session_state.draft_output)

    with col_stop_draft:
        if st.button("⏹ Stop Reading", use_container_width=True):
            stop_voice_playback()

    st.subheader("4. Human approval gate")
    st.info("The draft is not saved yet. Review it first, then approve or reject it.")

    edited_draft = st.text_area(
        "Edit the draft before approval if needed",
        value=st.session_state.draft_output,
        height=280,
    )

    col_approve, col_reject = st.columns(2)

    with col_approve:
        approve_clicked = st.button(
            "Approve and Save",
            type="primary",
            use_container_width=True,
        )

    with col_reject:
        reject_clicked = st.button(
            "Reject Draft",
            use_container_width=True,
        )

    if approve_clicked:
        saved_path = save_approved_output(
            user_request=st.session_state.current_request,
            approved_text=edited_draft,
        )

        st.session_state.draft_output = edited_draft
        st.session_state.approval_status = "approved"

        st.success(f"Approved output saved to `{saved_path}`.")

        if (
            st.session_state.voice_enabled
            and st.session_state.auto_read_after_approval
        ):
            read_text_aloud(edited_draft)

    if reject_clicked:
        stop_speaking()
        st.session_state.approval_status = "rejected"
        st.warning("Draft rejected. Nothing was saved.")

if st.session_state.approval_status == "approved":
    st.subheader("5. Voice playback for approved output")
    st.write("The approved output can be read aloud using local text-to-speech.")

    col_read_approved, col_stop_approved = st.columns(2)

    with col_read_approved:
        if st.button("🔊 Read Approved Output Aloud", use_container_width=True):
            read_text_aloud(st.session_state.draft_output)

    with col_stop_approved:
        if st.button("⏹ Stop Approved Reading", use_container_width=True):
            stop_voice_playback()

st.divider()
st.caption(
    "Final workflow: User → Voice or Text Input → Streamlit UI → Ollama → "
    "Draft → Voice Playback → Human Approval → approved_outputs.md"
)
