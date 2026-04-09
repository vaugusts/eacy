import unittest
from pathlib import Path

from apps.router.schema_loader import load_json_schema


ROOT = Path(__file__).resolve().parents[2]


class SchemaFileTests(unittest.TestCase):
    def test_foundation_schema_files_exist_and_parse(self) -> None:
        expected = [
            "schemas/command-registry.schema.json",
            "schemas/policy-rule.schema.json",
            "schemas/audit-entry.schema.json",
        ]

        for relative_path in expected:
            schema = load_json_schema(ROOT / relative_path)
            self.assertEqual(schema["type"], "object", relative_path)

    def test_command_registry_schema_requires_agent_scopes(self) -> None:
        schema = load_json_schema(ROOT / "schemas/command-registry.schema.json")
        command_item = schema["properties"]["commands"]["items"]
        required = set(command_item["required"])

        self.assertIn("allowed_agent_scopes", required)

    def test_policy_rule_schema_covers_agent_scope_constraints(self) -> None:
        schema = load_json_schema(ROOT / "schemas/policy-rule.schema.json")
        conditions = schema["properties"]["rules"]["items"]["properties"]["conditions"]["properties"]

        self.assertIn("allowed_agent_scopes", conditions)
        self.assertIn("require_allowed_parameters", conditions)

    def test_audit_entry_schema_requires_governance_fields(self) -> None:
        schema = load_json_schema(ROOT / "schemas/audit-entry.schema.json")
        required = set(schema["required"])

        for field in ["actor", "intent", "approved_command", "target", "outcome", "repo_revision"]:
            self.assertIn(field, required)


if __name__ == "__main__":
    unittest.main()
