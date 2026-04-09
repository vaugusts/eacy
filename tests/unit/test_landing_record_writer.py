import tempfile
import unittest
from pathlib import Path

from apps.workers.landing_record_writer import render_landing_record, write_landing_record

ROOT = Path(__file__).resolve().parents[2]


class LandingRecordWriterTests(unittest.TestCase):
    def _context(self) -> dict[str, str | int]:
        return {
            "landing_id": "tg-1-2",
            "update_id": 1,
            "message_id": 2,
            "drive_markdown_file_id": "md-123",
            "drive_audio_file_id": "au-123",
            "timestamp": "2026-04-09T00:00:00Z",
            "transcript": "hello world",
            "envelope_id": "tg-1-2",
            "telegram_file_id": "voice-file-123",
            "mime_type": "audio/ogg",
            "drive_markdown_url": "https://example/md",
            "drive_audio_url": "https://example/au",
            "import_state": "pending",
            "block_reason": "",
        }

    def test_render_landing_record_includes_frontmatter_and_body(self) -> None:
        content = render_landing_record(self._context(), templates_dir=ROOT / "templates/notes")

        self.assertIn("note_type: telegram_landing", content)
        self.assertIn("## Transcript", content)
        self.assertIn("hello world", content)

    def test_render_partial_record_adds_reconciliation_section(self) -> None:
        context = self._context()
        context["status"] = "partial"
        context["reconciliation_note"] = "Need manual reconcile"

        content = render_landing_record(context, templates_dir=ROOT / "templates/notes")

        self.assertIn("status: partial", content)
        self.assertIn("## Reconciliation", content)

    def test_write_landing_record_creates_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_landing_record(
                self._context(),
                repo_root=temp_dir,
                templates_dir=ROOT / "templates/notes",
            )

            self.assertTrue(path.exists())
            self.assertIn("knowledge/sources/telegram", str(path))


if __name__ == "__main__":
    unittest.main()
