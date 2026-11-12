"""Append privacy-safe processing summaries to a JSON Lines file."""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping


class AuditLogger:
    def __init__(self, path: str | Path = "audit/audit.jsonl") -> None:
        self.path = Path(path)
        self._lock = threading.Lock()

    def log_processing(
        self, entity_counts: Mapping[str, int], verified: bool
    ) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "text_processed",
            "entity_counts": dict(sorted(entity_counts.items())),
            "verified": verified,
        }
        serialized = json.dumps(record, sort_keys=True)
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as audit_file:
                audit_file.write(serialized + "\n")
