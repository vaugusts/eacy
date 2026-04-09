from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def enumerate_sync_candidates(repo_root: str | Path) -> list[dict[str, Any]]:
    manifest_dir = Path(repo_root) / "knowledge/manifests/telegram"
    if not manifest_dir.exists():
        return []

    candidates: list[dict[str, Any]] = []
    for manifest_path in sorted(manifest_dir.glob("*.json")):
        manifest = json.loads(manifest_path.read_text())
        candidate = _candidate_from_manifest(manifest, manifest_path)
        candidates.append(candidate)
    return candidates


def pending_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [candidate for candidate in candidates if candidate["import_state"] in {"pending", "ready", "blocked"}]


def _candidate_from_manifest(manifest: dict[str, Any], manifest_path: Path) -> dict[str, Any]:
    sync = manifest.get("sync", {})
    drive = manifest.get("drive", {})

    import_state = str(sync.get("import_state", "pending"))
    ready_for_import = bool(sync.get("ready_for_import", False))
    block_reason = str(sync.get("block_reason", ""))

    decision = "ready" if ready_for_import and import_state == "ready" else "blocked"
    if import_state == "pending":
        decision = "pending"

    return {
        "landing_id": manifest.get("landing_id", ""),
        "manifest_path": str(manifest_path),
        "status": manifest.get("status", "unknown"),
        "import_state": import_state,
        "ready_for_import": ready_for_import,
        "block_reason": block_reason,
        "decision": decision,
        "drive_markdown_file_id": drive.get("markdown_file_id", ""),
    }
