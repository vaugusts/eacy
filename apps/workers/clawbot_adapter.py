from __future__ import annotations

from pathlib import Path
from typing import Any

from apps.router.schema_loader import get_repo_root, load_yaml_file


def invoke_clawbot_tool(
    command: dict[str, Any],
    payload: dict[str, Any],
    contract_path: str | Path | None = None,
) -> dict[str, Any]:
    repo_root = get_repo_root()
    path = Path(contract_path) if contract_path else repo_root / "integrations/openclaw/voice-command-router.tool.yaml"
    contract = load_yaml_file(path)

    return {
        "status": "completed",
        "adapter": "clawbot_tool",
        "target": contract["tool"]["id"],
        "output_summary": (
            f"Simulated {contract['provider']} tool {contract['tool']['name']} "
            f"for correlation {payload['correlation_id']}"
        ),
        "artifact_refs": [str(path)],
    }
