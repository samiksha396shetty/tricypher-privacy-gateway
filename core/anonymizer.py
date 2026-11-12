"""Replace detected sensitive values with reversible, request-scoped tokens."""

from __future__ import annotations

from typing import Iterable

from core.token_vault import TokenVault
from detection.analyzer import Finding


class Anonymizer:
    """Anonymize text using findings produced by :class:`PIIAnalyzer`."""

    def anonymize(
        self, text: str, findings: Iterable[Finding], vault: TokenVault
    ) -> str:
        ordered_findings = sorted(findings, key=lambda item: (item.start, item.end))
        parts: list[str] = []
        cursor = 0

        for finding in ordered_findings:
            if finding.start < cursor:
                continue
            parts.append(text[cursor : finding.start])
            parts.append(vault.token_for(finding.entity_type, finding.text))
            cursor = finding.end

        parts.append(text[cursor:])
        return "".join(parts)