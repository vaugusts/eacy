from __future__ import annotations

from pathlib import Path

from apps.router.schema_loader import get_repo_root


def load_note_template(template_name: str, templates_dir: str | Path | None = None) -> str:
    base_dir = Path(templates_dir) if templates_dir else get_repo_root() / "templates/notes"
    suffix = "" if template_name.endswith(".md") else ".md"
    template_path = base_dir / f"{template_name}{suffix}"

    return template_path.read_text()
