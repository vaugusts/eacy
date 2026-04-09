from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from apps.router.schema_loader import get_repo_root, load_json_schema, validate_against_schema


class AuditLogger:
    def __init__(self, log_path: str | Path, schema_path: str | Path | None = None) -> None:
        repo_root = get_repo_root()
        self.log_path = Path(log_path)
        self.schema_path = Path(schema_path) if schema_path else repo_root / "schemas/audit-entry.schema.json"
        self.schema = load_json_schema(self.schema_path)

    def write(self, record: dict[str, Any]) -> dict[str, Any]:
        validate_against_schema(record, self.schema, context="audit_record")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True))
            handle.write("\n")
        return record


def redact_sensitive_parameters(parameters: dict[str, Any], redact_keys: list[str]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    redact_set = set(redact_keys)
    for key, value in parameters.items():
        if key in redact_set:
            redacted[key] = "[REDACTED]"
        elif isinstance(value, dict):
            redacted[key] = redact_sensitive_parameters(value, redact_keys)
        else:
            redacted[key] = value
    return redacted


def is_within_retention_window(
    record: dict[str, Any],
    retention_days: int,
    now: datetime | None = None,
) -> bool:
    reference_time = now or datetime.now(timezone.utc)
    occurred_at = datetime.fromisoformat(record["occurred_at"].replace("Z", "+00:00"))
    return occurred_at >= reference_time - timedelta(days=retention_days)
