from __future__ import annotations

from pathlib import Path
from typing import Any

from apps.router.note_writer import _render_frontmatter, _validate_note_frontmatter, parse_frontmatter
from apps.router.template_loader import load_note_template


def append_to_daily_note(
    request: dict[str, Any],
    knowledge_dir: str | Path,
    templates_dir: str | Path | None = None,
) -> dict[str, Any]:
    base_dir = Path(knowledge_dir) / "daily"
    base_dir.mkdir(parents=True, exist_ok=True)
    date = request["captured_at"][:10]
    path = base_dir / f"{date}.md"

    if path.exists():
        frontmatter, body = parse_frontmatter(path.read_text())
    else:
        template = load_note_template("daily", templates_dir=templates_dir)
        seeded = template.replace("{{date}}", date).replace("{{timestamp}}", request["captured_at"])
        frontmatter, body = parse_frontmatter(seeded)

    frontmatter["updated_at"] = request["captured_at"]
    frontmatter["topics"] = _merge_lists(frontmatter.get("topics", []), request.get("context", {}).get("topic_refs", []))
    frontmatter["project_refs"] = _merge_lists(frontmatter.get("project_refs", []), request.get("context", {}).get("project_refs", []))
    frontmatter["source_refs"] = _merge_source_refs(frontmatter.get("source_refs", []), request)
    _validate_note_frontmatter(frontmatter)

    capture_line = f"- {request['transcript']} (`{request['envelope_id']}`)"
    body = _insert_capture_line(body, capture_line)
    path.write_text(_render_frontmatter(frontmatter) + body)

    return {
      "note_type": "daily",
      "path": path,
      "frontmatter": frontmatter,
    }


def _insert_capture_line(body: str, capture_line: str) -> str:
    marker = "## Captures\n\n"
    if marker in body:
        head, tail = body.split(marker, 1)
        if tail.startswith("- \n"):
            tail = tail.replace("- \n", "", 1)
        return f"{head}{marker}{capture_line}\n{tail}"
    return body.rstrip() + f"\n\n## Captures\n\n{capture_line}\n"


def _merge_lists(existing: list[str], new_items: list[str]) -> list[str]:
    return list(dict.fromkeys(existing + new_items))


def _merge_source_refs(existing: list[dict[str, Any]], request: dict[str, Any]) -> list[dict[str, Any]]:
    candidate = {
        "source_type": "voice",
        "ref": request["envelope_id"],
        "captured_at": request["captured_at"],
    }
    refs = [item for item in existing if item.get("ref") != request["envelope_id"]]
    refs.append(candidate)
    return refs
