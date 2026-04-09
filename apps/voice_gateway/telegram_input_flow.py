from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from apps.workers.google_drive_adapter import upload_telegram_landing
from apps.workers.landing_manifest_writer import (
    build_partial_manifest,
    build_success_manifest,
    load_manifest,
    write_manifest,
)
from apps.workers.landing_record_writer import write_landing_record
from apps.workers.telegram_adapter import normalize_telegram_update
from apps.workers.transcription_adapter import transcribe_audio


def process_telegram_update(
    update: dict[str, Any],
    repo_root: str | Path,
    drive_folder_id: str,
    audio_lookup: dict[str, bytes] | None = None,
    received_at: str | None = None,
    simulate_partial_drive: bool = False,
    simulate_repo_write_failure: bool = False,
) -> dict[str, Any]:
    envelope = normalize_telegram_update(update, received_at=received_at)
    if envelope is None:
        return {"accepted": False, "reason": "unsupported_update"}

    now = received_at or _utc_now_iso()
    landing_id = envelope["envelope_id"]
    existing_manifest = load_manifest(landing_id, repo_root)
    if existing_manifest is not None:
        return {
            "accepted": True,
            "landing_id": landing_id,
            "status": existing_manifest["status"],
            "deduplicated": True,
            "manifest_path": str(Path(repo_root) / "knowledge/manifests/telegram" / f"{landing_id}.json"),
        }

    audio_bytes = (audio_lookup or {}).get(envelope["telegram_file_id"], b"audio")
    transcription = transcribe_audio(audio_bytes=audio_bytes, mime_type=envelope["mime_type"])
    transcript = transcription["transcript_text"]

    markdown_filename = f"{landing_id}.md"
    markdown_content = f"# Telegram Landing {landing_id}\n\n{transcript}\n"
    drive_result = upload_telegram_landing(
        folder_id=drive_folder_id,
        markdown_content=markdown_content,
        markdown_filename=markdown_filename,
        audio_bytes=audio_bytes,
        audio_filename=f"{landing_id}.oga",
        simulate_partial_failure=simulate_partial_drive,
    )

    record_context = {
        "landing_id": landing_id,
        "update_id": envelope["update_id"],
        "message_id": envelope["message_id"],
        "drive_markdown_file_id": drive_result["markdown"]["file_id"],
        "drive_audio_file_id": (drive_result.get("audio") or {}).get("file_id", ""),
        "timestamp": now,
        "transcript": transcript,
        "envelope_id": envelope["envelope_id"],
        "telegram_file_id": envelope["telegram_file_id"],
        "mime_type": envelope["mime_type"],
        "drive_markdown_url": drive_result["markdown"]["web_view_link"],
        "drive_audio_url": (drive_result.get("audio") or {}).get("web_view_link", ""),
        "import_state": "pending",
        "block_reason": "",
        "status": "landed",
        "reconciliation_note": "",
    }

    if drive_result.get("upload_state") == "partial" or simulate_repo_write_failure:
        record_context["status"] = "partial"
        record_context["import_state"] = "blocked"
        record_context["block_reason"] = "reconciliation_required"
        record_context["reconciliation_note"] = "Partial success recorded; reconciliation required."

    if not simulate_repo_write_failure:
        record_path = write_landing_record(record_context, repo_root=repo_root, templates_dir=Path(repo_root) / "templates/notes")
    else:
        record_path = Path(repo_root) / "knowledge/sources/telegram" / f"{landing_id}.md"

    if record_context["status"] == "landed":
        manifest = build_success_manifest(
            {
                "landing_id": landing_id,
                "envelope_id": envelope["envelope_id"],
                "drive_markdown_file_id": drive_result["markdown"]["file_id"],
                "drive_audio_file_id": (drive_result.get("audio") or {}).get("file_id", ""),
                "drive_folder_id": drive_result["folder_id"],
                "timestamp": now,
                "retry_count": 0,
            }
        )
    else:
        errors = ["repo_write_failed"] if simulate_repo_write_failure else ["drive_partial_upload"]
        manifest = build_partial_manifest(
            {
                "landing_id": landing_id,
                "envelope_id": envelope["envelope_id"],
                "drive_markdown_file_id": drive_result["markdown"]["file_id"],
                "drive_audio_file_id": (drive_result.get("audio") or {}).get("file_id", ""),
                "drive_folder_id": drive_result["folder_id"],
                "timestamp": now,
                "retry_count": 0,
                "recovery_hint": "retry_repo_write" if simulate_repo_write_failure else "retry_audio_upload",
                "drive_write_succeeded": True,
                "repo_write_succeeded": not simulate_repo_write_failure,
                "errors": errors,
                "status": "partial",
            }
        )

    manifest_path = write_manifest(manifest, repo_root=repo_root)

    return {
        "accepted": True,
        "envelope": envelope,
        "transcript": transcription,
        "drive": drive_result,
        "landing_id": landing_id,
        "record_path": str(record_path),
        "manifest_path": str(manifest_path),
        "status": manifest["status"],
        "deduplicated": False,
    }


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
