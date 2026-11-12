"""Load audit records for the dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_audit_records(path: str | Path = "audit/audit.jsonl") -> list[dict[str, Any]]:
    audit_path = Path(path)
    if not audit_path.exists():
        return []

    records: list[dict[str, Any]] = []
    with audit_path.open("r", encoding="utf-8") as audit_file:
        for line_number, line in enumerate(audit_file, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid audit JSON on line {line_number} of {audit_path}."
                ) from exc
            if not isinstance(record, dict):
                raise ValueError(
                    f"Audit record on line {line_number} of {audit_path} is not an object."
                )
            records.append(record)
    return records
