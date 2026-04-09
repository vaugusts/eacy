import json
import time
import unittest
from pathlib import Path

from apps.router.command_registry import load_command_registry
from apps.router.intent_resolver import resolve_command_intent
from apps.router.policy_engine import ActorContext, PolicyEngine, load_policy_definition


ROOT = Path(__file__).resolve().parents[2]


class RoutingLatencyTests(unittest.TestCase):
    def test_registry_backed_routing_smoke_test_finishes_under_two_seconds(self) -> None:
        fixture = json.loads((ROOT / "tests/fixtures/command_requests.json").read_text())["daily_digest"]
        registry = load_command_registry(ROOT / "registry/commands.yaml")
        engine = PolicyEngine(load_policy_definition(ROOT / "policies/execution-policy.yaml"))
        actor = ActorContext(**fixture["actor"])

        start = time.perf_counter()
        for _ in range(250):
            command = resolve_command_intent(registry, fixture["transcript"])
            decision = engine.evaluate(
                command=command,
                actor=actor,
                parameters=fixture["parameters"],
                channel=fixture["channel"],
            )
            self.assertTrue(decision.allowed)
        elapsed = time.perf_counter() - start

        self.assertLess(elapsed, 2.0)


if __name__ == "__main__":
    unittest.main()
