# Feature Specification: Telegram Note Input with Google Drive Landing Zone

**Feature Branch**: `002-telegram-note-input-drive-landing`  
**Created**: 2026-04-09  
**Status**: Draft  
**Input**: User description: "Add a Telegram voice-note input flow where a dedicated bot sends webhook updates to the backend gateway, the gateway downloads audio, transcribes it, transforms it into structured Markdown, uploads Markdown and optional raw audio to Google Drive as the landing zone, writes repo-native landing records and manifests, and prepares future sync into the Git-based KMS."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Capture a Telegram Voice Note into Landing Artifacts (Priority: P1)

As the repository owner, I want a Telegram voice note to become a Drive-backed
landing document plus repo-native tracking records so I can capture notes from
mobile with minimal friction without losing Git-based visibility.

**Why this priority**: This is the first usable vertical slice. Without it,
there is no real input channel from Telegram into the KMS.

**Independent Test**: A fixture Telegram voice update can be sent to the
webhook, the system downloads the file, transcribes it, uploads Markdown to
Google Drive, optionally uploads the audio file, and writes linked repo-native
landing records with stable identifiers.

**Acceptance Scenarios**:

1. **Given** a valid Telegram voice-message update for the dedicated note bot,
   **When** the webhook pipeline completes successfully, **Then** the system
   uploads a Markdown landing document to the configured Google Drive folder and
   writes linked repo-native landing artifacts for that note.
2. **Given** a Telegram update that does not contain a supported voice or audio
   message, **When** the webhook receives it, **Then** the system rejects or
   ignores it safely without creating misleading landing records.

---

### User Story 2 - Preserve Traceability Through Partial Failures and Retries (Priority: P2)

As the repository owner, I want the intake flow to remain recoverable when one
step fails so I can reconcile Drive uploads, repo manifests, and Telegram
retries without losing track of what happened.

**Why this priority**: Real integrations fail in partial ways. If the flow
cannot represent partial success, the landing zone becomes operationally unsafe.

**Independent Test**: A simulated run where Google Drive upload succeeds but
repo manifest writing fails returns a recoverable partial-success result with
Drive references and retry metadata, and a repeated Telegram delivery does not
create duplicate records.

**Acceptance Scenarios**:

1. **Given** a note whose Drive upload succeeds but repo artifact writing fails,
   **When** processing completes, **Then** the system returns a recoverable
   partial-success state with enough metadata to reconcile the note later.
2. **Given** the same Telegram update is delivered again, **When** the gateway
   processes it, **Then** the system resolves it idempotently instead of
   creating duplicate landing records.

---

### User Story 3 - Prepare Drive-Backed Notes for Later KMS Normalization (Priority: P3)

As the repository owner, I want every landed Telegram note to carry an explicit
sync contract so future scripts can import Drive Markdown into the normalized
Git-based KMS without reverse-engineering hidden runtime behavior.

**Why this priority**: The landing flow only stays consistent with the
Everything-as-Code model if future normalization is already defined through
repo-native contracts and state.

**Independent Test**: A sync-oriented module can enumerate pending Telegram
landing manifests, inspect Drive references and sync status, and determine which
records are ready for import into the long-term KMS.

**Acceptance Scenarios**:

1. **Given** a landed Telegram note, **When** an operator inspects the repo,
   **Then** they can find a machine-readable manifest and a human-readable
   landing record that reference the Drive Markdown file and current sync state.
2. **Given** a future sync script reads pending manifests, **When** it evaluates
   a Telegram landing record, **Then** it has the identifiers, timestamps, Drive
   references, and state transitions needed to import that note deterministically.

### Edge Cases

- Telegram retries the same update after a timeout or transient failure.
- Telegram sends a message type other than voice or audio.
- Telegram file metadata resolves successfully but the file download fails.
- Audio transcription fails after the file has been downloaded.
- Markdown upload to Google Drive succeeds but raw audio upload fails.
- Google Drive upload succeeds but repo-native artifact writing fails.
- Google OAuth access token is expired and must be refreshed.
- A Drive-backed landing note is imported later into the normalized KMS and
  must not be imported twice.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a repo-defined Telegram webhook intake endpoint
  in the backend gateway for the dedicated note-input bot.
- **FR-002**: System MUST normalize supported Telegram voice or audio updates
  into a typed intake envelope that preserves Telegram message metadata,
  timestamps, and stable identifiers for downstream processing.
- **FR-003**: System MUST retrieve Telegram file metadata and download the
  corresponding audio bytes through a Telegram adapter rather than embedding
  Telegram API calls directly in the webhook handler.
- **FR-004**: System MUST transcribe downloaded audio through a transcription
  adapter interface, and the first implementation MUST support OpenAI
  speech-to-text.
- **FR-005**: System MUST transform the transcript into a structured Markdown
  landing document that contains typed frontmatter plus body sections for raw
  transcript content and cleaned note content.
- **FR-006**: System MUST upload the Markdown landing document to a configured
  Google Drive landing folder using an OAuth user-token flow.
- **FR-007**: System SHOULD support uploading the raw audio file to a configured
  Google Drive folder and MUST preserve whether that upload was skipped,
  succeeded, or failed.
- **FR-008**: System MUST write a repo-native human-readable landing record for
  each successfully accepted Telegram note so the repository remains the durable
  control plane even when the landing Markdown resides in Google Drive.
- **FR-008a**: System MUST validate repo-native Telegram landing records against
  a dedicated landing-note schema rather than reusing the normalized KMS note
  schema intended for inbox, daily, topic, and other long-term knowledge notes.
- **FR-009**: System MUST write a machine-readable landing manifest for each
  accepted Telegram note that records note identity, Telegram metadata, Drive
  file references, processing status, sync status, and reconciliation metadata.
- **FR-010**: System MUST support partial-success outcomes when one external or
  repo-native write succeeds and a later step fails, and MUST preserve enough
  state to reconcile the note without re-ingesting it blindly.
- **FR-011**: System MUST support idempotent repeated ingestion keyed by stable
  Telegram and landing-note identifiers so retries do not create duplicate
  records.
- **FR-012**: System MUST define a repo-native contract and scaffolded module for
  future sync of Drive landing Markdown into normalized KMS locations.
- **FR-013**: System MUST keep the Telegram input flow separate from command and
  search routing concerns, except for small shared abstractions that are already
  repo-native.
- **FR-014**: System MUST keep all config surfaces, schemas, prompts,
  integration contracts, and failure-mode expectations for this flow versioned
  in the repository.
- **FR-015**: System MUST extend existing repo boundaries under `apps/`,
  `integrations/`, `schemas/`, `knowledge/`, and `tests/` rather than
  introducing a parallel top-level runtime or KMS structure.

### Key Entities *(include if feature involves data)*

- **TelegramIntakeEnvelope**: Normalized representation of a Telegram update,
  selected message, bot-facing metadata, file identifiers, and processing
  correlation fields.
- **DriveLandingDocument**: Markdown document generated from a transcript and
  uploaded to Google Drive as the first landing artifact.
- **RepoLandingRecord**: Human-readable Markdown record stored in the repo that
  links a Telegram intake event to the Drive landing document and current sync
  state, validated against a dedicated landing-note schema for ingress records.
- **LandingManifest**: Machine-readable repo artifact that stores identifiers,
  Telegram metadata, Drive references, processing state, sync state, and retry
  or reconciliation metadata.
- **DriveUploadReference**: Typed reference to a Google Drive file or folder,
  including file IDs, URLs, names, MIME metadata, and upload timestamps.
- **SyncState**: The status model that indicates whether a landed Telegram note
  is pending import, imported, skipped, failed, or requires reconciliation.

## Constitution Alignment *(mandatory)*

- The repository remains the durable control plane: Telegram, OpenAI, and
  Google Drive behavior will be represented through repo-native contracts,
  schemas, config examples, manifests, and sync scaffolding.
- The feature stays reviewable through Git because webhook behavior, manifest
  structure, Markdown transformation rules, and failure handling will be
  implemented as versioned files and tests rather than hidden external logic.
- The feature remains consistent with Markdown-first knowledge handling because
  Google Drive Markdown is treated only as an ingress-stage landing artifact;
  repo-native landing records, manifests, and future normalized knowledge remain
  authoritative in the repository.
- This feature does not introduce command execution, command registry changes,
  or new policy-gated automation paths. It is limited to input-channel
  ingestion, storage, and reconciliation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A fixture-based end-to-end test can verify Telegram webhook intake
  through Drive Markdown upload and repo manifest creation without requiring
  manual intervention.
- **SC-002**: Every accepted Telegram note produces a stable note identifier, a
  Drive Markdown reference, and a repo-native landing manifest with sync state.
- **SC-003**: A partial-failure test can verify that Drive-success and
  repo-write-failure scenarios return recoverable reconciliation data instead of
  silent data loss.
- **SC-004**: A sync-scaffold test can enumerate pending Telegram landing
  manifests and determine import readiness deterministically from repo-native
  state alone.

## Assumptions

- This is a personal-project flow that targets a single dedicated Telegram bot
  and a single Google Drive account owned by the repository operator.
- Google Drive authentication for the first release uses OAuth user tokens
  rather than a service account, and token/config examples remain documented in
  the repository.
- The first release targets one configured Google Drive folder for Markdown
  landing documents and an optional second configured folder for raw audio.
- Telegram landing records use a dedicated landing-note schema instead of the
  existing normalized KMS note schema because ingress records carry different
  metadata and lifecycle states from long-term curated notes.
- The first release implements a practical vertical slice with a real FastAPI
  webhook path, a real Google Drive API integration, and an OpenAI-backed
  transcription adapter, while leaving broader command/search concerns out of
  scope.
