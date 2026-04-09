import subprocess
import unittest
from pathlib import Path

from apps.router.repo_lint import REQUIRED_PATHS, validate_repo_backbone


ROOT = Path(__file__).resolve().parents[2]


class RepoBackboneTests(unittest.TestCase):
    def test_repo_backbone_validation_reports_required_paths(self) -> None:
        report = validate_repo_backbone(ROOT)

        self.assertTrue(report.is_valid, report.errors)
        missing = {item.path for item in report.items if not item.exists}
        self.assertFalse(missing)
        required = {str(path) for path in REQUIRED_PATHS}
        present = {item.path for item in report.items}
        self.assertTrue(required.issubset(present))

    def test_cli_validate_repo_command_succeeds(self) -> None:
        result = subprocess.run(
            ["python3", "-m", "apps.router.cli", "validate-repo"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Repository backbone validation passed", result.stdout)
        self.assertIn("registry/commands.yaml", result.stdout)
        self.assertIn("schemas/telegram-update.schema.json", result.stdout)

    def test_validate_repo_workflow_runs_on_pull_requests(self) -> None:
        workflow_path = ROOT / ".github/workflows/validate-repo.yml"
        workflow_text = workflow_path.read_text()

        self.assertIn("pull_request:", workflow_text)
        self.assertIn("python3 -m unittest discover -s tests", workflow_text)
        self.assertIn("python3 -m apps.router.cli validate-repo", workflow_text)

    def test_feature_quickstart_contains_validation_walkthrough(self) -> None:
        quickstart = (ROOT / "specs/002-telegram-note-input-drive-landing/quickstart.md").read_text()

        self.assertIn("python3 -m pytest tests/contract/test_telegram_input_contracts.py", quickstart)
        self.assertIn("tests/integration/test_telegram_note_retries.py", quickstart)
        self.assertIn("tests/integration/test_drive_sync_scaffold.py", quickstart)
        self.assertIn("ruff check .", quickstart)


if __name__ == "__main__":
    unittest.main()
