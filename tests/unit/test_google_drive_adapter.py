import unittest

from apps.workers.google_drive_adapter import upload_telegram_landing


class DummyDriveClient:
    def upload(self, **kwargs):
        return {
            "upload_state": "landed",
            "markdown": {"file_id": "md-1", "web_view_link": "https://example/md-1"},
            "audio": {"file_id": "au-1", "web_view_link": "https://example/au-1"},
            "recovery_hints": [],
            "folder_id": kwargs["folder_id"],
        }


class GoogleDriveAdapterTests(unittest.TestCase):
    def test_stub_upload_returns_markdown_and_optional_audio(self) -> None:
        result = upload_telegram_landing(
            folder_id="folder-1",
            markdown_content="# hi",
            markdown_filename="x.md",
            audio_bytes=b"audio",
            audio_filename="x.oga",
        )

        self.assertEqual(result["upload_state"], "landed")
        self.assertIn("file_id", result["markdown"])
        self.assertIn("file_id", result["audio"])

    def test_client_upload_passthrough(self) -> None:
        result = upload_telegram_landing(
            folder_id="folder-1",
            markdown_content="# hi",
            markdown_filename="x.md",
            client=DummyDriveClient(),
        )

        self.assertEqual(result["markdown"]["file_id"], "md-1")
        self.assertEqual(result["folder_id"], "folder-1")

    def test_partial_upload_returns_recovery_hints(self) -> None:
        result = upload_telegram_landing(
            folder_id="folder-1",
            markdown_content="# hi",
            markdown_filename="x.md",
            simulate_partial_failure=True,
        )

        self.assertEqual(result["upload_state"], "partial")
        self.assertIn("retry_audio_upload", result["recovery_hints"])


if __name__ == "__main__":
    unittest.main()
