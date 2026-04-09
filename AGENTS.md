# eacy Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-04-09

## Active Technologies

- Python 3.12 for runtime tooling
- Markdown, YAML, and JSON for durable system definitions
- Pydantic v2, PyYAML, jsonschema, Typer, FastAPI
- pytest and Ruff for validation

## Project Structure

```text
apps/
├── router/
├── voice-gateway/
└── workers/

automation/workflows/
docs/
deploy/
integrations/
knowledge/
policies/
prompts/
registry/
schemas/
specs/
templates/
tests/
```

## Commands

- `python3 -m pytest`
- `python3 -m json.tool schemas/note.schema.json`
- `ruff check .`
- `find specs/001-voice-kms-automation -maxdepth 2 -type f | sort`

## Code Style

Keep durable definitions human-readable and repo-native. Prefer typed contracts,
small focused Python modules, Markdown with structured frontmatter, and
deterministic execution rules over free-form automation.

## Recent Changes

- `001-voice-kms-automation`: added the initial constitution, architecture,
  spec-driven feature package, schemas, registry, policy files, note templates,
  starter integration contracts, and workflow samples.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
