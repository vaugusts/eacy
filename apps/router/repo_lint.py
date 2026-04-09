from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from apps.router.schema_loader import get_repo_root


REQUIRED_PATHS = [
    Path(".specify/memory/constitution.md"),
    Path("README.md"),
    Path("registry/commands.yaml"),
    Path("policies/execution-policy.yaml"),
    Path("schemas/command-registry.schema.json"),
    Path("schemas/policy-rule.schema.json"),
    Path("schemas/audit-entry.schema.json"),
    Path("automation/workflows/daily-topic-aggregation.yaml"),
    Path("templates/notes/inbox.md"),
    Path("knowledge/assets/index.md"),
    Path("prompts/system/note-curation.md"),
    Path("deploy/targets.yaml"),
    Path("schemas/telegram-update.schema.json"),
    Path("schemas/telegram-intake-envelope.schema.json"),
    Path("schemas/landing-note.schema.json"),
    Path("schemas/landing-manifest.schema.json"),
    Path("integrations/telegram/note-input-webhook.contract.yaml"),
    Path("integrations/openai/transcription.contract.yaml"),
    Path("integrations/google-drive/telegram-landing.contract.yaml"),
    Path("templates/notes/telegram-landing.md"),
    Path("knowledge/sources/telegram/README.md"),
    Path("knowledge/manifests/telegram/README.md"),
]


@dataclass(frozen=True)
class ValidationItem:
    path: str
    exists: bool


@dataclass(frozen=True)
class RepoValidationReport:
    is_valid: bool
    items: list[ValidationItem]
    errors: list[str]


def validate_repo_backbone(repo_root: str | Path | None = None) -> RepoValidationReport:
    root = Path(repo_root) if repo_root else get_repo_root()
    items: list[ValidationItem] = []
    errors: list[str] = []

    for relative_path in REQUIRED_PATHS:
        target = root / relative_path
        exists = target.exists()
        items.append(ValidationItem(path=str(relative_path), exists=exists))
        if not exists:
            errors.append(f"Missing required repo-native file: {relative_path}")

    return RepoValidationReport(
        is_valid=not errors,
        items=items,
        errors=errors,
    )


def format_report(report: RepoValidationReport) -> str:
    lines = []
    header = "Repository backbone validation passed" if report.is_valid else "Repository backbone validation failed"
    lines.append(header)
    lines.append("")
    for item in report.items:
        status = "OK" if item.exists else "MISSING"
        lines.append(f"- [{status}] {item.path}")
    if report.errors:
        lines.append("")
        lines.append("Errors:")
        for error in report.errors:
            lines.append(f"- {error}")
    return "\n".join(lines)
