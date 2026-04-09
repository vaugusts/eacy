# Quickstart

## Goal

Validate that the Telegram note-input feature package contains the planning and
contract artifacts needed before implementation begins.

## 1. Review the Feature Spec and Plan

Open:

- `/specs/002-telegram-note-input-drive-landing/spec.md`
- `/specs/002-telegram-note-input-drive-landing/plan.md`

Expected outcome: the feature scope, structure, constitution alignment, and
technical approach are clear before any code changes start.

## 2. Inspect the Planning Artifact Bundle

From the repo root:

```bash
find specs/002-telegram-note-input-drive-landing -maxdepth 2 -type f | sort
```

Expected outcome: `spec.md`, `plan.md`, `research.md`, `data-model.md`,
`quickstart.md`, and `contracts/` are present.

## 3. Review Existing Repo Boundaries the Feature Will Extend

Open:

- `/apps/voice_gateway/combined_mode.py`
- `/apps/router/note_writer.py`
- `/apps/workers/asset_indexer.py`
- `/schemas/note.schema.json`

Expected outcome: the feature extends the current `apps/`, `workers/`,
`schemas/`, and `knowledge/` conventions instead of creating a parallel runtime
or KMS structure.

## 4. Inspect the Feature Contracts

```bash
find specs/002-telegram-note-input-drive-landing/contracts -maxdepth 1 -type f | sort
```

Expected outcome: Telegram intake, landing manifest, and sync candidate
contracts are visible as versioned design artifacts.

## 5. Verify the Locked Design Decisions

```bash
rg -n "OAuth user-token|partial-success|idempotent|landing-note schema|sync_state" \
  specs/002-telegram-note-input-drive-landing/*.md \
  specs/002-telegram-note-input-drive-landing/contracts/*.yaml
```

Expected outcome: the feature artifacts explicitly capture OAuth user-token
Drive auth, retry idempotency, partial-success reconciliation, dedicated landing
schema usage, and sync-state handling.

## 6. Continue with Tasks

Generate `/specs/002-telegram-note-input-drive-landing/tasks.md` from this
artifact set before implementation begins.
