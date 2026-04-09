import json
import tempfile
import unittest
from pathlib import Path

from apps.router.daily_writer import append_to_daily_note
from apps.router.note_writer import parse_frontmatter


ROOT = Path(__file__).resolve().parents[2]


class DailyWriterTests(unittest.TestCase):
    def setUp(self) -> None:
        fixture_path = ROOT / "tests/fixtures/capture_request.json"
        self.request = json.loads(fixture_path.read_text())
        self.request["target_note_type"] = "daily"

    def test_append_to_daily_note_creates_file_and_capture_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            knowledge_dir = Path(temp_dir) / "knowledge"
            result = append_to_daily_note(
                self.request,
                knowledge_dir=knowledge_dir,
                templates_dir=ROOT / "templates/notes",
            )

            self.assertTrue(result["path"].exists())
            frontmatter, body = parse_frontmatter(result["path"].read_text())
            self.assertEqual(frontmatter["note_type"], "daily")
            self.assertIn("env-001", result["path"].read_text())
            self.assertIn("Remember to review the voice architecture", body)


if __name__ == "__main__":
    unittest.main()
