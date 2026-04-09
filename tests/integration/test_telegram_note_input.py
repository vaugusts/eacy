import json
import tempfile
import unittest
from pathlib import Path

from apps.voice_gateway.telegram_input_flow import process_telegram_update

ROOT = Path(__file__).resolve().parents[2]


class TelegramNoteInputIntegrationTests(unittest.TestCase):
    def test_successful_telegram_note_intake_writes_record_and_manifest(self) -> None:
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
                update=update,
                repo_root=repo_root,
                drive_folder_id="drive-folder-1",
                audio_lookup={"voice-file-123": b"voice-bytes"},
                received_at="2026-04-09T00:00:00Z",
            )

            self.assertTrue(result["accepted"])
            self.assertTrue(Path(result["record_path"]).exists())
            self.assertTrue(Path(result["manifest_path"]).exists())
            self.assertEqual(result["drive"]["folder_id"], "drive-folder-1")
            self.assertEqual(result["status"], "landed")


if __name__ == "__main__":
    unittest.main()
