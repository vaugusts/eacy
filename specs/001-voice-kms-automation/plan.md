# Implementation Plan: Everything-as-Code Voice-Driven Knowledge Backbone

**Branch**: `001-voice-kms-automation` | **Date**: 2026-04-09 | **Spec**: [spec.md](/Users/leo/Sources/Personal/eacy/specs/001-voice-kms-automation/spec.md)
**Input**: Feature specification from `/specs/001-voice-kms-automation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Create a repository-native backbone for voice-driven knowledge capture and
governed automation. The first increment delivers the knowledge structure,
schemas, command registry, policy definitions, starter workflow contracts,
architecture docs, and spec-driven scaffolding needed to implement the runtime
in small, auditable steps.

## Technical Context

**Language/Version**: Python 3.12 for runtime tooling, Markdown/YAML/JSON for durable definitions  
**Primary Dependencies**: Pydantic v2, PyYAML, jsonschema, Typer, FastAPI, pytest  
**Storage**: Git repository filesystem for Markdown and contracts, JSONL audit logs, Google Drive for binary assets  
**Testing**: pytest, schema validation tests, contract snapshot tests, GitHub Actions validation runs  
**Target Platform**: macOS and Linux local-first runtime plus GitHub Actions runners  
**Project Type**: single-repo platform with docs, configuration, workflow definitions, and Python-based runtime tooling  
**Performance Goals**: capture-to-note transformation under 10 seconds excluding transcription; command routing decisions under 2 seconds for registry-backed commands  
**Constraints**: no unrestricted shell execution, command registry required for all executable actions, medium/high-risk confirmation support, repo-native auditability  
**Scale/Scope**: personal or small-team knowledge base with 10k+ notes, thousands of indexed assets, and dozens of governed commands and workflows

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution v1.1.0.

- **I. Repository-Native Backbone**: PASS. Core durable assets are represented
  as Markdown, YAML, JSON Schema, workflow definitions, and spec artifacts in
  the repo. External file stores (initially Google Drive) are limited to
  non-Markdown binary assets and indexed from the repo.
- **II. Git-First Change Control**: PASS. All proposed changes are versioned
  in repository files and structured for PR-based review.
- **III. Markdown-First Curated Knowledge**: PASS. The design separates inbox
  capture, daily notes, topic notes, decision notes, references, and asset
  indexes, with raw captures distinguished from curated outputs.
- **IV. Governed Voice-to-Action**: PASS. Every voice request is transcribed,
  parsed into a structured command envelope, resolved against the command
  registry, and validated against policy before any executor runs. Free-form
  voice-to-shell execution is rejected by construction.
- **V. Policy-Gated Execution and Audit**: PASS. Command and policy starter
  files declare risk level, confirmation requirements, executor type, allowed
  parameters, and output contract. Audit records emit actor, intent, approved
  command, target, outcome, and repo revision. This applies to both
  human-initiated and AI agent-initiated actions (see Principle VII).
- **VI. Spec-Driven Incremental Evolution**: PASS. Constitution, spec, plan,
  tasks, research, contracts, and quickstart artifacts are part of the initial
  delivery. Scope is held to one spec cycle per PR.
- **VII. AI Agent Authorization and Oversight**: PASS. The command registry
  schema carries an allowed-agent-scopes field; the policy engine enforces it
  on every invocation so AI agents route through the same gates as human
  actors. Agents cannot modify the registry, policy definitions, or this
  constitution without a human-approved pull request (enforced via the PR
  template compliance checklist at `.github/pull_request_template.md`).

**Exceptions**: None required for this feature. Any exception raised during
implementation MUST be recorded in `policies/exceptions/` per the Governance
section of the constitution.

## Project Structure

### Documentation (this feature)

```text
specs/001-voice-kms-automation/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
├── checklists/
└── tasks.md
```

### Source Code (repository root)

```text
apps/
├── router/
├── voice-gateway/
└── workers/

automation/
└── workflows/

docs/
├── architecture/
└── pseudocode/

deploy/

integrations/
├── n8n/
└── openclaw/

knowledge/
├── assets/
├── daily/
├── decisions/
├── entities/
├── inbox/
├── projects/
├── references/
├── sources/
├── topics/
└── weekly/

policies/
prompts/
registry/
schemas/
templates/
└── notes/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Use a documentation-and-contracts-first monorepo with
planned Python runtime directories under `apps/`. Knowledge, governance,
integrations, and workflow contracts remain top-level so they stay visible and
easy for humans and coding agents to discover.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
