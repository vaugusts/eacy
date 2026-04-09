from __future__ import annotations

from pathlib import Path
from typing import Any

from apps.router.schema_loader import get_repo_root, load_yaml_file


def dispatch_n8n_webhook(
    command: dict[str, Any],
    payload: dict[str, Any],
    contract_path: str | Path | None = None,
) -> dict[str, Any]:
    repo_root = get_repo_root()
    path = Path(contract_path) if contract_path else repo_root / command["executor"]["target"]
    contract = load_yaml_file(path)

    if command["id"] not in contract["supported_commands"]:
        raise ValueError(f"Command {command['id']} is not supported by {path}")

    return {
        "status": "accepted",
        "adapter": "n8n_webhook",
        "target": f"{contract['webhook']['method']} {contract['webhook']['path']}",
        "output_summary": (
            f"Accepted by n8n contract {contract['contract_id']} "
            f"for correlation {payload['correlation_id']}"
        ),
        "artifact_refs": [str(path)],
    }
