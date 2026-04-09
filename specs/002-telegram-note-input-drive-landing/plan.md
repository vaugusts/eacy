# Implementation Plan: Telegram Note Input with Google Drive Landing Zone

**Branch**: `002-telegram-note-input-drive-landing` | **Date**: 2026-04-09 | **Spec**: [spec.md](/Users/leo/Sources/Personal/eacy/specs/002-telegram-note-input-drive-landing/spec.md)
**Input**: Feature specification from `/specs/002-telegram-note-input-drive-landing/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Create the first production-oriented Telegram input channel for EACY. The
feature adds a FastAPI webhook flow in `apps.voice_gateway` that receives
Telegram note-bot updates, normalizes supported voice or audio messages into a
typed intake envelope, downloads audio through a Telegram adapter, transcribes
it through an OpenAI-backed transcription adapter, uploads Markdown and optional
audio to Google Drive through an OAuth user-token flow, and writes repo-native
landing records and manifests that preserve traceability and prepare later sync
into the normalized Git-based KMS.

## Technical Context

**Language/Version**: Python 3.12 for runtime tooling, Markdown/YAML/JSON for durable definitions  
**Primary Dependencies**: FastAPI, Pydantic v2, PyYAML, jsonschema, httpx, OpenAI Python SDK, google-api-python-client, google-auth, google-auth-oauthlib, pytest  
**Storage**: Git repository filesystem for repo-native landing records, manifests, and sync scaffolding; Google Drive for ingress-stage Markdown and optional raw audio; local OAuth credential and token files for Drive access  
**Testing**: pytest, schema validation tests, contract snapshot tests, integration tests with fixture Telegram updates and stubbed external adapters, Ruff  
**Target Platform**: macOS and Linux local-first runtime plus deployable webhook service endpoint  
**Project Type**: single-repo platform with FastAPI webhook service and adapter-based worker modules  
**Performance Goals**: validate and normalize webhook updates in under 1 second before external calls; complete end-to-end intake for short voice notes within 30 seconds under healthy provider latency; maintain idempotent retries for duplicate Telegram deliveries  
**Constraints**: OAuth user-token Google Drive authentication, repo-native manifests and landing records, idempotent Telegram retry handling, partial-success reconciliation, ingress-stage external Markdown only, no command or search channel changes in this feature  
**Scale/Scope**: single-user personal workflow with one dedicated Telegram bot, one Google Drive account, and repeated low-volume note capture over time

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution v1.2.0.

- **I. Repository-Native Backbone**: PASS. Telegram, OpenAI, and Google Drive
  behavior will be defined through repo-native schemas, contracts, manifests,
  configuration surfaces, and tests. External services perform transport and
  storage, but the repository remains the control plane.
- **II. Git-First Change Control**: PASS. The feature is expressed through a new
  spec package plus versioned runtime, schema, contract, and documentation
  files suitable for branch and PR review.
- **III. Markdown-First Curated Knowledge**: PASS. Google Drive Markdown is used
  only as an ingress-stage landing artifact under the v1.2.0 amendment. The
  repository retains human-readable landing records, machine-readable manifests,
  sync state, and future import logic, while normalized knowledge remains
  repo-native.
- **IV. Governed Voice-to-Action**: PASS. This feature adds capture-mode ingress
  only. It normalizes Telegram voice input into a typed intake envelope and does
  not bypass or modify the existing command or combined-mode safety model.
- **V. Policy-Gated Execution and Audit**: PASS. The feature does not add new
  governed command execution paths. Failure modes, reconciliation metadata, and
  typed external adapter contracts remain explicit and reviewable.
- **VI. Spec-Driven Incremental Evolution**: PASS. Scope is limited to one
  reviewable input-channel feature package with explicit contracts and future
  sync scaffolding.
- **VII. AI Agent Authorization and Oversight**: PASS. OpenAI is used only as a
  transcription backend through a repo-defined adapter. No new agent permission
  surfaces or command registry modifications are introduced.

**Exceptions**: None required. The constitution was already amended to v1.2.0
to allow ingress-stage external Markdown landing artifacts under repo-controlled
reconciliation.

## Project Structure

### Documentation (this feature)

```text
specs/002-telegram-note-input-drive-landing/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
apps/
├── router/
├── voice-gateway/
│   └── README.md
├── voice_gateway/
│   ├── combined_mode.py
│   ├── telegram_input_flow.py
│   └── telegram_webhook.py
└── workers/
    ├── asset_indexer.py
    ├── google_drive_adapter.py
    ├── landing_manifest_writer.py
    ├── landing_record_writer.py
    ├── telegram_adapter.py
    └── transcription_adapter.py

integrations/
├── google-drive/
├── openai/
└── telegram/

knowledge/
├── manifests/
│   └── telegram/
└── sources/
    └── telegram/

schemas/
├── landing-manifest.schema.json
├── landing-note.schema.json
├── telegram-intake-envelope.schema.json
└── telegram-update.schema.json

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Extend the existing `apps/`, `integrations/`,
`knowledge/`, `schemas/`, and `tests/` layout rather than introducing new
top-level runtime or KMS folders. Use `apps.voice_gateway` as the canonical
Python package for webhook orchestration, keep external API boundaries in
`apps/workers`, represent repo-native durable state in `knowledge/sources` and
`knowledge/manifests`, and document external interfaces through feature
contracts plus long-lived integration contracts.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
