"""Reusable Streamlit UI components."""

from __future__ import annotations

from typing import Sequence

import streamlit as st

from detection.analyzer import Finding


def render_findings(findings: Sequence[Finding]) -> None:
    if not findings:
        st.success("No supported PII patterns were detected.")
        return

    st.subheader(f"Detected {len(findings)} item(s)")
    st.dataframe(
        [
            {
                "Type": finding.entity_type,
                "Detected value": finding.text,
                "Confidence": f"{finding.score:.0%}",
            }
            for finding in findings
        ],
        use_container_width=True,
        hide_index=True,
    )
