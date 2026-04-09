import json
import tempfile
import unittest
from pathlib import Path

from apps.router.command_registry import load_command_registry
from apps.router.policy_engine import ActorContext, PolicyEngine, load_policy_definition
from apps.workers.execution_dispatcher import dispatch_command


ROOT = Path(__file__).resolve().parents[2]


class CommandModeIntegrationTests(unittest.TestCase):
    def test_command_mode_executes_daily_digest_request(self) -> None:
        fixtures = json.loads((ROOT / "tests/fixtures/command_requests.json").read_text())
        fixture = fixtures["daily_digest"]

        registry = load_command_registry(ROOT / "registry/commands.yaml")
        policy_engine = PolicyEngine(load_policy_definition(ROOT / "policies/execution-policy.yaml"))
        actor = ActorContext(**fixture["actor"])

        with tempfile.TemporaryDirectory() as temp_dir:
            audit_log = Path(temp_dir) / "audit.jsonl"
            result = dispatch_command(
                transcript=fixture["transcript"],
                registry=registry,
                policy_engine=policy_engine,
                actor=actor,
                parameters=fixture["parameters"],
                channel=fixture["channel"],
                correlation_id=fixture["correlation_id"],
                repo_revision=fixture["repo_revision"],
                audit_log_path=audit_log,
            )

            self.assertEqual(result["status"], "completed")
            self.assertTrue(audit_log.exists())
            self.assertIn("knowledge.digest.daily", audit_log.read_text())


if __name__ == "__main__":
    unittest.main()
