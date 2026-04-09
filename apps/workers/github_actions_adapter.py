from __future__ import annotations

from typing import Any


def dispatch_github_action(command: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "completed",
        "adapter": "github_action",
        "target": command["executor"]["target"],
        "output_summary": (
            f"Simulated workflow dispatch to {command['executor']['target']} "
            f"for correlation {payload['correlation_id']}"
        ),
        "artifact_refs": [command["executor"]["target"]],
    }
