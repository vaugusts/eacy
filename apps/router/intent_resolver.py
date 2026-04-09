from __future__ import annotations

from typing import Any

from apps.router.command_registry import match_trigger_phrase


def resolve_command_intent(registry: dict[str, Any], transcript: str) -> dict[str, Any]:
    return match_trigger_phrase(registry, transcript)
