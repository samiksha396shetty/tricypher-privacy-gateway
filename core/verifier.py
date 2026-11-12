"""Check that anonymized text no longer contains recognized sensitive values."""

from __future__ import annotations

from dataclasses import dataclass

from detection.analyzer import Finding, PIIAnalyzer


@dataclass(frozen=True)
class VerificationResult:
    is_safe: bool
    residual_findings: tuple[Finding, ...]


class AnonymizationVerifier:
    def __init__(self, analyzer: PIIAnalyzer | None = None) -> None:
        self._analyzer = analyzer or PIIAnalyzer()

    def verify(self, anonymized_text: str) -> VerificationResult:
        residuals = tuple(self._analyzer.analyze(anonymized_text))
        return VerificationResult(
            is_safe=not residuals,
            residual_findings=residuals,
        )