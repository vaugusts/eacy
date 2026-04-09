# Feature Specification: Everything-as-Code Voice-Driven Knowledge Backbone

**Feature Branch**: `001-voice-kms-automation`  
**Created**: 2026-04-09  
**Status**: Implemented  
**Input**: User description: "Build an Everything-as-Code Voice-Driven Knowledge & Automation System"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Govern the System from One Repo (Priority: P1)

As the repository owner, I want the core knowledge model, command registry,
policies, prompts, schemas, workflow definitions, templates, and deployment
assets to live in one repository so I can evolve the system through Git-based
review and AI-assisted change.

**Why this priority**: Without a coherent repo backbone, voice automation and
integrations become fragmented and unsafe.

**Independent Test**: A collaborator can inspect the repository and find
concrete files for knowledge structure, command definitions, execution policy,
schemas, and feature planning without relying on undocumented dashboards.

**Acceptance Scenarios**:

1. **Given** a fresh clone of the repo, **When** an engineer reviews the top
   level structure, **Then** they can identify where knowledge, automation,
   policies, schemas, integrations, and specs are defined.
2. **Given** a proposed behavior change, **When** it affects command execution
   or knowledge structure, **Then** the change can be expressed as repo file
   edits with traceable review history.

---

### User Story 2 - Capture Speech into Structured Knowledge (Priority: P1)

As a voice user, I want speech in capture mode to become structured Markdown in
the right inbox, daily, topic, project, or decision note so voice capture grows
the knowledge base without turning it into an uncurated transcript dump.

**Why this priority**: Capture is the lowest-friction path into the system and
must preserve long-term knowledge quality.

**Independent Test**: A sample voice envelope can be transformed into a note
that includes frontmatter, provenance, and links to topics or assets.

**Acceptance Scenarios**:

1. **Given** a transcript tagged for inbox capture, **When** the gateway
   processes it, **Then** a Markdown note is created in `knowledge/inbox/` with
   raw status and source metadata.
2. **Given** a transcript that targets a daily note, **When** it is processed,
   **Then** the system appends structured content to the matching daily note and
   records the source transcript reference.
3. **Given** a transcript that refers to an existing project or topic,
   **When** the router resolves capture context, **Then** the created note links
   back to the relevant project or topic note.

---

### User Story 3 - Trigger Governed Commands from Voice (Priority: P2)

As a voice user, I want command mode to resolve speech into approved commands so
I can trigger safe automation without unrestricted shell access.

**Why this priority**: Command execution is valuable only if it remains typed,
predictable, and auditable.

**Independent Test**: A voice intent can be matched to a registry entry,
validated against policy, and routed to an executor with a normalized output.

**Acceptance Scenarios**:

1. **Given** a transcript that matches a low-risk command phrase,
   **When** the router evaluates it, **Then** the system validates input and
   dispatches the declared executor without asking for free-form shell text.
2. **Given** a transcript that maps to a medium-risk or high-risk command,
   **When** policy evaluation runs, **Then** the system requires confirmation or
   blocks the request according to policy.
3. **Given** a transcript that does not map to an approved command,
   **When** command resolution fails, **Then** the request is rejected with a
   safe explanation and audit entry.

---

### User Story 4 - Combine Capture and Action in One Utterance (Priority: P2)

As a voice user, I want a single utterance to both update knowledge and trigger
an approved related flow so note-taking and automation stay connected.

**Why this priority**: Combined mode is a core differentiator and creates a
useful bridge between knowledge capture and operational workflows.

**Independent Test**: One voice envelope can create or update a note, then
trigger a linked digest or indexing command while preserving shared correlation
metadata.

**Acceptance Scenarios**:

1. **Given** a combined-mode utterance to capture a note and refresh a topic
   summary, **When** it is processed, **Then** the note change and command audit
   share a common correlation identifier.
2. **Given** a combined-mode utterance whose note write succeeds but command
   execution is denied by policy, **When** processing completes, **Then** the
   note remains saved and the failed command decision is linked back to it.

---

### User Story 5 - Connect External Services Through Repo Contracts (Priority: P3)

As the system integrator, I want Google Drive, NotebookLM, n8n, GitHub Actions,
and OpenClaw or Clawbot integrations to be represented through repo-native
contracts so optional services can be swapped or extended without losing
control.

**Why this priority**: Optional integrations add leverage, but only if the repo
remains authoritative.

**Independent Test**: An integrator can inspect versioned contracts and see how
an external system maps to commands, assets, or workflow inputs and outputs.

**Acceptance Scenarios**:

1. **Given** an external automation backend such as n8n, **When** it is used,
   **Then** the repo contains a contract that defines webhook shape, command
   mapping, and expected outputs.
2. **Given** a Google Drive asset, **When** it is referenced by the system,
   **Then** the repo retains metadata, summary, and links even though the binary
   stays in Drive.
3. **Given** a NotebookLM source pack workflow, **When** sources are assembled,
   **Then** the source selection and resulting references are represented in the
   repo.

### Edge Cases

- Ambiguous speech matches multiple command trigger phrases.
- A combined-mode request succeeds on note creation but fails policy evaluation
  for execution.
- A capture request references a project, topic, or asset that does not yet
  exist.
- A command references parameters outside the allowlisted schema.
- A Google Drive asset link becomes stale or permissions change.
- A backend executor returns partial success or an unstructured error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST store Markdown knowledge, schemas, templates, prompts,
  automation definitions, policies, and integration contracts in this
  repository.
- **FR-002**: System MUST distinguish core repo-native components from optional
  integrations and external storage services.
- **FR-003**: System MUST use Git and GitHub-friendly workflows as the primary
  change-management path.
- **FR-004**: System MUST support Markdown-first knowledge organization for
  inbox, daily, weekly, topics, projects, entities, decisions, references,
  source indexes, asset indexes, prompts, automation docs, and runbooks.
- **FR-005**: System MUST separate raw captured notes from curated knowledge.
- **FR-006**: System MUST support voice capture mode that writes structured
  Markdown content to the appropriate note destination.
- **FR-007**: System MUST support voice command mode that resolves speech into a
  predefined command registry entry.
- **FR-008**: System MUST support combined mode where one utterance updates
  knowledge and triggers a related approved flow.
- **FR-009**: System MUST normalize every voice request into a typed input
  envelope before further processing.
- **FR-010**: System MUST maintain a command registry where every executable
  command declares id, description, trigger phrases, input schema, allowed
  parameters, executor type, target workflow or script, risk level,
  confirmation policy, audit requirements, and output contract.
- **FR-011**: System MUST enforce policy before any command execution.
- **FR-012**: System MUST prevent arbitrary free-form command execution from
  voice input.
- **FR-013**: System MUST classify commands by risk and support confirmation for
  medium-risk and high-risk actions.
- **FR-014**: System MUST emit structured audit records for command evaluation
  and execution outcomes.
- **FR-015**: System MUST keep external file stores (initially Google Drive)
  limited to binary or shareable non-Markdown assets while retaining
  repo-native metadata and indexes for those assets.
- **FR-016**: System MUST represent automation backends such as GitHub Actions,
  n8n, local scripts, and OpenClaw or Clawbot through repo-defined contracts.
- **FR-017**: System MUST preserve traceability between notes, source assets,
  execution events, and summaries.
- **FR-018**: System MUST support topic and daily aggregation flows that
  transform captured material into curated knowledge outputs.
- **FR-019**: System MUST be extendable through spec-driven artifacts including
  constitution, specifications, plans, tasks, prompts, and review guidance.
- **FR-020**: System MUST support local-first or self-hostable runtime options
  where practical.
- **FR-021**: System MUST apply the same registry resolution, policy
  evaluation, and audit emission to AI agent-initiated actions as to
  human-initiated actions, and MUST prevent AI agents from modifying the
  command registry, policy definitions, or constitution without a
  human-approved pull request.

### Key Entities *(include if feature involves data)*

- **VoiceEnvelope**: Normalized representation of a transcript, mode,
  parameters, context, and provenance.
- **KnowledgeNote**: A Markdown note with typed frontmatter, links, tags,
  provenance, and curation state.
- **CommandDefinition**: A registry entry that defines a voice-triggerable
  action and the rules required to execute it safely.
- **PolicyRule**: A machine-readable rule that constrains execution based on
  risk, executor type, parameters, or environment.
- **WorkflowDefinition**: A repo-native workflow contract that maps a command to
  one or more execution steps and outputs.
- **AssetRecord**: Metadata and summary for a binary or shared external asset.
- **AuditEntry**: A structured execution or decision record tied to a command,
  actor, repo revision, and outcome.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new collaborator can identify the location of the knowledge
  model, command registry, policy definitions, schemas, and integration
  contracts within 10 minutes of cloning the repo.
- **SC-002**: Every executable command in the starter system includes complete
  typed metadata for risk, input validation, audit, and output shape.
- **SC-003**: A capture-mode voice request can be transformed into a valid
  Markdown note with frontmatter and provenance in under 10 seconds, excluding
  speech-to-text latency.
- **SC-004**: A command-mode request cannot reach an executor without passing
  registry resolution and policy evaluation.
- **SC-005**: Combined-mode operations preserve a shared correlation identifier
  across note output and execution audit.
- **SC-006**: External asset references remain searchable from the repository
  even when the binary payload resides in an external file store.
- **SC-007**: Every audit record emitted by the system contains actor, intent,
  approved command, target, outcome, and repo revision with no missing fields,
  verified by contract tests.

## Assumptions

- GitHub remains the canonical source of truth for version history and review.
- The first increment optimizes for repository structure, schemas, and starter
  contracts rather than a complete production voice client.
- Voice transcription may be supplied by a later local or hosted provider, but
  the normalized envelope contract remains repo-defined.
- An external file store (initially Google Drive) is available for binary
  assets, but Markdown knowledge remains in the repo.
- Safety and auditability are higher priority than unconstrained automation
  breadth.
