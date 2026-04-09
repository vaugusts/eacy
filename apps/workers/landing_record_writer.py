from __future__ import annotations

from pathlib import Path
from typing import Any

from apps.router.template_loader import load_note_template


def render_landing_record(context: dict[str, Any], templates_dir: str | Path | None = None) -> str:
    template = load_note_template("telegram-landing", templates_dir=templates_dir)
    transcript = context.get("transcript", "")
    mapping = {
        "{{landing_id}}": context["landing_id"],
        "{{update_id}}": str(context["update_id"]),
        "{{message_id}}": str(context["message_id"]),
        "{{drive_markdown_file_id}}": context["drive_markdown_file_id"],
        "{{drive_audio_file_id}}": context.get("drive_audio_file_id", ""),
        "{{timestamp}}": context["timestamp"],
        "{{transcript}}": transcript,
        "{{envelope_id}}": context["envelope_id"],
        "{{telegram_file_id}}": context["telegram_file_id"],
        "{{mime_type}}": context["mime_type"],
        "{{drive_markdown_url}}": context["drive_markdown_url"],
        "{{drive_audio_url}}": context.get("drive_audio_url", ""),
        "{{import_state}}": context.get("import_state", "pending"),
        "{{block_reason}}": context.get("block_reason", ""),
    }

    rendered = template
    for key, value in mapping.items():
        rendered = rendered.replace(key, value)

    status = context.get("status", "landed")
    rendered = rendered.replace("status: landed", f"status: {status}")

    reconciliation_note = context.get("reconciliation_note", "")
    if reconciliation_note:
        rendered += f"\n\n## Reconciliation\n\n- {reconciliation_note}\n"

    return rendered


def write_landing_record(
    context: dict[str, Any],
    repo_root: str | Path,
    templates_dir: str | Path | None = None,
) -> Path:
    content = render_landing_record(context, templates_dir=templates_dir)
    target_dir = Path(repo_root) / "knowledge/sources/telegram"
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{context['landing_id']}.md"
    path.write_text(content)
    return path
