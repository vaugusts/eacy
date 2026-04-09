from __future__ import annotations

from pathlib import Path
from typing import Any

from apps.router.capture_router import process_capture_request
from apps.router.command_registry import get_command_by_id
from apps.workers.correlation import link_note_and_audit
from apps.workers.execution_dispatcher import dispatch_command


def process_combined_request(
    request: dict[str, Any],
    knowledge_dir: str | Path,
    registry: dict[str, Any],
    policy_engine: Any,
    actor: Any,
    repo_revision: str,
    audit_log_path: str | Path,
    templates_dir: str | Path | None = None,
) -> dict[str, Any]:
    note_result = process_capture_request(
        request,
        knowledge_dir=knowledge_dir,
        templates_dir=templates_dir,
    )

    command = get_command_by_id(registry, request["command_id"])
    command_result = dispatch_command(
        transcript=command["trigger_phrases"][0],
        registry=registry,
        policy_engine=policy_engine,
        actor=actor,
        parameters=request.get("command_parameters", {}),
        channel="voice",
        correlation_id=request["envelope_id"],
        repo_revision=repo_revision,
        audit_log_path=audit_log_path,
    )

    link_result = link_note_and_audit(
        note_path=note_result["path"],
        command_result=command_result,
        correlation_id=request["envelope_id"],
    )

    note_result["correlation_id"] = request["envelope_id"]

    return {
        "correlation_id": request["envelope_id"],
        "note": note_result,
        "command": command_result,
        "link": link_result,
    }
