import tempfile
import unittest

from apps.workers.landing_manifest_writer import (
    build_partial_manifest,
    build_success_manifest,
    load_manifest,
    write_manifest,
)


class LandingManifestWriterTests(unittest.TestCase):
    def test_build_success_manifest_has_reconciliation_defaults(self) -> None:
        manifest = build_success_manifest(
            {
                "landing_id": "tg-1-2",
                "envelope_id": "tg-1-2",
                "drive_markdown_file_id": "md-1",
                "drive_audio_file_id": "au-1",
                "drive_folder_id": "folder-1",
                "timestamp": "2026-04-09T00:00:00Z",
            }
        )

        self.assertEqual(manifest["status"], "landed")
        self.assertEqual(manifest["retry_count"], 0)
        self.assertFalse(manifest["reconciliation"]["needs_recovery"])

    def test_partial_manifest_and_load_roundtrip(self) -> None:
        manifest = build_partial_manifest(
            {
                "landing_id": "tg-2-3",
                "envelope_id": "tg-2-3",
                "drive_markdown_file_id": "md-2",
                "drive_folder_id": "folder-2",
                "timestamp": "2026-04-09T00:00:00Z",
                "recovery_hint": "retry_repo_write",
                "repo_write_succeeded": False,
            }
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            write_manifest(manifest, repo_root=temp_dir)
            loaded = load_manifest("tg-2-3", repo_root=temp_dir)

            assert loaded is not None
            self.assertEqual(loaded["status"], "partial")
            self.assertTrue(loaded["reconciliation"]["needs_recovery"])
            self.assertEqual(loaded["sync"]["import_state"], "blocked")


if __name__ == "__main__":
    unittest.main()
