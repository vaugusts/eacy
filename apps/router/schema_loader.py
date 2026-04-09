from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


class SchemaValidationError(ValueError):
    """Raised when data does not satisfy the supported schema subset."""


def get_repo_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__)).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".specify").exists():
            return candidate
    raise FileNotFoundError("Unable to locate repository root")


def load_json_schema(path: str | Path) -> dict[str, Any]:
    schema_path = Path(path)
    return json.loads(schema_path.read_text())


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    yaml_path = Path(path)
    data = yaml.safe_load(yaml_path.read_text())
    if not isinstance(data, dict):
        raise SchemaValidationError(f"{yaml_path} did not parse into an object")
    return data


def validate_against_schema(instance: Any, schema: dict[str, Any], context: str = "$") -> None:
    schema_type = schema.get("type")

    if schema_type == "object" or ("properties" in schema and schema_type is None):
        _validate_object(instance, schema, context)
        return

    if schema_type == "array":
        _validate_array(instance, schema, context)
        return

    if schema_type == "string":
        _validate_string(instance, schema, context)
        return

    if schema_type == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            raise SchemaValidationError(f"{context} must be an integer")
        if "minimum" in schema and instance < schema["minimum"]:
            raise SchemaValidationError(f"{context} must be >= {schema['minimum']}")
        return

    if schema_type == "boolean":
        if not isinstance(instance, bool):
            raise SchemaValidationError(f"{context} must be a boolean")
        return

    if schema_type == "number":
        if not isinstance(instance, (int, float)) or isinstance(instance, bool):
            raise SchemaValidationError(f"{context} must be a number")
        return

    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaValidationError(f"{context} must be one of {schema['enum']}")


def _validate_object(instance: Any, schema: dict[str, Any], context: str) -> None:
    if not isinstance(instance, dict):
        raise SchemaValidationError(f"{context} must be an object")

    properties = schema.get("properties", {})
    required = schema.get("required", [])
    additional_properties = schema.get("additionalProperties", True)

    for field in required:
        if field not in instance:
            raise SchemaValidationError(f"{context}.{field} is required")

    if additional_properties is False:
        unexpected = set(instance) - set(properties)
        if unexpected:
            raise SchemaValidationError(f"{context} contains unexpected keys: {sorted(unexpected)}")

    for key, value in instance.items():
        if key in properties:
            validate_against_schema(value, properties[key], f"{context}.{key}")


def _validate_array(instance: Any, schema: dict[str, Any], context: str) -> None:
    if not isinstance(instance, list):
        raise SchemaValidationError(f"{context} must be an array")

    if "minItems" in schema and len(instance) < schema["minItems"]:
        raise SchemaValidationError(f"{context} must contain at least {schema['minItems']} items")

    if schema.get("uniqueItems"):
        normalized = [json.dumps(item, sort_keys=True) for item in instance]
        if len(normalized) != len(set(normalized)):
            raise SchemaValidationError(f"{context} items must be unique")

    item_schema = schema.get("items")
    if item_schema is not None:
        for index, item in enumerate(instance):
            validate_against_schema(item, item_schema, f"{context}[{index}]")


def _validate_string(instance: Any, schema: dict[str, Any], context: str) -> None:
    if not isinstance(instance, str):
        raise SchemaValidationError(f"{context} must be a string")

    if "minLength" in schema and len(instance) < schema["minLength"]:
        raise SchemaValidationError(f"{context} must be at least {schema['minLength']} characters")

    if "pattern" in schema and re.match(schema["pattern"], instance) is None:
        raise SchemaValidationError(f"{context} does not match required pattern")

    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaValidationError(f"{context} must be one of {schema['enum']}")

    if schema.get("format") == "date-time":
        try:
            datetime.fromisoformat(instance.replace("Z", "+00:00"))
        except ValueError as exc:
            raise SchemaValidationError(f"{context} must be a valid date-time") from exc
