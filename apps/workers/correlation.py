from __future__ import annotations

from pathlib import Path
from typing import Any

from apps.router.note_writer import _render_frontmatter, parse_frontmatter


def link_note_and_audit(
    note_path: str | Path,
    command_result: dict[str, Any],
    correlation_id: str,
) -> dict[str, Any]:
    path = Path(note_path)
    frontmatter, body = parse_frontmatter(path.read_text())

    frontmatter["capture_mode"] = "combined"
    command_refs = frontmatter.get("command_refs", [])
    command_id = command_result["command_id"]
    if command_id not in command_refs:
        command_refs = [*command_refs, command_id]
    frontmatter["command_refs"] = command_refs

    body = _upsert_linked_automation_section(
        body=body,
        correlation_id=correlation_id,
        command_id=command_id,
        decision=command_result["decision"],
        status=command_result["status"],
        error_message=command_result.get("error_message"),
    )
    path.write_text(_render_frontmatter(frontmatter) + body)

    return {
        "note_path": path,
        "correlation_id": correlation_id,
        "command_id": command_id,
        "decision": command_result["decision"],
        "status": command_result["status"],
    }


def _upsert_linked_automation_section(
    body: str,
    correlation_id: str,
    command_id: str,
    decision: str,
    status: str,
    error_message: str | None,
) -> str:
    section_header = "## Linked Automation"
    lines = [
        section_header,
        "",
        f"- Correlation ID: `{correlation_id}`",
        f"- Command ID: `{command_id}`",
        f"- Decision: `{decision}`",
        f"- Status: `{status}`",
    ]
    if error_message:
        lines.append(f"- Error: {error_message}")
    new_section = "\n".join(lines) + "\n"

    if section_header not in body:
        return body.rstrip() + "\n\n" + new_section

    prefix, _existing = body.split(section_header, 1)
    return prefix.rstrip() + "\n\n" + new_section
