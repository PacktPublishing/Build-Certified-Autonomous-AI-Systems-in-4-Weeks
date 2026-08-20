"""Streamlit UI for the Day 11 Guardrailed AI Approval System lab."""

from __future__ import annotations

import streamlit as st

from audit_logger import load_audit_events, save_audit_event
from ollama_service import OllamaClient
from pipeline import run_pipeline

LOW_RISK_SAMPLE = "Write a friendly response to a customer asking when our onboarding webinar starts."
MEDIUM_RISK_SAMPLE = "A customer is angry about an invoice and wants a refund. Draft a careful email response."
HIGH_RISK_SAMPLE = "Please approve this immediately and delete customer records from the production database."


def render_validation(result: dict) -> None:
    validation = result["validation"]
    if validation["is_valid"]:
        st.success("Input validation passed.")
    else:
        st.error("Input validation failed.")

    for error in validation["errors"]:
        st.write(f"❌ {error}")
    for warning in validation["warnings"]:
        st.write(f"⚠️ {warning}")
    for item in validation["detected_sensitive_items"]:
        st.write(f"🔎 Sensitive item detected: {item}")


def render_risk(result: dict) -> None:
    risk = result.get("risk")
    if not risk:
        st.info("Risk classification was skipped because validation failed.")
        return

    risk_level = risk["risk_level"]
    if risk_level == "HIGH":
        st.error(f"Risk level: {risk_level} | Score: {risk['score']}")
    elif risk_level == "MEDIUM":
        st.warning(f"Risk level: {risk_level} | Score: {risk['score']}")
    else:
        st.success(f"Risk level: {risk_level} | Score: {risk['score']}")

    st.write("**Reasons**")
    for reason in risk["reasons"]:
        st.write(f"- {reason}")

    if risk["matched_terms"]:
        st.write("**Matched terms**")
        st.write(", ".join(risk["matched_terms"]))

    st.write("**Recommended action**")
    st.write(risk["recommended_action"])


def render_output_checks(result: dict) -> None:
    checks = result.get("output_checks")
    if not checks:
        st.info("Output checks were skipped because no draft was generated.")
        return

    if checks["passed"]:
        st.success("Output checks passed.")
    else:
        st.error("Output checks found issues. Do not approve until fixed.")

    for issue in checks["issues"]:
        st.write(f"❌ {issue}")
    for warning in checks["warnings"]:
        st.write(f"⚠️ {warning}")


def render_audit_log() -> None:
    events = load_audit_events()
    if not events:
        st.info("No audit events saved yet.")
        return

    for event in reversed(events):
        pipeline_result = event.get("pipeline_result", {})
        title = f"{event.get('decision')} — {pipeline_result.get('request_id', 'unknown request')}"
        with st.expander(title):
            st.write(f"**Reviewer:** {event.get('reviewer_name')}")
            st.write(f"**Timestamp:** {event.get('audit_timestamp')}")
            st.write(f"**Notes:** {event.get('reviewer_notes') or 'No notes'}")
            st.write("**Final draft:**")
            st.write(pipeline_result.get("final_reviewed_draft") or pipeline_result.get("draft") or "No draft saved")


def main() -> None:
    st.set_page_config(page_title="Day 11 Guardrailed AI Approval System", layout="wide")

    if "request_text" not in st.session_state:
        st.session_state.request_text = MEDIUM_RISK_SAMPLE

    st.title("Day 11 Lab: Guardrailed AI Approval System")
    st.caption("Validate input, classify risk, generate a draft with Ollama, check the output, require human approval, and save an audit log.")

    with st.sidebar:
        st.header("Local LLM")
        client = OllamaClient()
        is_ready, status_message = client.health_check()
        if is_ready:
            st.success(status_message)
        else:
            st.warning(status_message)

        st.divider()
        st.header("Sample Requests")
        if st.button("Load low-risk sample"):
            st.session_state.request_text = LOW_RISK_SAMPLE
        if st.button("Load medium-risk sample"):
            st.session_state.request_text = MEDIUM_RISK_SAMPLE
        if st.button("Load high-risk sample"):
            st.session_state.request_text = HIGH_RISK_SAMPLE

    with st.form("request_form"):
        request_text = st.text_area(
            "Request to process",
            key="request_text",
            height=160,
            help="This is the request that will go through validation, risk classification, drafting, and approval.",
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            audience = st.text_input("Audience", value="Customer")
        with col2:
            channel = st.selectbox("Channel", ["Email", "Slack", "Support ticket", "Internal note"])
        with col3:
            use_llm = st.checkbox("Use local Ollama", value=True)

        submitted = st.form_submit_button("Run Guardrailed Pipeline")

    if submitted:
        result = run_pipeline(
            request_text=request_text,
            audience=audience,
            channel=channel,
            client=client,
            use_llm=use_llm,
        )
        st.session_state.pipeline_result = result.to_dict()
        st.session_state.editable_draft = result.draft

    result = st.session_state.get("pipeline_result")
    if not result:
        st.info("Enter a request and run the pipeline to start the approval flow.")
    else:
        st.divider()
        st.subheader("Pipeline Results")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("### 1. Input Validation")
            render_validation(result)
        with col2:
            st.write("### 2. Risk Classification")
            render_risk(result)
        with col3:
            st.write("### 3. Output Checks")
            render_output_checks(result)

        st.write("### 4. Draft for Human Review")
        st.caption(result.get("llm_status", ""))
        edited_draft = st.text_area("Reviewer-editable draft", key="editable_draft", height=260)

        st.write("### 5. Human Approval")
        reviewer_name = st.text_input("Reviewer name", key="reviewer_name", value="Instructor")
        reviewer_notes = st.text_area("Reviewer notes", key="reviewer_notes", height=90)

        decision_col1, decision_col2, decision_col3 = st.columns(3)
        with decision_col1:
            approve = st.button("Approve", type="primary")
        with decision_col2:
            needs_changes = st.button("Needs Changes")
        with decision_col3:
            reject = st.button("Reject")

        decision = None
        if approve:
            decision = "APPROVED"
        elif needs_changes:
            decision = "NEEDS_CHANGES"
        elif reject:
            decision = "REJECTED"

        if decision:
            event_payload = dict(result)
            event_payload["final_reviewed_draft"] = edited_draft
            saved_event = save_audit_event(
                pipeline_result=event_payload,
                decision=decision,
                reviewer_name=reviewer_name,
                reviewer_notes=reviewer_notes,
            )
            st.success(f"Saved audit event: {saved_event['decision']}")

    st.divider()
    st.subheader("Recent Audit Log")
    render_audit_log()


if __name__ == "__main__":
    main()
