from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from apps.router.intent_resolver import resolve_command_intent
from apps.router.policy_engine import ActorContext, PolicyEngine
from apps.router.schema_loader import SchemaValidationError
from apps.workers.audit_logger import AuditLogger
from apps.workers.clawbot_adapter import invoke_clawbot_tool
from apps.workers.github_actions_adapter import dispatch_github_action
from apps.workers.n8n_adapter import dispatch_n8n_webhook


def dispatch_command(
    transcript: str,
    registry: dict[str, Any],
    policy_engine: PolicyEngine,
    actor: ActorContext,
    parameters: dict[str, Any],
    channel: str,
    correlation_id: str,
    repo_revision: str,
    audit_log_path: str | Path,
) -> dict[str, Any]:
    audit_logger = AuditLogger(log_path=audit_log_path)

    try:
        command = resolve_command_intent(registry, transcript)
    except SchemaValidationError:
        audit_logger.write(
            _build_unknown_command_audit_record(
                actor=actor,
                transcript=transcript,
                repo_revision=repo_revision,
                correlation_id=correlation_id,
            )
        )
        return {
            "command_id": "unknown",
            "correlation_id": correlation_id,
            "status": "blocked",
            "decision": "deny",
            "reasons": ["Unknown command transcript"],
            "error_message": "Unknown command transcript",
        }

    decision = policy_engine.evaluate(
        command=command,
        actor=actor,
        parameters=parameters,
        channel=channel,
    )

    if not decision.allowed:
        audit_logger.write(
            _build_audit_record(
                actor=actor,
                transcript=transcript,
                command=command,
                outcome="blocked",
                repo_revision=repo_revision,
                correlation_id=correlation_id,
            )
        )
        return {
            "command_id": command["id"],
            "correlation_id": correlation_id,
            "status": "blocked",
            "decision": "deny",
            "reasons": decision.reasons,
            "error_message": "; ".join(decision.reasons) or "Command denied by policy",
        }

    if decision.requires_confirmation:
        reasons = decision.reasons + ["Command requires confirmation before execution"]
        audit_logger.write(
            _build_audit_record(
                actor=actor,
                transcript=transcript,
                command=command,
                outcome="blocked",
                repo_revision=repo_revision,
                correlation_id=correlation_id,
            )
        )
        return {
            "command_id": command["id"],
            "correlation_id": correlation_id,
            "status": "blocked",
            "decision": "confirm",
            "reasons": reasons,
            "error_message": "Command requires confirmation before execution",
        }

    if command["executor"]["type"] == "github_action":
        adapter_result = dispatch_github_action(
            command,
            {
                "correlation_id": correlation_id,
                "parameters": parameters,
                "actor": actor.actor_id,
            },
        )
    elif command["executor"]["type"] == "n8n_webhook":
        adapter_result = dispatch_n8n_webhook(
            command,
            {
                "correlation_id": correlation_id,
                "parameters": parameters,
                "actor": actor.actor_id,
                "command_id": command["id"],
            },
        )
    elif command["executor"]["type"] == "clawbot_tool":
        adapter_result = invoke_clawbot_tool(
            command,
            {
                "correlation_id": correlation_id,
                "parameters": parameters,
                "actor": actor.actor_id,
                "command_id": command["id"],
            },
        )
    else:
        adapter_result = {
            "status": "completed",
            "adapter": command["executor"]["type"],
            "target": command["executor"]["target"],
            "output_summary": f"Simulated executor {command['executor']['type']}",
            "artifact_refs": [command["executor"]["target"]],
        }

    audit_logger.write(
        _build_audit_record(
            actor=actor,
            transcript=transcript,
            command=command,
            outcome="succeeded",
            repo_revision=repo_revision,
            correlation_id=correlation_id,
        )
    )

    return {
        "command_id": command["id"],
        "correlation_id": correlation_id,
        "status": adapter_result["status"],
        "decision": "allowed",
        "reasons": decision.reasons,
        "output_summary": adapter_result["output_summary"],
        "artifact_refs": adapter_result["artifact_refs"],
    }


def _build_audit_record(
    actor: ActorContext,
    transcript: str,
    command: dict[str, Any],
    outcome: str,
    repo_revision: str,
    correlation_id: str,
) -> dict[str, Any]:
    return {
        "audit_id": f"{correlation_id}-{command['id']}",
        "occurred_at": _utc_now_iso(),
        "actor": actor.actor_id,
        "intent": transcript,
        "approved_command": command["id"],
        "target": command["executor"]["target"],
        "outcome": outcome,
        "repo_revision": repo_revision,
        "risk_level": command["risk_level"],
        "correlation_id": correlation_id,
    }


def _build_unknown_command_audit_record(
    actor: ActorContext,
    transcript: str,
    repo_revision: str,
    correlation_id: str,
) -> dict[str, Any]:
    return {
        "audit_id": f"{correlation_id}-unknown",
        "occurred_at": _utc_now_iso(),
        "actor": actor.actor_id,
        "intent": transcript,
        "approved_command": "unknown",
        "target": "unresolved",
        "outcome": "blocked",
        "repo_revision": repo_revision,
        "risk_level": "blocked",
        "correlation_id": correlation_id,
    }


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
