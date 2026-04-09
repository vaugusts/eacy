import unittest
from pathlib import Path

import yaml

from apps.router.command_registry import load_command_registry


ROOT = Path(__file__).resolve().parents[2]


class IntegrationContractTests(unittest.TestCase):
    def test_github_action_registry_targets_exist(self) -> None:
        registry = load_command_registry(ROOT / "registry/commands.yaml")
        github_targets = [
            command["executor"]["target"]
            for command in registry["commands"]
            if command["executor"]["type"] == "github_action"
        ]

        for target in github_targets:
            self.assertTrue((ROOT / target).exists(), target)

    def test_n8n_contract_matches_assets_sync_command(self) -> None:
        contract = yaml.safe_load((ROOT / "integrations/n8n/daily-digest.contract.yaml").read_text())

        self.assertEqual(contract["integration"], "n8n")
        self.assertIn("assets.sync.drive", contract["supported_commands"])
        self.assertEqual(contract["webhook"]["method"], "POST")
        self.assertIn("correlation_id", contract["request"]["fields"])


    def test_telegram_openai_and_drive_landing_contracts_exist(self) -> None:
        required_contracts = [
            "integrations/telegram/note-input-webhook.contract.yaml",
            "integrations/openai/transcription.contract.yaml",
            "integrations/google-drive/telegram-landing.contract.yaml",
        ]

        for relative_path in required_contracts:
            self.assertTrue((ROOT / relative_path).exists(), relative_path)

    def test_openclaw_contract_declares_router_tool(self) -> None:
        contract = yaml.safe_load((ROOT / "integrations/openclaw/voice-command-router.tool.yaml").read_text())

        self.assertEqual(contract["provider"], "openclaw")
        self.assertEqual(contract["tool"]["id"], "voice_command_router")
        self.assertIn("registry/commands.yaml", contract["tool"]["policies_required"])


if __name__ == "__main__":
    unittest.main()
