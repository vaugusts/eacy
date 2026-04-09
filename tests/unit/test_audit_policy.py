import unittest
from datetime import datetime, timezone

from apps.workers.audit_logger import is_within_retention_window, redact_sensitive_parameters


class AuditPolicyTests(unittest.TestCase):
    def test_redacts_nested_sensitive_parameters(self) -> None:
        parameters = {
            "title": "ok",
            "api_key": "secret",
            "nested": {
                "access_token": "secret-token",
                "safe_value": "visible",
            },
        }

        redacted = redact_sensitive_parameters(parameters, ["api_key", "access_token"])

        self.assertEqual(redacted["api_key"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["access_token"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["safe_value"], "visible")

    def test_retention_window_expires_old_records(self) -> None:
        record = {
            "occurred_at": "2026-01-01T00:00:00Z",
        }

        self.assertFalse(
            is_within_retention_window(
                record,
                retention_days=30,
                now=datetime(2026, 4, 9, tzinfo=timezone.utc),
            )
        )


if __name__ == "__main__":
    unittest.main()
