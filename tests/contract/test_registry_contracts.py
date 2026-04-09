import unittest
from pathlib import Path

from apps.router.command_registry import load_command_registry
from apps.router.policy_engine import load_policy_definition


ROOT = Path(__file__).resolve().parents[2]


class RegistryContractTests(unittest.TestCase):
    def test_governance_scaffolding_exists(self) -> None:
        pr_template = ROOT / ".github/pull_request_template.md"
        exception_readme = ROOT / "policies/exceptions/README.md"

        self.assertTrue(pr_template.exists())
        self.assertTrue(exception_readme.exists())

        pr_text = pr_template.read_text()
        self.assertIn(".specify/memory/constitution.md", pr_text)
        for principle in [
            "I. Repository-Native Backbone",
            "II. Git-First Change Control",
            "III. Markdown-First Curated Knowledge",
            "IV. Governed Voice-to-Action",
            "V. Policy-Gated Execution and Audit",
            "VI. Spec-Driven Incremental Evolution",
            "VII. AI Agent Authorization and Oversight",
        ]:
            self.assertIn(principle, pr_text)

        exception_text = exception_readme.read_text()
        for field in ["Date", "Rationale", "Scope", "Review-Date"]:
            self.assertIn(field, exception_text)

    def test_registry_includes_low_and_medium_risk_commands_with_agent_scopes(self) -> None:
        registry = load_command_registry(ROOT / "registry/commands.yaml")
        risks = {command["risk_level"] for command in registry["commands"]}

        self.assertIn("low", risks)
        self.assertIn("medium", risks)

        for command in registry["commands"]:
            self.assertIn("allowed_agent_scopes", command)
            self.assertIsInstance(command["allowed_agent_scopes"], list)

    def test_policy_definition_covers_parameter_and_agent_scope_rules(self) -> None:
        policy = load_policy_definition(ROOT / "policies/execution-policy.yaml")
        rule_ids = {rule["rule_id"] for rule in policy["rules"]}

        self.assertIn("deny-unknown-parameter", rule_ids)
        self.assertIn("enforce-agent-scopes", rule_ids)

    def test_registry_targets_reference_real_files_or_functions(self) -> None:
        registry = load_command_registry(ROOT / "registry/commands.yaml")
        local_cli_targets = {
            "note_writer.write_inbox_note",
            "daily_writer.append_to_daily_note",
            "topic_pack.generate",
        }

        for command in registry["commands"]:
            executor = command["executor"]
            target = executor["target"]

            if executor["type"] == "github_action":
                self.assertTrue((ROOT / target).exists(), target)
            elif executor["type"] == "n8n_webhook":
                self.assertTrue((ROOT / target).exists(), target)
            elif executor["type"] == "local_cli":
                self.assertIn(target, local_cli_targets)


if __name__ == "__main__":
    unittest.main()
