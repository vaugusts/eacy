from __future__ import annotations

from pathlib import Path
from typing import Any

from apps.router.daily_writer import append_to_daily_note
from apps.router.note_writer import write_inbox_note


def process_capture_request(
    request: dict[str, Any],
    knowledge_dir: str | Path,
    templates_dir: str | Path | None = None,
) -> dict[str, Any]:
    note_type = resolve_capture_target(request)

    if note_type == "daily":
        return append_to_daily_note(request, knowledge_dir=knowledge_dir, templates_dir=templates_dir)

    return write_inbox_note(request, knowledge_dir=knowledge_dir, templates_dir=templates_dir)


def resolve_capture_target(request: dict[str, Any]) -> str:
    return request.get("target_note_type", "inbox")
