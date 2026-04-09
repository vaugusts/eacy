import json
import unittest
from pathlib import Path

from apps.workers.telegram_adapter import build_file_download_url, normalize_telegram_update

ROOT = Path(__file__).resolve().parents[2]


class TelegramAdapterTests(unittest.TestCase):
    def test_normalize_voice_update(self) -> None:
        update = json.loads((ROOT / "tests/fixtures/telegram_voice_update.json").read_text())

        envelope = normalize_telegram_update(update, received_at="2026-04-09T00:00:00Z")

        self.assertIsNotNone(envelope)
        assert envelope is not None
        self.assertEqual(envelope["message_kind"], "voice")
        self.assertEqual(envelope["telegram_file_id"], "voice-file-123")
        self.assertEqual(envelope["source"]["provider"], "telegram")

    def test_unsupported_update_returns_none(self) -> None:
        update = json.loads((ROOT / "tests/fixtures/telegram_unsupported_update.json").read_text())

        envelope = normalize_telegram_update(update)

        self.assertIsNone(envelope)

    def test_build_file_download_url(self) -> None:
        url = build_file_download_url("token-abc", "voice/file_123.oga")
        self.assertEqual(url, "https://api.telegram.org/file/bottoken-abc/voice/file_123.oga")


if __name__ == "__main__":
    unittest.main()
