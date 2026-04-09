import json
import tempfile
import unittest
from pathlib import Path

from apps.router.note_writer import write_inbox_note
from apps.workers.correlation import link_note_and_audit


ROOT = Path(__file__).resolve().parents[2]


class CombinedModeCorrelationTests(unittest.TestCase):
    def test_link_note_and_audit_updates_note_with_combined_metadata(self) -> None:
        request = json.loads((ROOT / "tests/fixtures/capture_request.json").read_text())

        with tempfile.TemporaryDirectory() as temp_dir:
            knowledge_dir = Path(temp_dir) / "knowledge"
            note_result = write_inbox_note(
                request,
                knowledge_dir=knowledge_dir,
                templates_dir=ROOT / "templates/notes",
            )
            command_result = {
                "command_id": "topics.pack.generate",
                "decision": "deny",
                "status": "blocked",
                "error_message": "Agent scope does not allow this command",
            }

            link_result = link_note_and_audit(
                note_path=note_result["path"],
                command_result=command_result,
                correlation_id="cmb-001",
            )

            note_text = note_result["path"].read_text()
            self.assertEqual(link_result["correlation_id"], "cmb-001")
            self.assertIn("capture_mode: combined", note_text)
            self.assertIn("- topics.pack.generate", note_text)
            self.assertIn("## Linked Automation", note_text)
            self.assertIn("Correlation ID: `cmb-001`", note_text)


if __name__ == "__main__":
    unittest.main()
