# Tasks: Telegram Note Input with Google Drive Landing Zone

**Input**: Design documents from `/specs/002-telegram-note-input-drive-landing/`  
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Include contract validation, schema validation, unit tests, and integration tests for webhook intake, partial failures, retries, and sync scaffolding as implementation begins.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Constitution v1.2.0 obligations around ingress-stage external Markdown, repo-native manifests, and reconciliation are enforced through Phase 2 foundational tasks.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the directories, placeholders, and fixtures needed to implement the Telegram intake feature without introducing a parallel repo structure.

- [ ] T001 Create repo-native integration placeholders in integrations/telegram/README.md, integrations/openai/README.md, and integrations/google-drive/README.md
- [ ] T002 [P] Create repo-native landing directories with README placeholders in knowledge/sources/telegram/README.md and knowledge/manifests/telegram/README.md
- [ ] T003 [P] Add fixture scaffolding for Telegram and provider responses in tests/fixtures/telegram_voice_update.json, tests/fixtures/telegram_unsupported_update.json, and tests/fixtures/telegram_file_download.json
- [ ] T004 [P] Update runtime overview for Telegram intake in apps/voice-gateway/README.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define the schemas, templates, contracts, and repo-level validation hooks that every Telegram intake story depends on.

- [ ] T005 Define Telegram update schema in schemas/telegram-update.schema.json
- [ ] T006 Define Telegram intake envelope schema in schemas/telegram-intake-envelope.schema.json
- [ ] T007 Define dedicated landing-note schema in schemas/landing-note.schema.json
- [ ] T008 Define landing-manifest schema in schemas/landing-manifest.schema.json
- [ ] T009 [P] Add repo-native integration contracts in integrations/telegram/note-input-webhook.contract.yaml, integrations/openai/transcription.contract.yaml, and integrations/google-drive/telegram-landing.contract.yaml
- [ ] T010 [P] Add feature contract tests in tests/contract/test_telegram_input_contracts.py
- [ ] T011 [P] Extend integration contract coverage in tests/contract/test_integration_contracts.py for Telegram, OpenAI, and Google Drive landing contracts
- [ ] T012 [P] Extend schema parsing coverage in tests/contract/test_schema_files.py for telegram-update, telegram-intake-envelope, landing-note, and landing-manifest schemas
- [ ] T013 Create Telegram landing Markdown template in templates/notes/telegram-landing.md
- [ ] T014 Update repo backbone validation for Telegram intake assets in apps/router/repo_lint.py and tests/integration/test_repo_backbone.py

**Checkpoint**: The repo can validate the new Telegram intake schemas, contracts, landing-note template, and required repo-native paths before runtime code is added.

---

## Phase 3: User Story 1 - Capture a Telegram Voice Note into Landing Artifacts (Priority: P1) 🎯 MVP

**Goal**: Accept a supported Telegram voice or audio update and land it as Drive-backed Markdown plus repo-native landing records.

**Independent Test**: A fixture Telegram voice update can hit the webhook, download audio, transcribe it, upload Markdown to Drive, optionally upload audio, and write linked repo-native landing artifacts with stable identifiers.

- [ ] T015 [P] [US1] Add unit tests for Telegram update normalization in tests/unit/test_telegram_adapter.py
- [ ] T016 [P] [US1] Add unit tests for transcription adapter behavior in tests/unit/test_transcription_adapter.py
- [ ] T017 [P] [US1] Add unit tests for Google Drive upload behavior in tests/unit/test_google_drive_adapter.py
- [ ] T018 [P] [US1] Add unit tests for landing record rendering in tests/unit/test_landing_record_writer.py
- [ ] T019 [P] [US1] Add integration test for successful Telegram note intake in tests/integration/test_telegram_note_input.py
- [ ] T020 [US1] Implement Telegram API adapter and intake envelope normalization in apps/workers/telegram_adapter.py
- [ ] T021 [US1] Implement transcription adapter interface and OpenAI-backed transcription in apps/workers/transcription_adapter.py
- [ ] T022 [US1] Implement Google Drive OAuth uploader for Markdown and optional audio in apps/workers/google_drive_adapter.py
- [ ] T023 [US1] Implement repo-native landing record writer in apps/workers/landing_record_writer.py
- [ ] T024 [US1] Implement success-path landing manifest writer in apps/workers/landing_manifest_writer.py
- [ ] T025 [US1] Implement Telegram note-input orchestration in apps/voice_gateway/telegram_input_flow.py
- [ ] T026 [US1] Implement FastAPI Telegram webhook endpoint in apps/voice_gateway/telegram_webhook.py

**Checkpoint**: Telegram note input works end to end for the success path and leaves stable repo-native landing artifacts.

---

## Phase 4: User Story 2 - Preserve Traceability Through Partial Failures and Retries (Priority: P2)

**Goal**: Make the Telegram intake flow recoverable under partial failures and duplicate webhook deliveries.

**Independent Test**: A Drive-success and repo-write-failure scenario returns recoverable reconciliation data, and repeated Telegram delivery resolves idempotently instead of creating duplicates.

- [ ] T027 [P] [US2] Add unit tests for manifest state transitions and reconciliation data in tests/unit/test_landing_manifest_writer.py
- [ ] T028 [P] [US2] Add integration test for duplicate Telegram retry handling in tests/integration/test_telegram_note_retries.py
- [ ] T029 [P] [US2] Add integration test for Drive-success repo-write-failure reconciliation in tests/integration/test_telegram_partial_failures.py
- [ ] T030 [US2] Extend landing manifest reconciliation and retry tracking in apps/workers/landing_manifest_writer.py
- [ ] T031 [US2] Extend Google Drive upload results with partial-success and recovery metadata in apps/workers/google_drive_adapter.py
- [ ] T032 [US2] Extend Telegram input orchestration with idempotent retry handling and partial-success outcomes in apps/voice_gateway/telegram_input_flow.py
- [ ] T033 [US2] Extend repo landing record rendering for partial, failed, and reconciled states in apps/workers/landing_record_writer.py

**Checkpoint**: The intake flow remains deterministic and recoverable under retries and partial failures.

---

## Phase 5: User Story 3 - Prepare Drive-Backed Notes for Later KMS Normalization (Priority: P3)

**Goal**: Expose repo-native sync state and a scaffolded import path for future normalization of Drive landing Markdown into the long-term KMS.

**Independent Test**: A sync-oriented module can enumerate pending landing manifests, determine import readiness from repo-native state, and explain why a note is blocked or ready.

- [ ] T034 [P] [US3] Add unit tests for sync candidate enumeration in tests/unit/test_drive_sync.py
- [ ] T035 [P] [US3] Add integration test for pending-import manifest scanning in tests/integration/test_drive_sync_scaffold.py
- [ ] T036 [US3] Implement sync candidate enumeration and decision scaffolding in apps/workers/drive_sync.py
- [ ] T037 [US3] Extend landing manifest writer to persist sync-import readiness metadata in apps/workers/landing_manifest_writer.py
- [ ] T038 [US3] Add sync workflow operator guidance in knowledge/references/operations-runbook.md

**Checkpoint**: Repo-native manifests and sync scaffolding are sufficient to drive a future import workflow without hidden runtime state.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finish operator guidance, verification coverage, and feature-level validation across all Telegram intake stories.

- [ ] T039 [P] Update README.md and apps/voice-gateway/README.md with Telegram bot, webhook, OAuth token, and landing-zone setup guidance
- [ ] T040 [P] Add feature quickstart walkthrough validation in specs/002-telegram-note-input-drive-landing/quickstart.md and tests/integration/test_repo_backbone.py
- [ ] T041 Run quickstart validation from specs/002-telegram-note-input-drive-landing/quickstart.md
- [ ] T042 Run repository verification for pyproject.toml and specs/002-telegram-note-input-drive-landing/tasks.md with python3 -m pytest and ruff check .

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; can start immediately.
- **Foundational (Phase 2)**: Depends on Setup; BLOCKS all user stories.
- **User Story 1 (Phase 3)**: Starts after Phase 2 and delivers the MVP vertical slice.
- **User Story 2 (Phase 4)**: Depends on User Story 1 because it extends the success-path flow with retries and reconciliation.
- **User Story 3 (Phase 5)**: Depends on User Story 1 for manifests and landing records, and should follow User Story 2 so sync logic sees the final state model.
- **Polish (Phase 6)**: Follows whichever user stories are in scope for the increment.

### Within-Story Dependencies

- T005-T008 (schemas) block T010-T012 (contract and schema tests).
- T009-T014 (contracts, template, repo validation) block User Story 1 runtime work.
- T020-T024 block T025 and T026.
- T024 and T025 block T030, T032, and T037.
- T030-T033 block T036 and T038.

### Parallel Opportunities

- In Phase 1, T002-T004 can run in parallel after T001.
- In Phase 2, T005-T009 can run in parallel by file, followed by T010-T012 in parallel.
- In User Story 1, T015-T019 can run in parallel before implementation tasks start.
- In User Story 2, T027-T029 can run in parallel before reconciliation logic changes.
- In User Story 3, T034 and T035 can run in parallel before sync scaffold implementation.

## Parallel Example: User Story 1

```bash
# Launch story-specific tests together before runtime implementation
Task: "T015 [US1] Add unit tests for Telegram update normalization in tests/unit/test_telegram_adapter.py"
Task: "T016 [US1] Add unit tests for transcription adapter behavior in tests/unit/test_transcription_adapter.py"
Task: "T017 [US1] Add unit tests for Google Drive upload behavior in tests/unit/test_google_drive_adapter.py"
Task: "T018 [US1] Add unit tests for landing record rendering in tests/unit/test_landing_record_writer.py"
Task: "T019 [US1] Add integration test for successful Telegram note intake in tests/integration/test_telegram_note_input.py"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Deliver User Story 1 end to end.
3. Validate Telegram intake with the new integration, contract, and schema tests.
4. Stop and review before expanding retry and sync behavior.

### Incremental Delivery

1. Build the success-path Telegram landing flow first.
2. Add retries, partial-success handling, and reconciliation second.
3. Add sync scaffolding third.
4. Finish with operator docs and full verification.
