# Tasks: Everything-as-Code Voice-Driven Knowledge Backbone

**Input**: Design documents from `/specs/001-voice-kms-automation/`  
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Include schema validation, contract validation, and runtime unit tests as implementation begins.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Constitution v1.1.0 obligations (Principles V and VII) are enforced through Phase 2 foundational tasks.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the Python runtime, validation tooling, repo-level conventions, and governance scaffolding required by the constitution.

- [X] T001 Create Python project metadata and dependencies in pyproject.toml
- [X] T002 Create runtime package skeleton under apps/voice-gateway, apps/router, and apps/workers
- [X] T003 [P] Add test layout scaffolding under tests/unit, tests/integration, and tests/contract
- [X] T004 [P] Add developer guidance in README.md and docs/architecture/system-overview.md
- [X] T005 [P] Add PR template with constitution compliance checklist in .github/pull_request_template.md (covers all seven principles and links to .specify/memory/constitution.md)
- [X] T006 [P] Add exception log scaffolding in policies/exceptions/README.md defining the dated-entry format, rationale, scope, and review-date fields

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the shared schema, registry, policy, audit, and agent-authorization foundations before user story work. Principle V (policy-gated execution) and Principle VII (AI agent authorization) are enforced here.

- [X] T007 Implement schema loading and validation helpers in apps/router/schema_loader.py
- [X] T008 Define command registry entry JSON schema in schemas/command-registry.schema.json, including id, description, trigger phrases, input schema, allowed parameters, executor type, risk level, confirmation policy, audit requirements, output contract, and allowed_agent_scopes field (Principle VII)
- [X] T009 Define policy rule JSON schema in schemas/policy-rule.schema.json, covering risk thresholds, confirmation requirements, parameter allowlists, and agent-scope constraints
- [X] T010 Define audit record JSON schema in schemas/audit-entry.schema.json, requiring actor, intent, approved command, target, outcome, and repo revision fields (Principle V)
- [X] T011 Implement command registry loader in apps/router/command_registry.py
- [X] T012 Implement policy evaluation engine in apps/router/policy_engine.py that enforces risk, confirmation, parameter allowlists, and agent-scope gates uniformly for human and agent actors
- [X] T013 Implement audit writer in apps/workers/audit_logger.py emitting records that validate against schemas/audit-entry.schema.json
- [X] T014 Implement note template loader in apps/router/template_loader.py
- [X] T015 [P] Create starter command registry entries in registry/ covering at least one low-risk and one medium-risk command, each with complete typed metadata
- [X] T016 [P] Create starter policy rules in policies/ that cover the starter registry entries
- [X] T017 [P] Add contract fixture tests for registry and policy files in tests/contract/test_registry_contracts.py
- [X] T018 [P] Add JSON schema parsing tests for registry, policy, and audit schemas in tests/contract/test_schema_files.py

**Checkpoint**: The runtime can load repo-native definitions, reject invalid inputs, and enforce agent-scope gates through policy evaluation.

---

## Phase 3: User Story 1 - Govern the System from One Repo (Priority: P1) 🎯 MVP

**Goal**: Make the repository itself a coherent, inspectable control plane.

**Independent Test**: A collaborator can inspect repo files and validate that commands, policies, schemas, workflows, and knowledge templates are all present and cross-linked.

- [X] T019 [P] [US1] Add repo structure validation script in apps/router/repo_lint.py
- [X] T020 [US1] Add CLI entrypoint for repo validation in apps/router/cli.py (depends on T019)
- [X] T021 [US1] Add integration test for repo validation walkthrough in tests/integration/test_repo_backbone.py
- [X] T022 [US1] Add dedicated CI validation workflow in .github/workflows/validate-repo.yml that runs repo_lint, schema validation, and contract tests on every PR

**Checkpoint**: The repo backbone is inspectable and mechanically validated on every PR.

---

## Phase 4: User Story 2 - Capture Speech into Structured Knowledge (Priority: P1)

**Goal**: Transform capture-mode voice input into structured Markdown notes.

**Independent Test**: A sample voice envelope becomes an inbox or daily note with valid frontmatter and provenance.

- [X] T023 [P] [US2] Add capture request fixture in tests/fixtures/capture_request.json
- [X] T024 [P] [US2] Add unit tests for note rendering in tests/unit/test_note_writer.py
- [X] T025 [US2] Implement note writing service in apps/router/note_writer.py (depends on T014)
- [X] T026 [US2] Implement capture target resolution in apps/router/capture_router.py (depends on T025)
- [X] T027 [US2] Implement daily note append behavior in apps/router/daily_writer.py (depends on T025)
- [X] T028 [US2] Add integration test for capture mode in tests/integration/test_capture_mode.py

**Checkpoint**: Capture mode can create and update Markdown knowledge safely.

---

## Phase 5: User Story 3 - Trigger Governed Commands from Voice (Priority: P2)

**Goal**: Resolve approved commands and dispatch only validated requests.

**Independent Test**: A transcript maps to a command id, passes validation and policy, and yields a normalized execution result.

- [X] T029 [P] [US3] Add command resolution fixtures in tests/fixtures/command_requests.json
- [X] T030 [P] [US3] Add unit tests for registry matching and policy decisions in tests/unit/test_command_routing.py
- [X] T031 [US3] Implement transcript-to-command resolver in apps/router/intent_resolver.py (depends on T011)
- [X] T032 [US3] Implement execution dispatcher in apps/workers/execution_dispatcher.py that receives a session actor type (human or agent scope) and passes it to the policy engine (depends on T012, T013)
- [X] T033 [US3] Implement GitHub Actions adapter in apps/workers/github_actions_adapter.py
- [X] T034 [US3] Add integration test for command mode in tests/integration/test_command_mode.py
- [X] T035 [US3] Add integration test in tests/integration/test_agent_scope_enforcement.py verifying that an AI-agent actor is blocked from invoking commands whose allowed_agent_scopes do not include it, even when all other gates pass (Principle VII)

**Checkpoint**: Command mode is deterministic, typed, policy-gated, and agent-aware.

---

## Phase 6: User Story 4 - Combine Capture and Action in One Utterance (Priority: P2)

**Goal**: Support a single utterance that writes knowledge and triggers a related flow.

**Independent Test**: A combined-mode request produces a note result and a linked command audit record using the same correlation id.

- [X] T036 [P] [US4] Add combined-mode fixtures in tests/fixtures/combined_requests.json
- [X] T037 [P] [US4] Add unit tests for correlation handling in tests/unit/test_combined_mode.py
- [X] T038 [US4] Implement combined-mode coordinator in apps/voice-gateway/combined_mode.py (depends on T026, T032)
- [X] T039 [US4] Implement note-to-audit linking helpers in apps/workers/correlation.py (depends on T013)
- [X] T040 [US4] Add integration test for combined mode in tests/integration/test_combined_mode.py asserting that a policy-denied command still persists the note write with a linked audit decision

**Checkpoint**: Combined mode preserves knowledge updates even when command execution is denied or fails.

---

## Phase 7: User Story 5 - Connect External Services Through Repo Contracts (Priority: P3)

**Goal**: Integrate optional services without moving source-of-truth definitions out of the repo.

**Independent Test**: n8n, GitHub Actions, and Clawbot integrations can be understood and validated from repo contracts.

- [X] T041 [P] [US5] Add contract validation tests for integrations in tests/contract/test_integration_contracts.py
- [X] T042 [US5] Implement n8n webhook adapter in apps/workers/n8n_adapter.py
- [X] T043 [US5] Implement Clawbot adapter in apps/workers/clawbot_adapter.py
- [X] T044 [US5] Implement external-asset index updater in apps/workers/asset_indexer.py (initial backend: Google Drive)
- [X] T045 [US5] Add integration test for asset indexing in tests/integration/test_asset_sync.py

**Checkpoint**: Optional integrations remain bounded by repo-defined contracts.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improve observability, hardening, and operating guidance across all stories.

- [X] T046 [P] Documentation updates in docs/ and README.md
- [X] T047 Add audit retention and redaction tests in tests/unit/test_audit_policy.py
- [X] T048 Add performance smoke tests for routing in tests/integration/test_routing_latency.py
- [X] T049 Add runbook guidance in knowledge/references/operations-runbook.md
- [X] T050 Run quickstart validation from specs/001-voice-kms-automation/quickstart.md

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories.
- **User Story 1 (Phase 3)** and **User Story 2 (Phase 4)**: Can begin after Phase 2.
- **User Story 3 (Phase 5)**: Depends on registry, policy, audit, and agent-scope foundations (Phase 2).
- **User Story 4 (Phase 6)**: Depends on User Story 2 and User Story 3.
- **User Story 5 (Phase 7)**: Depends on User Story 3.
- **Polish (Phase 8)**: Follows whichever user stories are in scope for the increment.

### Within-Story Dependencies

- T008–T010 (schemas) block T011–T013 (loaders and engines).
- T011–T013 block T015–T016 (starter content can only validate once loaders and schemas exist).
- T014 (template loader) blocks T025 (note writer).
- T025 blocks T026 and T027.
- T011 and T012 block T031 and T032.
- T026 and T032 block T038 (combined mode coordinator).
- T013 blocks T039 (correlation helpers write audit).

## Implementation Strategy

1. Deliver the repo backbone, governance scaffolding (PR template, exception log), and validation flow first.
2. Land schemas, loaders, policy engine with agent-scope enforcement, and starter content.
3. Add capture mode to prove the Markdown-first KMS path.
4. Add governed command routing and agent-scope integration tests.
5. Add combined mode after capture and command mode are stable.
6. Add optional integrations behind adapters and contracts.
