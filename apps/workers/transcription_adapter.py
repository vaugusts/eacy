from __future__ import annotations

from typing import Any


def transcribe_audio(
    audio_bytes: bytes,
    mime_type: str,
    model: str = "gpt-4o-mini-transcribe",
    client: Any | None = None,
) -> dict[str, Any]:
    if client is not None:
        return client.transcribe(audio_bytes=audio_bytes, mime_type=mime_type, model=model)

    text = f"transcribed {len(audio_bytes)} bytes from {mime_type}"
    return {
        "transcript_text": text,
        "duration_seconds": 0.0,
        "provider_request_id": "local-stub",
        "model": model,
    }
