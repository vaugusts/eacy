# Research Notes

## Decision 1: Use the Repository as the System Control Plane

- **Decision**: Treat the repo as the durable control plane for knowledge,
  commands, policies, prompts, workflow definitions, and integration contracts.
- **Rationale**: This keeps evolution Git-first, reviewable, and extendable by
  AI coding agents.
- **Alternatives considered**:
  - SaaS-first workflow tooling: rejected because configuration drifts away from
    Git.
  - Database-first knowledge store: rejected because Markdown-first knowledge is
    a core principle.

## Decision 2: Keep Knowledge Markdown-First with Typed Frontmatter

- **Decision**: Store core knowledge as Markdown with JSON-schema-backed
  frontmatter conventions.
- **Rationale**: Markdown stays human-readable while schemas prevent structure
  drift.
- **Alternatives considered**:
  - Pure JSON documents: rejected because they are less ergonomic for curation.
  - Wiki-only storage: rejected because it weakens repo-native control.

## Decision 3: Normalize Voice Input Before Any Execution

- **Decision**: Introduce a typed `VoiceEnvelope` contract ahead of note or
  command handling.
- **Rationale**: This creates one safe entry point for capture, command, and
  combined modes.
- **Alternatives considered**:
  - Direct transcript-to-command matching: rejected because it weakens safety.
  - Separate gateways for each mode: rejected because it duplicates logic.

## Decision 4: Route Automation Through a Registry and Policy Layer

- **Decision**: Command execution is allowed only through registry definitions
  validated against policy and risk rules.
- **Rationale**: Deterministic execution is safer and easier to audit than
  agentic improvisation.
- **Alternatives considered**:
  - Free-form shell command agents: rejected as unsafe.
  - Executor-specific hardcoding: rejected because it does not scale.

## Decision 5: Use Adapter-Based Execution Backends

- **Decision**: Support local CLI, GitHub Actions, n8n, generic webhooks, and
  OpenClaw or Clawbot via typed adapters.
- **Rationale**: The repo stays authoritative while execution backends remain
  swappable.
- **Alternatives considered**:
  - GitHub Actions only: rejected because local-first use cases matter.
  - n8n only: rejected because it over-centralizes runtime in one tool.

## Decision 6: Keep Google Drive Narrow and Explicit

- **Decision**: Use Google Drive only for non-Markdown assets and shareable
  artifacts, with repo-side asset indexes and summaries.
- **Rationale**: This preserves a Markdown-first KMS while still supporting rich
  files and sharing workflows.
- **Alternatives considered**:
  - Store all documents in Drive: rejected because it fractures the knowledge
    backbone.
  - Store all binaries in git: rejected because it scales poorly.
