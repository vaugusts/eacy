from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from apps.router.note_writer import _render_frontmatter, parse_frontmatter
from apps.router.schema_loader import get_repo_root, load_json_schema, validate_against_schema


def update_asset_index(
    asset_records: list[dict[str, Any]],
    index_path: str | Path,
    updated_at: str | None = None,
) -> dict[str, Any]:
    repo_root = get_repo_root()
    schema = load_json_schema(repo_root / "schemas/asset-index.schema.json")
    for record in asset_records:
        validate_against_schema(record, schema, context="asset_record")

    path = Path(index_path)
    frontmatter, body = parse_frontmatter(path.read_text())
    frontmatter["updated_at"] = updated_at or _utc_now_iso()

    asset_table = _render_asset_table(asset_records)
    sync_notes = _extract_sync_notes(body)
    body = f"## Asset Table\n\n{asset_table}\n\n## Sync Notes\n\n{sync_notes}".rstrip() + "\n"
    path.write_text(_render_frontmatter(frontmatter) + body)

    return {
        "path": path,
        "asset_count": len(asset_records),
        "updated_at": frontmatter["updated_at"],
    }


def _render_asset_table(asset_records: list[dict[str, Any]]) -> str:
    lines = [
        "| Asset ID | Type | Storage | Linked Notes | Summary |",
        "|----------|------|---------|--------------|---------|",
    ]
    for record in asset_records:
        linked_notes = ", ".join(f"`{item}`" for item in record.get("linked_notes", [])) or "-"
        lines.append(
            "| `{asset_id}` | {asset_type} | `{storage_ref}` | {linked_notes} | {summary} |".format(
                asset_id=record["asset_id"],
                asset_type=record["asset_type"],
                storage_ref=record["storage_ref"],
                linked_notes=linked_notes,
                summary=record["summary"].replace("|", "/"),
            )
        )
    return "\n".join(lines)


def _extract_sync_notes(body: str) -> str:
    marker = "## Sync Notes\n\n"
    if marker not in body:
        return "- Keep the asset index in sync with approved external stores."
    return body.split(marker, 1)[1].strip()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
