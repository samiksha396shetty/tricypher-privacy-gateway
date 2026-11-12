"""End-to-end detection, anonymization, and verification pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field

from audit.logger import AuditLogger
from core.anonymizer import Anonymizer
from core.token_vault import TokenVault
from core.verifier import AnonymizationVerifier, VerificationResult
from detection.analyzer import Finding, PIIAnalyzer


@dataclass(frozen=True)
class PipelineResult:
    anonymized_text: str
    findings: tuple[Finding, ...]
    verification: VerificationResult
    _vault: TokenVault = field(repr=False, compare=False)


class PrivacyPipeline:
    def __init__(
        self,
        analyzer: PIIAnalyzer | None = None,
        anonymizer: Anonymizer | None = None,
        verifier: AnonymizationVerifier | None = None,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self._analyzer = analyzer or PIIAnalyzer()
        self._anonymizer = anonymizer or Anonymizer()
        self._verifier = verifier or AnonymizationVerifier(self._analyzer)
        self._audit_logger = audit_logger

    def process(self, text: str) -> PipelineResult:
        findings = tuple(self._analyzer.analyze(text))
        vault = TokenVault()
        anonymized_text = self._anonymizer.anonymize(text, findings, vault)
        verification = self._verifier.verify(anonymized_text)

        if self._audit_logger is not None:
            self._audit_logger.log_processing(
                entity_counts=self._count_entities(findings),
                verified=verification.is_safe,
            )

        return PipelineResult(
            anonymized_text=anonymized_text,
            findings=findings,
            verification=verification,
            _vault=vault,
        )

    @staticmethod
    def _count_entities(findings: tuple[Finding, ...]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for finding in findings:
            counts[finding.entity_type] = counts.get(finding.entity_type, 0) + 1
        return counts

    @staticmethod
    def restore(text: str, result: PipelineResult) -> str:
        return result._vault.restore(text)