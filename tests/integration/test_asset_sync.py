import tempfile
import unittest
from pathlib import Path

from apps.workers.asset_indexer import update_asset_index


ROOT = Path(__file__).resolve().parents[2]


class AssetSyncIntegrationTests(unittest.TestCase):
    def test_asset_index_update_rewrites_asset_table(self) -> None:
        asset_records = [
            {
                "asset_id": "drv-pdf-999",
                "title": "Voice Safety Spec",
                "asset_type": "pdf",
                "storage_system": "google_drive",
                "storage_ref": "https://drive.google.com/file/d/drv-pdf-999",
                "summary": "Specification for safe voice-driven execution",
                "tags": ["voice", "safety"],
                "linked_notes": ["knowledge/topics/voice-architecture.md"],
                "source_ref": "drive-folder-001",
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            index_path = Path(temp_dir) / "index.md"
            index_path.write_text((ROOT / "knowledge/assets/index.md").read_text())

            result = update_asset_index(asset_records=asset_records, index_path=index_path)

            self.assertEqual(result["asset_count"], 1)
            self.assertIn("drv-pdf-999", index_path.read_text())
            self.assertIn("voice-driven execution", index_path.read_text())


if __name__ == "__main__":
    unittest.main()
