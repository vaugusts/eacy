import json
import tempfile
import unittest
from pathlib import Path

from apps.router.capture_router import process_capture_request
from apps.router.note_writer import parse_frontmatter


ROOT = Path(__file__).resolve().parents[2]


class CaptureModeTests(unittest.TestCase):
    def test_routes_inbox_and_daily_capture_requests(self) -> None:
        fixture = json.loads((ROOT / "tests/fixtures/capture_request.json").read_text())

        with tempfile.TemporaryDirectory() as temp_dir:
            knowledge_dir = Path(temp_dir) / "knowledge"
            inbox_result = process_capture_request(
                fixture,
                knowledge_dir=knowledge_dir,
                templates_dir=ROOT / "templates/notes",
            )
            self.assertEqual(inbox_result["note_type"], "inbox")
            self.assertTrue(inbox_result["path"].exists())

            daily_request = dict(fixture)
            daily_request["target_note_type"] = "daily"
            daily_result = process_capture_request(
                daily_request,
                knowledge_dir=knowledge_dir,
                templates_dir=ROOT / "templates/notes",
            )

            self.assertEqual(daily_result["note_type"], "daily")
            self.assertTrue(daily_result["path"].exists())
            frontmatter, _ = parse_frontmatter(daily_result["path"].read_text())
            self.assertEqual(frontmatter["note_type"], "daily")


if __name__ == "__main__":
    unittest.main()
