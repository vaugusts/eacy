import tempfile
import unittest

from apps.workers.drive_sync import enumerate_sync_candidates
from apps.workers.landing_manifest_writer import build_partial_manifest, build_success_manifest, write_manifest


class DriveSyncUnitTests(unittest.TestCase):
    def test_enumerate_sync_candidates_reports_ready_and_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ready_manifest = build_success_manifest(
                {
                    "landing_id": "tg-ready",
                    "envelope_id": "tg-ready",
                    "drive_markdown_file_id": "md-ready",
                    "drive_folder_id": "folder-1",
                    "timestamp": "2026-04-09T00:00:00Z",
                }
            )
            blocked_manifest = build_partial_manifest(
                {
                    "landing_id": "tg-blocked",
                    "envelope_id": "tg-blocked",
                    "drive_markdown_file_id": "md-blocked",
                    "drive_folder_id": "folder-1",
                    "timestamp": "2026-04-09T00:00:00Z",
                }
            )

            write_manifest(ready_manifest, repo_root=temp_dir)
            write_manifest(blocked_manifest, repo_root=temp_dir)

            candidates = enumerate_sync_candidates(temp_dir)
            by_id = {item["landing_id"]: item for item in candidates}

            self.assertEqual(by_id["tg-ready"]["decision"], "ready")
            self.assertEqual(by_id["tg-ready"]["import_state"], "ready")
            self.assertEqual(by_id["tg-blocked"]["decision"], "blocked")
            self.assertEqual(by_id["tg-blocked"]["import_state"], "blocked")


if __name__ == "__main__":
    unittest.main()
