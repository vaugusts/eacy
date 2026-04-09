import json
import tempfile
import unittest
from pathlib import Path

from apps.voice_gateway.telegram_input_flow import process_telegram_update

ROOT = Path(__file__).resolve().parents[2]


class TelegramRetryIntegrationTests(unittest.TestCase):
    def test_duplicate_update_is_idempotent(self) -> None:
        update = json.loads((ROOT / "tests/fixtures/telegram_voice_update.json").read_text())

        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            (repo_root / "knowledge/sources/telegram").mkdir(parents=True, exist_ok=True)
            (repo_root / "knowledge/manifests/telegram").mkdir(parents=True, exist_ok=True)
            (repo_root / "templates/notes").mkdir(parents=True, exist_ok=True)
            (repo_root / "templates/notes/telegram-landing.md").write_text(
                (ROOT / "templates/notes/telegram-landing.md").read_text()
            )

            first = process_telegram_update(update, repo_root=repo_root, drive_folder_id="folder-1")
            second = process_telegram_update(update, repo_root=repo_root, drive_folder_id="folder-1")

            self.assertTrue(first["accepted"])
            self.assertFalse(first["deduplicated"])
            self.assertTrue(second["accepted"])
            self.assertTrue(second["deduplicated"])
            self.assertEqual(first["landing_id"], second["landing_id"])


if __name__ == "__main__":
    unittest.main()
