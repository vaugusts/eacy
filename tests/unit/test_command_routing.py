import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from apps.router.command_registry import load_command_registry
from apps.router.intent_resolver import resolve_command_intent
from apps.router.policy_engine import ActorContext, PolicyEngine, load_policy_definition
from apps.workers.execution_dispatcher import dispatch_command


ROOT = Path(__file__).resolve().parents[2]


class CommandRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture_path = ROOT / "tests/fixtures/command_requests.json"
        cls.fixtures = json.loads(fixture_path.read_text())
        cls.registry = load_command_registry(ROOT / "registry/commands.yaml")
        cls.policy = load_policy_definition(ROOT / "policies/execution-policy.yaml")

    def test_resolve_command_intent_matches_transcript(self) -> None:
        fixture = self.fixtures["daily_digest"]

        command = resolve_command_intent(self.registry, fixture["transcript"])

        self.assertEqual(command["id"], "knowledge.digest.daily")
        self.assertEqual(command["executor"]["type"], "github_action")

    def test_dispatch_command_returns_normalized_result_for_low_risk_command(self) -> None:
        fixture = self.fixtures["daily_digest"]
        actor = ActorContext(**fixture["actor"])

        with tempfile.TemporaryDirectory() as temp_dir:
            result = dispatch_command(
                transcript=fixture["transcript"],
                registry=self.registry,
                policy_engine=PolicyEngine(self.policy),
                actor=actor,
                parameters=fixture["parameters"],
                channel=fixture["channel"],
                correlation_id=fixture["correlation_id"],
                repo_revision=fixture["repo_revision"],
                audit_log_path=Path(temp_dir) / "audit.jsonl",
            )

        self.assertEqual(result["command_id"], "knowledge.digest.daily")
        self.assertEqual(result["correlation_id"], fixture["correlation_id"])
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["decision"], "allowed")

    def test_dispatch_command_blocks_agent_without_scope(self) -> None:
        fixture = self.fixtures["topic_pack_denied_agent"]
        actor = ActorContext(**fixture["actor"])

        with tempfile.TemporaryDirectory() as temp_dir:
            result = dispatch_command(
                transcript=fixture["transcript"],
                registry=self.registry,
                policy_engine=PolicyEngine(self.policy),
                actor=actor,
                parameters=fixture["parameters"],
                channel=fixture["channel"],
                correlation_id=fixture["correlation_id"],
                repo_revision=fixture["repo_revision"],
                audit_log_path=Path(temp_dir) / "audit.jsonl",
            )

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["decision"], "deny")
        self.assertIn("Agent scope", " ".join(result["reasons"]))

    def test_dispatch_command_requires_confirmation_for_medium_risk_voice_command(self) -> None:
        registry = self.registry
        actor = ActorContext(actor_id="leo", actor_type="human", scopes=[])

        with tempfile.TemporaryDirectory() as temp_dir:
            audit_log_path = Path(temp_dir) / "audit.jsonl"
            result = dispatch_command(
                transcript="sync drive assets",
                registry=registry,
                policy_engine=PolicyEngine(self.policy),
                actor=actor,
                parameters={"folder_id": "abc123"},
                channel="voice",
                correlation_id="cmd-confirm-001",
                repo_revision="abc123",
                audit_log_path=audit_log_path,
            )

            self.assertEqual(result["command_id"], "assets.sync.drive")
            self.assertEqual(result["correlation_id"], "cmd-confirm-001")
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["decision"], "confirm")
            self.assertIn("confirmation", result["error_message"].lower())
            self.assertTrue(audit_log_path.exists())
            self.assertIn('"outcome": "blocked"', audit_log_path.read_text())

    def test_dispatch_command_denies_unknown_transcript_and_audits_it(self) -> None:
        actor = ActorContext(actor_id="leo", actor_type="human", scopes=[])

        with tempfile.TemporaryDirectory() as temp_dir:
            audit_log_path = Path(temp_dir) / "audit.jsonl"
            result = dispatch_command(
                transcript="do something unregistered",
                registry=self.registry,
                policy_engine=PolicyEngine(self.policy),
                actor=actor,
                parameters={},
                channel="voice",
                correlation_id="cmd-unknown-001",
                repo_revision="abc123",
                audit_log_path=audit_log_path,
            )

            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["decision"], "deny")
            self.assertEqual(result["command_id"], "unknown")
            self.assertEqual(result["correlation_id"], "cmd-unknown-001")
            self.assertIn("unknown", result["error_message"].lower())
            self.assertTrue(audit_log_path.exists())
            self.assertIn('"approved_command": "unknown"', audit_log_path.read_text())

    def test_dispatch_command_emits_current_audit_timestamp(self) -> None:
        fixture = self.fixtures["daily_digest"]
        actor = ActorContext(**fixture["actor"])

        with tempfile.TemporaryDirectory() as temp_dir:
            audit_log_path = Path(temp_dir) / "audit.jsonl"
            before = datetime.now(timezone.utc)
            dispatch_command(
                transcript=fixture["transcript"],
                registry=self.registry,
                policy_engine=PolicyEngine(self.policy),
                actor=actor,
                parameters=fixture["parameters"],
                channel=fixture["channel"],
                correlation_id=fixture["correlation_id"],
                repo_revision=fixture["repo_revision"],
                audit_log_path=audit_log_path,
            )
            after = datetime.now(timezone.utc)

            stored = json.loads(audit_log_path.read_text().splitlines()[0])
            occurred_at = datetime.fromisoformat(stored["occurred_at"].replace("Z", "+00:00"))

        self.assertGreaterEqual(occurred_at, before)
        self.assertLessEqual(occurred_at, after)


if __name__ == "__main__":
    unittest.main()
