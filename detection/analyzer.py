"""Rule-based PII detection for common identifiers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

from detection.custom_recognizers import CUSTOM_RECOGNIZERS
from detection.validators import (
    is_valid_credit_card,
    is_valid_email,
    is_valid_ip_address,
    is_valid_phone,
    is_valid_ssn,
)


@dataclass(frozen=True)
class Finding:
    entity_type: str
    start: int
    end: int
    text: str
    score: float


@dataclass(frozen=True)
class _Recognizer:
    entity_type: str
    pattern: re.Pattern[str]
    validator: Callable[[str], bool]
    score: float


class PIIAnalyzer:
    """Detect common PII locally without sending text to an external service."""

    def __init__(self) -> None:
        recognizers = [
            _Recognizer(
                "EMAIL",
                re.compile(
                    r"(?<![\w.+-])[\w.!#$%&'*+/=?^`{|}~-]+@"
                    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
                    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+"
                ),
                is_valid_email,
                0.99,
            ),
            _Recognizer(
                "SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), is_valid_ssn, 0.99
            ),
            _Recognizer(
                "CREDIT_CARD",
                re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)"),
                is_valid_credit_card,
                0.98,
            ),
            _Recognizer(
                "IP_ADDRESS",
                re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
                is_valid_ip_address,
                0.90,
            ),
            _Recognizer(
                "PHONE",
                re.compile(
                    r"(?<!\w)(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)"
                    r"\d{3}[\s.-]?\d{4}(?!\w)"
                ),
                is_valid_phone,
                0.85,
            ),
        ]
        recognizers.extend(
            _Recognizer(
                item["entity_type"],
                re.compile(item["pattern"], re.IGNORECASE),
                item["validator"],
                item["score"],
            )
            for item in CUSTOM_RECOGNIZERS
        )
        self._recognizers = recognizers

    def analyze(self, text: str) -> list[Finding]:
        candidates: list[Finding] = []
        for recognizer in self._recognizers:
            for match in recognizer.pattern.finditer(text):
                value = match.group()
                if recognizer.validator(value):
                    candidates.append(
                        Finding(
                            entity_type=recognizer.entity_type,
                            start=match.start(),
                            end=match.end(),
                            text=value,
                            score=recognizer.score,
                        )
                    )

        candidates.sort(key=lambda finding: (finding.start, -finding.score, -finding.end))
        selected: list[Finding] = []
        occupied_until = -1
        for finding in candidates:
            if finding.start < occupied_until:
                continue
            selected.append(finding)
            occupied_until = finding.end
        return selected
