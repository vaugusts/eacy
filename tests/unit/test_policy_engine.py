import unittest
from pathlib import Path

from apps.router.command_registry import load_command_registry
from apps.router.policy_engine import ActorContext, PolicyEngine, load_policy_definition


ROOT = Path(__file__).resolve().parents[2]


class PolicyEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_command_registry(ROOT / "registry/commands.yaml")
        cls.policy = load_policy_definition(ROOT / "policies/execution-policy.yaml")
        cls.engine = PolicyEngine(cls.policy)

    def test_denies_unknown_parameters(self) -> None:
        command = next(item for item in self.registry["commands"] if item["id"] == "note.capture.inbox")
        actor = ActorContext(actor_id="leo", actor_type="human", scopes=[])

        decision = self.engine.evaluate(
            command=command,
            actor=actor,
            parameters={"title": "ok", "unexpected": "boom"},
            channel="voice",
        )

        self.assertFalse(decision.allowed)
        self.assertEqual("deny", decision.effect)

    def test_requires_confirmation_for_medium_risk_voice_command(self) -> None:
        command = next(item for item in self.registry["commands"] if item["id"] == "assets.sync.drive")
        actor = ActorContext(actor_id="leo", actor_type="human", scopes=[])

        decision = self.engine.evaluate(
            command=command,
            actor=actor,
            parameters={"folder_id": "abc123"},
            channel="voice",
        )

        self.assertTrue(decision.allowed)
        self.assertTrue(decision.requires_confirmation)

    def test_denies_agent_without_allowed_scope(self) -> None:
        command = next(item for item in self.registry["commands"] if item["id"] == "topics.pack.generate")
        actor = ActorContext(actor_id="codex", actor_type="agent", scopes=["note-curator"])

        decision = self.engine.evaluate(
            command=command,
            actor=actor,
            parameters={"topic_slug": "voice-architecture"},
            channel="voice",
        )

        self.assertFalse(decision.allowed)
        self.assertEqual("deny", decision.effect)


if __name__ == "__main__":
    unittest.main()
