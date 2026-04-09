from __future__ import annotations

from typing import Any


def upload_telegram_landing(
    folder_id: str,
    markdown_content: str,
    markdown_filename: str,
    audio_bytes: bytes | None = None,
    audio_filename: str | None = None,
    client: Any | None = None,
    simulate_partial_failure: bool = False,
) -> dict[str, Any]:
    if client is not None:
        return client.upload(
            folder_id=folder_id,
            markdown_content=markdown_content,
            markdown_filename=markdown_filename,
            audio_bytes=audio_bytes,
            audio_filename=audio_filename,
        )

    markdown_id = f"drv-md-{abs(hash(markdown_filename)) % 10_000_000}"
    result: dict[str, Any] = {
        "upload_state": "landed",
        "markdown": {
            "file_id": markdown_id,
            "web_view_link": f"https://drive.google.com/file/d/{markdown_id}/view",
        },
        "audio": None,
        "recovery_hints": [],
        "folder_id": folder_id,
    }

    if audio_bytes is not None and audio_filename:
        audio_id = f"drv-aud-{abs(hash(audio_filename)) % 10_000_000}"
        result["audio"] = {
            "file_id": audio_id,
            "web_view_link": f"https://drive.google.com/file/d/{audio_id}/view",
        }

    if simulate_partial_failure:
        result["upload_state"] = "partial"
        result["recovery_hints"] = ["retry_audio_upload", "reconcile_manifest"]
        result["audio"] = None

    return result
