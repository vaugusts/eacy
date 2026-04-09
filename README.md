# EACY

EACY is a single-repo, Everything-as-Code backbone for voice-driven knowledge
management and governed automation. The repository holds the knowledge model,
command registry, execution policy, schemas, prompts, workflow definitions,
integration contracts, deployment assets, and the spec-driven artifacts used to
evolve the system safely.

Start with [docs/architecture/system-overview.md](/Users/leo/Sources/Personal/eacy/docs/architecture/system-overview.md),
the repo map in [docs/repo-tree.md](/Users/leo/Sources/Personal/eacy/docs/repo-tree.md),
and the initial feature package in
[specs/001-voice-kms-automation/spec.md](/Users/leo/Sources/Personal/eacy/specs/001-voice-kms-automation/spec.md).

## Current Runtime Coverage

- Capture mode writes inbox and daily Markdown notes with typed frontmatter.
- Command mode resolves registry entries, enforces policy, blocks unknown or
  unauthorized requests, and emits audit records.
- Combined mode writes knowledge first, then links the resulting note to the
  command decision through a shared correlation id.
- Optional adapters exist for GitHub Actions, n8n webhooks, and OpenClaw or
  Clawbot-style tool contracts.

## Validation Commands

Run these from the repo root:

```bash
python3 -m pytest
python3 -m unittest discover -s tests
ruff check .
python3 -m json.tool schemas/note.schema.json >/dev/null
```
