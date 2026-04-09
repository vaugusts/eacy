<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- Modified principles:
  - I. Repository-Native Backbone (linked exception clause to Governance process)
  - IV. Governed Voice-to-Action (clarified normalization pipeline)
  - V. Policy-Gated Execution and Audit (extended to AI agent-initiated actions)
  - VI. Spec-Driven Incremental Evolution (added scope heuristic)
  - Added principle -> VII. AI Agent Authorization and Oversight
- Modified sections:
  - System Boundaries (removed Google Drive specificity; generalized to external file stores)
  - Governance (added conflict resolution, exception approval process, compliance enforcement mechanism)
- Templates requiring updates:
  - ✅ synced /Users/leo/Sources/Personal/eacy/.specify/templates/spec-template.md
  - ✅ synced /Users/leo/Sources/Personal/eacy/.specify/templates/plan-template.md
  - ✅ synced /Users/leo/Sources/Personal/eacy/.specify/templates/tasks-template.md
- Follow-up TODOs:
  - Create .github/pull_request_template.md with constitution compliance checklist
  - Create policies/exceptions/ directory and log
-->
# EACY Constitution

## Core Principles

### I. Repository-Native Backbone
All durable system behavior MUST be represented in this repository: knowledge
structures, schemas, prompts, workflow definitions, command registry entries,
policies, integration contracts, deployment assets, and tests. External
services MAY execute or store data, but their contracts, mappings, and
configuration surfaces MUST remain versioned here. Hidden manual configuration
is a defect unless documented as an approved exception under the exception
process defined in Governance.

### II. Git-First Change Control
GitHub is the operational source of truth for system evolution. Every change to
knowledge structure, execution policy, automation definition, or integration
contract MUST be reviewable, reversible, and traceable to commits, branches,
and pull requests. Runtime behavior that cannot be reconstructed from the repo
and audit records MUST be treated as non-compliant.

### III. Markdown-First Curated Knowledge
Human-readable knowledge MUST live primarily as Markdown with consistent
frontmatter, relationship links, and provenance. The system MUST distinguish raw
capture from curated knowledge, support inbox and temporal aggregation flows,
and preserve traceability back to source assets or transcripts. Raw transcripts
alone do not satisfy this principle.

### IV. Governed Voice-to-Action
Voice operation MUST explicitly support capture mode, command mode, and combined
mode. Speech MAY initiate automation only after it has been transcribed,
parsed into a structured command, resolved against the command registry, and
validated against policy. Free-form voice-to-shell execution is prohibited.

### V. Policy-Gated Execution and Audit
Every executable action MUST declare risk level, confirmation requirements,
allowed parameters, executor type, and output contract. Medium-risk and
high-risk actions MUST support confirmation before execution. All executions
MUST emit structured audit records that capture actor, intent, approved command,
target, outcome, and repo revision. This principle applies equally to
human-initiated and AI agent-initiated actions.

### VI. Spec-Driven Incremental Evolution
Meaningful changes MUST proceed through a spec-driven lifecycle: constitution
alignment, feature specification, implementation plan, tasks, implementation,
verification, and iteration. The repository MUST stay friendly to AI-assisted
development by keeping interfaces typed, artifacts explicit, and changes small
enough to review and extend incrementally. A single spec cycle per pull request
is the default scope heuristic.

### VII. AI Agent Authorization and Oversight

AI agents MUST operate under declared permission scopes and MUST NOT exceed the
authorization level of the human actor who initiated the session. Agents MAY
perform read operations and draft artifacts autonomously. Write and execution
operations MUST be validated against the policy layer with the same confirmation
requirements as human-initiated actions. Agents MUST NOT modify the command
registry, policy definitions, or this constitution without an explicit
human-approved pull request.

## System Boundaries

Core repo-native components include the Markdown knowledge base, schemas,
command registry, policy layer, prompt library, workflow definitions, tests,
documentation, and deployment assets. Runtime components such as the voice
gateway, command router, local workers, and GitHub Actions runners MAY execute
outside the repo, but their behavior MUST be defined by repo-native contracts.
External file stores are reserved for non-Markdown assets and binary content
that cannot practically be versioned here; the repo MUST retain indexes,
metadata, summaries, and references for those assets.

## Delivery Workflow and Quality Gates

Each feature MUST define user value, acceptance criteria, schemas or contracts
when interfaces change, and verification steps before implementation is claimed
complete. Changes that affect execution safety MUST update the command registry,
policy definitions, and audit expectations together. Cross-system integrations
MUST ship with documented contracts, failure modes, and local or CI validation
steps. Repo structure changes MUST preserve clear boundaries between knowledge,
automation, governance, integrations, and runtime code.

## Governance

This constitution supersedes conflicting local conventions. Amendments require a
documented pull request that explains rationale, migration impact, and template
or workflow changes needed to keep the repo coherent. Versioning follows
semantic intent: MAJOR for incompatible governance changes, MINOR for new
principles or materially expanded obligations, PATCH for clarifications without
behavioral change. Every implementation plan and code review MUST include an
explicit constitution compliance check using the checklist in
`.github/pull_request_template.md`.

When principles appear to conflict, the more restrictive obligation applies
until the conflict is resolved by amendment. Delivery urgency does not override
safety or audit obligations.

Exceptions to any principle require documented approval recorded as a dated
entry in `policies/exceptions/` with rationale, scope, and a scheduled review
date. Exceptions lapse if not renewed at their review date.

**Version**: 1.1.0 | **Ratified**: 2026-04-09 | **Last Amended**: 2026-04-09
