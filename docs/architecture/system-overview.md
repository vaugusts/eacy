# System Overview

## Recommended Architecture

The recommended architecture uses the repository as the control plane and
knowledge plane, while keeping runtime execution pluggable.

### 1. Repo-Native Control Plane

This layer stores the durable definitions:

- Markdown knowledge and indexes in `knowledge/`
- command registry in `registry/`
- execution policies in `policies/`
- JSON schemas in `schemas/`
- note and prompt templates in `templates/`
- workflow definitions in `automation/workflows/`
- integration contracts in `integrations/`
- spec-driven artifacts in `specs/` and `.specify/`

### 2. Runtime and Execution Plane

This layer reads repo-native definitions and performs work:

- `apps/voice-gateway/` receives transcript events
- `apps/router/` classifies mode and resolves commands
- `apps/workers/` hosts adapters for local CLI, GitHub Actions, n8n, or webhooks
- `.github/workflows/` executes approved automation in CI or on demand

### 3. Optional Integration Plane

Optional services are attached through contracts, not ad hoc wiring:

- Google Drive for non-Markdown assets and shareable artifacts
- NotebookLM for source-pack synthesis
- ChatGPT for transformation and reasoning tasks
- n8n for visual automation backends
- OpenClaw or Clawbot for tool or skill execution

### 4. External Storage and Collaboration Plane

This layer is intentionally narrow:

- Google Drive stores binary assets, PDFs, images, slides, recordings, and
  shareable documents
- GitHub stores history, code review, issues, pull requests, and Actions logs

## Data Flow

### Capture Mode

1. Voice transcript enters the gateway as a typed voice envelope.
2. The router classifies the request as `capture`.
3. A note template is selected.
4. Structured Markdown is written to the appropriate knowledge path.
5. Asset and provenance references are added.
6. An audit record is appended.

### Command Mode

1. Voice transcript enters the gateway as a typed voice envelope.
2. The router classifies the request as `command`.
3. The registry resolves trigger phrase to command definition.
4. Input is validated against schema and policy.
5. Confirmation is requested when policy requires it.
6. The execution adapter invokes the approved backend.
7. Output is normalized and logged.

### Combined Mode

1. The gateway normalizes a single utterance into note content and intent.
2. The note is written first with correlation metadata.
3. The command path is evaluated against registry and policy.
4. Execution outcome is linked back to the created or updated note, even when
   the command is denied or requires confirmation.

## Control Flow

Control always passes through four repo-defined checkpoints:

1. `voice envelope` normalization
2. `command registry` resolution
3. `policy` evaluation
4. `audit` emission

No runtime component is allowed to skip those checkpoints for executable
commands.

## Execution Model

Execution is adapter-based and deterministic:

- `local_cli`: approved local scripts with fixed argument mapping
- `github_action`: workflow dispatch or repository-local CI jobs
- `n8n_webhook`: versioned n8n entry points with repo contracts
- `webhook`: generic typed webhook adapter
- `clawbot_tool`: OpenClaw or Clawbot tool invocation

Each command definition declares its executor type, allowed parameters, risk
level, confirmation policy, and output contract. The adapter layer never
receives untyped free-form shell text from users.

The runtime currently normalizes three adapter styles:

- `github_action` for repo-local workflows under `.github/workflows/`
- `n8n_webhook` for optional webhook-backed automation that may return accepted
  asynchronous runs
- `clawbot_tool` for governed tool contracts such as the OpenClaw router

## Why This Fits an Everything-as-Code Repo

This design keeps the repository as the backbone because the durable system is
expressed as files, not dashboards. Knowledge stays Markdown-first, automation
stays declarative, external integrations stay contract-driven, and AI coding
agents have explicit artifacts to modify safely over time. The runtime can grow
from local scripts to GitHub Actions or n8n without moving the system's source
of truth away from Git.

## Assumptions

- Python is the most practical implementation language for the initial runtime.
- GitHub remains the canonical VCS and automation entry point.
- Google Drive is a supporting asset store, not the primary knowledge system.
- Voice transcription may come from a local model or hosted provider later, but
  the repo owns the normalized contract.
