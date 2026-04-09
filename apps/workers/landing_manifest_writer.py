from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apps.router.schema_loader import get_repo_root, load_json_schema, validate_against_schema


def write_manifest(manifest: dict[str, Any], repo_root: str | Path) -> Path:
    root = Path(repo_root)
    schema = load_json_schema(get_repo_root() / "schemas/landing-manifest.schema.json")
    validate_against_schema(manifest, schema, context="landing_manifest")

    target_dir = root / "knowledge/manifests/telegram"
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{manifest['landing_id']}.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    return path


def load_manifest(landing_id: str, repo_root: str | Path) -> dict[str, Any] | None:
    path = Path(repo_root) / "knowledge/manifests/telegram" / f"{landing_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def build_success_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    manifest = {
        "manifest_version": "1.0.0",
        "landing_id": payload["landing_id"],
        "envelope_id": payload["envelope_id"],
        "status": "landed",
        "retry_count": int(payload.get("retry_count", 0)),
        "reconciliation": {
            "needs_recovery": False,
            "recovery_hint": "",
            "drive_write_succeeded": True,
            "repo_write_succeeded": True,
        },
        "drive": {
            "markdown_file_id": payload["drive_markdown_file_id"],
            "audio_file_id": payload.get("drive_audio_file_id", ""),
            "folder_id": payload["drive_folder_id"],
        },
        "errors": [],
        "created_at": payload["timestamp"],
        "updated_at": payload["timestamp"],
        "sync": {
            "import_state": "pending",
            "block_reason": "",
            "ready_for_import": False,
            "readiness_reason": "awaiting_sync_evaluation",
        },
    }
    return apply_sync_readiness(manifest)


def build_partial_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    manifest = {
        "manifest_version": "1.0.0",
        "landing_id": payload["landing_id"],
        "envelope_id": payload["envelope_id"],
        "status": payload.get("status", "partial"),
        "retry_count": int(payload.get("retry_count", 0)),
        "reconciliation": {
            "needs_recovery": True,
            "recovery_hint": payload.get("recovery_hint", "retry_repo_write"),
            "drive_write_succeeded": bool(payload.get("drive_write_succeeded", True)),
            "repo_write_succeeded": bool(payload.get("repo_write_succeeded", False)),
        },
        "drive": {
            "markdown_file_id": payload.get("drive_markdown_file_id", ""),
            "audio_file_id": payload.get("drive_audio_file_id", ""),
            "folder_id": payload.get("drive_folder_id", ""),
        },
        "errors": payload.get("errors", ["partial_failure"]),
        "created_at": payload["timestamp"],
        "updated_at": payload["timestamp"],
        "sync": {
            "import_state": "blocked",
            "block_reason": payload.get("block_reason", "reconciliation_required"),
            "ready_for_import": False,
            "readiness_reason": "reconciliation_required",
        },
    }
    return apply_sync_readiness(manifest)


def apply_sync_readiness(manifest: dict[str, Any]) -> dict[str, Any]:
    sync = manifest.setdefault("sync", {})
    status = manifest.get("status")
    reconciliation = manifest.get("reconciliation", {})

    if status == "landed" and not reconciliation.get("needs_recovery", False):
        sync["import_state"] = "ready"
        sync["block_reason"] = ""
        sync["ready_for_import"] = True
        sync["readiness_reason"] = "landing_complete"
        return manifest

    sync["import_state"] = "blocked"
    sync["ready_for_import"] = False
    if not sync.get("block_reason"):
        sync["block_reason"] = "reconciliation_required"
    sync["readiness_reason"] = "blocked_until_reconciled"
    return manifest
