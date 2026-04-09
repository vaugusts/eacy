---
schema_version: "1.0.0"
note_type: runbook
title: "Operations Runbook"
status: active
created_at: "2026-04-09T00:00:00Z"
updated_at: "2026-04-09T00:00:00Z"
tags:
  - operations
  - runbook
source_refs: []
topics:
  - system-operations
project_refs:
  - eacy
entity_refs: []
decision_refs: []
summary: "Starter runbook for validating and operating the repo-native backbone"
capture_mode: command
command_refs:
  - knowledge.digest.daily
  - assets.sync.drive
  - topics.pack.generate
---

## Validation

- Run `python3 -m pytest`.
- Run `python3 -m unittest discover -s tests`.
- Run `ruff check .`.
- Parse JSON schemas in `schemas/`.
- Review `specs/001-voice-kms-automation/quickstart.md` before implementation.

## Safety Checks

- Reject any command not declared in `registry/commands.yaml`.
- Confirm medium-risk and high-risk commands before execution.
- Append an audit record for every command decision and execution attempt.
- Combined-mode note writes must survive command denial, and the resulting note
  must include the correlation id and linked command metadata.

## Recovery

- If an integration contract fails validation, disable that executor in policy
  rather than bypassing policy checks.
- If a capture flow is ambiguous, route to inbox instead of forcing a command.

## Asset Sync

- Refresh `knowledge/assets/index.md` through the governed `assets.sync.drive`
  command path.
- Validate every imported asset record against
  `schemas/asset-index.schema.json`.
- Keep linked notes repo-relative so the asset index remains durable under git.

## Telegram Landing Sync Scaffold

- Inspect pending Telegram landing manifests under
  `knowledge/manifests/telegram/`.
- Use `apps.workers.drive_sync.enumerate_sync_candidates()` to list sync
  candidates and their decisions (`ready`, `pending`, `blocked`).
- Treat `sync.import_state=ready` with `sync.ready_for_import=true` as safe
  candidates for future normalization import jobs.
- Treat `sync.import_state=blocked` as reconciliation-required; resolve
  `sync.block_reason` and `reconciliation.recovery_hint` before import.
- Keep import decisions repo-native by updating manifests rather than relying on
  hidden runtime state.
