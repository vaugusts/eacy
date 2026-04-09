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

## Telegram Intake Setup (Feature 002)

Feature 002 adds a Telegram voice-note ingress channel with Drive landing-zone
artifacts and repo-native manifests.

Required environment variables for local setup:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`
- `GOOGLE_DRIVE_FOLDER_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET_FILE`
- `GOOGLE_OAUTH_TOKEN_FILE`

Quick validation path:

```bash
python3 -m pytest tests/integration/test_telegram_note_input.py
python3 -m pytest tests/integration/test_telegram_note_retries.py
python3 -m pytest tests/integration/test_telegram_partial_failures.py
python3 -m pytest tests/integration/test_drive_sync_scaffold.py
```
