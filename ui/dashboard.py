"""Streamlit dashboard for the TriCypher privacy gateway."""

from __future__ import annotations

import streamlit as st

from audit.audit_view import load_audit_records
from audit.logger import AuditLogger
from core.llm_service import LLMService
from core.pipeline import PipelineResult, PrivacyPipeline
from ui.components import render_findings


def _process_input(text: str) -> PipelineResult:
    return PrivacyPipeline(audit_logger=AuditLogger()).process(text)


def render_dashboard() -> None:
    st.set_page_config(page_title="TriCypher Privacy Gateway", page_icon="🔐")
    st.title("TriCypher Privacy Gateway")
    st.caption(
        "Detect and replace common identifiers locally before sharing text with an LLM."
    )

    tab_analyze, tab_audit = st.tabs(["Analyze text", "Audit log"])
    with tab_analyze:
        source_text = st.text_area(
            "Text to protect",
            height=220,
            placeholder="Paste text containing identifiers you want to protect.",
        )
        user_request = st.text_input(
            "Optional LLM request",
            placeholder="For example: Summarize the protected text",
        )
        combined_text = (
            f"Request: {user_request}\n\nText:\n{source_text}"
            if user_request
            else source_text
        )

        if st.button("Detect and anonymize", type="primary"):
            if not combined_text.strip():
                st.warning("Enter text or an LLM request first.")
            else:
                st.session_state["pipeline_result"] = _process_input(combined_text)
                st.session_state["processed_input"] = combined_text

        result = st.session_state.get("pipeline_result")
        if isinstance(result, PipelineResult):
            if st.session_state.get("processed_input") != combined_text:
                st.info("Input changed. Detect and anonymize it again before continuing.")
            else:
                render_findings(result.findings)
                st.subheader("Anonymized text")
                st.code(result.anonymized_text, language=None)
                if result.verification.is_safe:
                    st.success("Verification passed: no supported PII patterns remain.")
                else:
                    st.error(
                        f"Verification found {len(result.verification.residual_findings)} "
                        "possible residual item(s). Do not send this text to an LLM."
                    )

                service = LLMService()
                if user_request:
                    if st.button(
                        "Send anonymized text to LLM",
                        disabled=(
                            not result.verification.is_safe or not service.is_configured
                        ),
                    ):
                        try:
                            with st.spinner("Waiting for the LLM response..."):
                                response = service.complete(result.anonymized_text)
                        except (RuntimeError, ValueError) as exc:
                            st.error(str(exc))
                        else:
                            st.subheader("LLM response")
                            st.write(PrivacyPipeline.restore(response, result))
                    if not service.is_configured:
                        st.info("Set LLM_API_KEY in your environment to enable the LLM.")
                    st.caption(
                        "Only verified anonymized text is sent. The LLM provider may "
                        "retain requests according to its own policies."
                    )

    with tab_audit:
        st.caption("Audit records contain timestamps and entity counts, not source text.")
        records = load_audit_records()
        if records:
            st.dataframe(records, use_container_width=True, hide_index=True)
        else:
            st.info("No audit records yet.")
