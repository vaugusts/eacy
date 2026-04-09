from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from apps.router.schema_loader import (
    get_repo_root,
    load_json_schema,
    load_yaml_file,
    validate_against_schema,
)


@dataclass(frozen=True)
class ActorContext:
    actor_id: str
    actor_type: str
    scopes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    effect: str
    requires_confirmation: bool
    reasons: list[str] = field(default_factory=list)


def load_policy_definition(path: str | Path | None = None) -> dict[str, Any]:
    repo_root = get_repo_root()
    policy_path = Path(path) if path else repo_root / "policies/execution-policy.yaml"
    schema_path = repo_root / "schemas/policy-rule.schema.json"

    policy = load_yaml_file(policy_path)
    schema = load_json_schema(schema_path)
    validate_against_schema(policy, schema, context=str(policy_path))

    return policy


class PolicyEngine:
    def __init__(self, policy_definition: dict[str, Any]) -> None:
        self.policy_definition = policy_definition

    def evaluate(
        self,
        command: dict[str, Any],
        actor: ActorContext,
        parameters: dict[str, Any],
        channel: str,
    ) -> PolicyDecision:
        reasons: list[str] = []
        risk_level = command["risk_level"]
        risk_rule = self.policy_definition["risk_model"][risk_level]
        effect = risk_rule["effect"]
        allowed = effect != "deny"
        requires_confirmation = effect == "confirm"

        executor_type = command["executor"]["type"]
        if executor_type not in risk_rule["allow_executors"]:
            return PolicyDecision(
                allowed=False,
                effect="deny",
                requires_confirmation=False,
                reasons=[f"Executor {executor_type} is not allowed for risk level {risk_level}"],
            )

        unknown_parameters = sorted(set(parameters) - set(command["allowed_parameters"]))
        if unknown_parameters:
            return PolicyDecision(
                allowed=False,
                effect="deny",
                requires_confirmation=False,
                reasons=[f"Unknown parameters: {', '.join(unknown_parameters)}"],
            )

        for rule in self.policy_definition["rules"]:
            if not self._rule_matches(rule, command, actor, channel):
                continue

            if rule["effect"] == "deny":
                if rule["rule_id"] == "enforce-agent-scopes" and actor.actor_type == "agent":
                    allowed_scopes = set(command.get("allowed_agent_scopes", []))
                    if not allowed_scopes.intersection(actor.scopes):
                        return PolicyDecision(
                            allowed=False,
                            effect="deny",
                            requires_confirmation=False,
                            reasons=["Agent scope does not allow this command"],
                        )
                if rule["rule_id"] == "deny-unknown-parameter" and unknown_parameters:
                    return PolicyDecision(
                        allowed=False,
                        effect="deny",
                        requires_confirmation=False,
                        reasons=[f"Unknown parameters: {', '.join(unknown_parameters)}"],
                    )

            if rule["effect"] == "confirm":
                requires_confirmation = True
                allowed = True
                effect = "confirm"
                reasons.append(rule["rule_id"])

        return PolicyDecision(
            allowed=allowed,
            effect=effect if allowed else "deny",
            requires_confirmation=requires_confirmation if allowed else False,
            reasons=reasons,
        )

    def _rule_matches(
        self,
        rule: dict[str, Any],
        command: dict[str, Any],
        actor: ActorContext,
        channel: str,
    ) -> bool:
        applies_to = rule["applies_to"]
        conditions = rule.get("conditions", {})

        if applies_to == "any":
            return True

        if applies_to.startswith("risk_level="):
            expected = applies_to.split("=", 1)[1]
            if command["risk_level"] != expected:
                return False
            channels = conditions.get("channels")
            return channels is None or channel in channels

        if applies_to.startswith("actor_type="):
            expected = applies_to.split("=", 1)[1]
            return actor.actor_type == expected

        if applies_to.startswith("executor.type="):
            expected = applies_to.split("=", 1)[1]
            return command["executor"]["type"] == expected

        return False
