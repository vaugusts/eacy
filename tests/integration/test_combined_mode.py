import json
import tempfile
import unittest
from pathlib import Path

from apps.router.command_registry import load_command_registry
from apps.router.policy_engine import ActorContext, PolicyEngine, load_policy_definition
from apps.voice_gateway.combined_mode import process_combined_request


ROOT = Path(__file__).resolve().parents[2]


class CombinedModeIntegrationTests(unittest.TestCase):
    def test_policy_denied_command_still_persists_note_with_linked_audit(self) -> None:
        fixtures = json.loads((ROOT / "tests/fixtures/combined_requests.json").read_text())
        fixture = fixtures["denied_agent"]
        actor = ActorContext(**fixture["actor"])

        with tempfile.TemporaryDirectory() as temp_dir:
            result = process_combined_request(
                request=fixture,
                knowledge_dir=Path(temp_dir) / "knowledge",
                registry=load_command_registry(ROOT / "registry/commands.yaml"),
                policy_engine=PolicyEngine(load_policy_definition(ROOT / "policies/execution-policy.yaml")),
                actor=actor,
                repo_revision=fixture["repo_revision"],
                audit_log_path=Path(temp_dir) / "audit.jsonl",
                templates_dir=ROOT / "templates/notes",
            )

            note_path = result["note"]["path"]
            self.assertTrue(note_path.exists())
            self.assertEqual(result["command"]["status"], "blocked")
            self.assertEqual(result["command"]["decision"], "deny")
            self.assertIn("topics.pack.generate", note_path.read_text())
            self.assertIn("Correlation ID: `cmb-001`", note_path.read_text())
            self.assertIn('"approved_command": "topics.pack.generate"', (Path(temp_dir) / "audit.jsonl").read_text())


if __name__ == "__main__":
    unittest.main()
