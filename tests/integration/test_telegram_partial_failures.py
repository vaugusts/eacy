import json
import tempfile
import unittest
from pathlib import Path

from apps.voice_gateway.telegram_input_flow import process_telegram_update

ROOT = Path(__file__).resolve().parents[2]


class TelegramPartialFailureIntegrationTests(unittest.TestCase):
    def test_drive_success_repo_write_failure_returns_recovery_metadata(self) -> None:
        update = json.loads((ROOT / "tests/fixtures/telegram_voice_update.json").read_text())

        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            (repo_root / "knowledge/sources/telegram").mkdir(parents=True, exist_ok=True)
            (repo_root / "knowledge/manifests/telegram").mkdir(parents=True, exist_ok=True)
            (repo_root / "templates/notes").mkdir(parents=True, exist_ok=True)
            (repo_root / "templates/notes/telegram-landing.md").write_text(
                (ROOT / "templates/notes/telegram-landing.md").read_text()
            )

            result = process_telegram_update(
                update,
                repo_root=repo_root,
                drive_folder_id="folder-1",
                simulate_repo_write_failure=True,
            )

            self.assertTrue(result["accepted"])
            self.assertEqual(result["status"], "partial")
            manifest = json.loads(Path(result["manifest_path"]).read_text())
            self.assertEqual(manifest["status"], "partial")
            self.assertTrue(manifest["reconciliation"]["needs_recovery"])
            self.assertEqual(manifest["reconciliation"]["recovery_hint"], "retry_repo_write")


if __name__ == "__main__":
    unittest.main()
