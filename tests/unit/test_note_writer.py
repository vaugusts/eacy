import json
import tempfile
import unittest
from pathlib import Path

from apps.router.note_writer import parse_frontmatter, render_inbox_note, write_inbox_note


ROOT = Path(__file__).resolve().parents[2]


class NoteWriterTests(unittest.TestCase):
    def setUp(self) -> None:
        fixture_path = ROOT / "tests/fixtures/capture_request.json"
        self.request = json.loads(fixture_path.read_text())

    def test_render_inbox_note_includes_frontmatter_and_transcript(self) -> None:
        rendered = render_inbox_note(self.request, templates_dir=ROOT / "templates/notes")

        frontmatter, body = parse_frontmatter(rendered["content"])
        self.assertEqual(frontmatter["note_type"], "inbox")
        self.assertEqual(frontmatter["status"], "raw")
        self.assertIn("voice-architecture", frontmatter["topics"])
        self.assertIn("Remember to review the voice architecture", body)

    def test_write_inbox_note_creates_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            knowledge_dir = Path(temp_dir) / "knowledge"
            result = write_inbox_note(
                self.request,
                knowledge_dir=knowledge_dir,
                templates_dir=ROOT / "templates/notes",
            )

            self.assertTrue(result["path"].exists())
            frontmatter, body = parse_frontmatter(result["path"].read_text())
            self.assertEqual(frontmatter["title"], "Voice architecture follow-up")
            self.assertIn("Suggested destination", body)


if __name__ == "__main__":
    unittest.main()
