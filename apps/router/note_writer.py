from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from apps.router.schema_loader import get_repo_root, load_json_schema, validate_against_schema
from apps.router.template_loader import load_note_template


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        raise ValueError("Markdown does not start with frontmatter")

    _, rest = markdown.split("---\n", 1)
    frontmatter_text, body = rest.split("\n---\n", 1)
    frontmatter = yaml.safe_load(frontmatter_text) or {}
    return frontmatter, body


def render_inbox_note(
    request: dict[str, Any],
    templates_dir: str | Path | None = None,
) -> dict[str, Any]:
    template = load_note_template("inbox", templates_dir=templates_dir)
    timestamp = request["captured_at"]
    title = request.get("parameters", {}).get("title") or _title_from_transcript(request["transcript"])
    slug = _slugify(title)

    content = (
        template.replace("{{slug}}", slug)
        .replace("{{timestamp}}", timestamp)
        .replace("{{envelope_id}}", request["envelope_id"])
        .replace("{{transcript}}", request["transcript"])
    )

    frontmatter, body = parse_frontmatter(content)
    frontmatter["title"] = title
    frontmatter["tags"] = list(dict.fromkeys(frontmatter["tags"] + request.get("parameters", {}).get("tags", [])))
    frontmatter["topics"] = request.get("context", {}).get("topic_refs", [])
    frontmatter["project_refs"] = request.get("context", {}).get("project_refs", [])

    _validate_note_frontmatter(frontmatter)
    rendered = _render_frontmatter(frontmatter) + body

    return {
        "path_name": f"{slug}.md",
        "title": title,
        "content": rendered,
        "frontmatter": frontmatter,
    }


def write_inbox_note(
    request: dict[str, Any],
    knowledge_dir: str | Path,
    templates_dir: str | Path | None = None,
) -> dict[str, Any]:
    rendered = render_inbox_note(request, templates_dir=templates_dir)
    base_dir = Path(knowledge_dir) / "inbox"
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / rendered["path_name"]
    path.write_text(rendered["content"])

    return {
        "note_type": "inbox",
        "path": path,
        "frontmatter": rendered["frontmatter"],
    }


def _validate_note_frontmatter(frontmatter: dict[str, Any]) -> None:
    repo_root = get_repo_root()
    schema = load_json_schema(repo_root / "schemas/note.schema.json")
    validate_against_schema(frontmatter, schema, context="note_frontmatter")


def _render_frontmatter(frontmatter: dict[str, Any]) -> str:
    yaml_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=False).strip()
    return f"---\n{yaml_text}\n---\n"


def _slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "capture"


def _title_from_transcript(transcript: str) -> str:
    trimmed = transcript.strip()
    if len(trimmed) <= 60:
        return trimmed
    return trimmed[:57].rstrip() + "..."
