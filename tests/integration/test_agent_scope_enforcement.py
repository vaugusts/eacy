import json
import tempfile
import unittest
from pathlib import Path

from apps.router.command_registry import load_command_registry
from apps.router.policy_engine import ActorContext, PolicyEngine, load_policy_definition
from apps.workers.execution_dispatcher import dispatch_command


ROOT = Path(__file__).resolve().parents[2]


class AgentScopeEnforcementTests(unittest.TestCase):
    def test_agent_without_declared_scope_is_blocked_even_when_other_gates_pass(self) -> None:
        fixtures = json.loads((ROOT / "tests/fixtures/command_requests.json").read_text())
        fixture = fixtures["topic_pack_denied_agent"]

        registry = load_command_registry(ROOT / "registry/commands.yaml")
        policy_engine = PolicyEngine(load_policy_definition(ROOT / "policies/execution-policy.yaml"))
        actor = ActorContext(**fixture["actor"])

        with tempfile.TemporaryDirectory() as temp_dir:
            result = dispatch_command(
                transcript=fixture["transcript"],
                registry=registry,
                policy_engine=policy_engine,
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


if __name__ == "__main__":
    unittest.main()
