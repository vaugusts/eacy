import unittest

from apps.workers.transcription_adapter import transcribe_audio


class DummyTranscriptionClient:
    def transcribe(self, audio_bytes: bytes, mime_type: str, model: str) -> dict[str, object]:
        return {
            "transcript_text": "hello from dummy",
            "duration_seconds": 1.25,
            "provider_request_id": "req-123",
            "model": model,
        }


class TranscriptionAdapterTests(unittest.TestCase):
    def test_default_stub_transcription(self) -> None:
        result = transcribe_audio(b"audio", "audio/ogg")

        self.assertIn("transcribed", result["transcript_text"])
        self.assertEqual(result["provider_request_id"], "local-stub")

    def test_client_backed_transcription(self) -> None:
        result = transcribe_audio(b"audio", "audio/ogg", client=DummyTranscriptionClient())

        self.assertEqual(result["transcript_text"], "hello from dummy")
        self.assertEqual(result["provider_request_id"], "req-123")


if __name__ == "__main__":
    unittest.main()
