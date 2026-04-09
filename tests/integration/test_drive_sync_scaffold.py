import tempfile
import unittest

from apps.workers.drive_sync import enumerate_sync_candidates, pending_candidates
from apps.workers.landing_manifest_writer import build_partial_manifest, build_success_manifest, write_manifest


class DriveSyncScaffoldIntegrationTests(unittest.TestCase):
    def test_pending_import_manifest_scanning(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ready_manifest = build_success_manifest(
                {
                    "landing_id": "tg-ready-int",
                    "envelope_id": "tg-ready-int",
                    "drive_markdown_file_id": "md-ready-int",
                    "drive_folder_id": "folder-1",
                    "timestamp": "2026-04-09T00:00:00Z",
                }
            )
            blocked_manifest = build_partial_manifest(
                {
                    "landing_id": "tg-blocked-int",
                    "envelope_id": "tg-blocked-int",
                    "drive_markdown_file_id": "md-blocked-int",
                    "drive_folder_id": "folder-1",
                    "timestamp": "2026-04-09T00:00:00Z",
                }
            )

            write_manifest(ready_manifest, repo_root=temp_dir)
            write_manifest(blocked_manifest, repo_root=temp_dir)

            all_candidates = enumerate_sync_candidates(temp_dir)
            pending = pending_candidates(all_candidates)

            self.assertEqual(len(all_candidates), 2)
            self.assertEqual(len(pending), 2)
            decisions = {item["landing_id"]: item["decision"] for item in all_candidates}
            self.assertEqual(decisions["tg-ready-int"], "ready")
            self.assertEqual(decisions["tg-blocked-int"], "blocked")


if __name__ == "__main__":
    unittest.main()
