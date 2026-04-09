from __future__ import annotations

from pathlib import Path
from typing import Any

from apps.router.schema_loader import (
    SchemaValidationError,
    get_repo_root,
    load_json_schema,
    load_yaml_file,
    validate_against_schema,
)


def load_command_registry(path: str | Path | None = None) -> dict[str, Any]:
    repo_root = get_repo_root()
    registry_path = Path(path) if path else repo_root / "registry/commands.yaml"
    schema_path = repo_root / "schemas/command-registry.schema.json"

    registry = load_yaml_file(registry_path)
    schema = load_json_schema(schema_path)
    validate_against_schema(registry, schema, context=str(registry_path))

    return registry


def get_command_by_id(registry: dict[str, Any], command_id: str) -> dict[str, Any]:
    for command in registry["commands"]:
        if command["id"] == command_id:
            return command
    raise KeyError(command_id)


def match_trigger_phrase(registry: dict[str, Any], transcript: str) -> dict[str, Any]:
    normalized = transcript.strip().lower()
    for command in registry["commands"]:
        phrases = [phrase.strip().lower() for phrase in command["trigger_phrases"]]
        if normalized in phrases:
            return command
    raise SchemaValidationError(f"No command found for transcript: {transcript}")
