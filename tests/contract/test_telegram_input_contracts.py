import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


class TelegramInputContractTests(unittest.TestCase):
    def test_telegram_webhook_contract_shape(self) -> None:
        contract = yaml.safe_load((ROOT / "integrations/telegram/note-input-webhook.contract.yaml").read_text())

        self.assertEqual(contract["integration"], "telegram")
        self.assertEqual(contract["webhook"]["method"], "POST")
        self.assertEqual(contract["request"]["schema"], "schemas/telegram-update.schema.json")
        self.assertIn("voice", contract["request"]["supported_message_kinds"])

    def test_transcription_contract_shape(self) -> None:
        contract = yaml.safe_load((ROOT / "integrations/openai/transcription.contract.yaml").read_text())

        self.assertEqual(contract["integration"], "openai")
        self.assertEqual(contract["operation"], "audio.transcribe")
        self.assertIn("audio_bytes", contract["request"]["fields"])
        self.assertIn("transcript_text", contract["response"]["success"])

    def test_drive_landing_contract_shape(self) -> None:
        contract = yaml.safe_load((ROOT / "integrations/google-drive/telegram-landing.contract.yaml").read_text())

        self.assertEqual(contract["integration"], "google_drive")
        self.assertEqual(contract["auth"]["mode"], "oauth_user_token")
        self.assertTrue(contract["operations"]["upload_markdown"]["required"])
        self.assertIn("upload_state", contract["response"]["metadata"])


if __name__ == "__main__":
    unittest.main()
