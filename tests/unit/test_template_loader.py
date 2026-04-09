import unittest
from pathlib import Path

from apps.router.template_loader import load_note_template


ROOT = Path(__file__).resolve().parents[2]


class TemplateLoaderTests(unittest.TestCase):
    def test_loads_named_note_template(self) -> None:
        template = load_note_template("inbox", templates_dir=ROOT / "templates/notes")

        self.assertIn("note_type: inbox", template)
        self.assertIn("{{transcript}}", template)


if __name__ == "__main__":
    unittest.main()
