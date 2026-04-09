import json
import tempfile
import unittest
from pathlib import Path

from apps.router.schema_loader import SchemaValidationError
from apps.workers.audit_logger import AuditLogger


ROOT = Path(__file__).resolve().parents[2]


class AuditLoggerTests(unittest.TestCase):
    def test_writes_valid_jsonl_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "audit.jsonl"
            logger = AuditLogger(
                log_path=log_path,
                schema_path=ROOT / "schemas/audit-entry.schema.json",
            )

            record = logger.write(
                {
                    "audit_id": "audit-001",
                    "occurred_at": "2026-04-09T12:00:00Z",
                    "actor": "leo",
                    "intent": "capture inbox note",
                    "approved_command": "note.capture.inbox",
                    "target": "knowledge/inbox/example.md",
                    "outcome": "succeeded",
                    "repo_revision": "abc123",
                    "risk_level": "low",
                    "correlation_id": "corr-001",
                }
            )

            self.assertEqual(record["audit_id"], "audit-001")
            stored = json.loads(log_path.read_text().splitlines()[0])
            self.assertEqual(stored["approved_command"], "note.capture.inbox")

    def test_rejects_invalid_timestamp_format(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "audit.jsonl"
            logger = AuditLogger(
                log_path=log_path,
                schema_path=ROOT / "schemas/audit-entry.schema.json",
            )

            with self.assertRaises(SchemaValidationError):
                logger.write(
                    {
                        "audit_id": "audit-001",
                        "occurred_at": "not-a-timestamp",
                        "actor": "leo",
                        "intent": "capture inbox note",
                        "approved_command": "note.capture.inbox",
                        "target": "knowledge/inbox/example.md",
                        "outcome": "succeeded",
                        "repo_revision": "abc123",
                        "risk_level": "low",
                        "correlation_id": "corr-001",
                    }
                )


if __name__ == "__main__":
    unittest.main()
