# Data Model

## Core Entities

### TelegramIntakeEnvelope

| Field | Type | Notes |
|-------|------|-------|
| `intake_id` | string | Stable identifier for this intake attempt and its downstream artifacts |
| `correlation_id` | string | Shared correlation identifier across webhook, manifest, and landing record |
| `telegram_update_id` | integer | Telegram update identifier for retry detection |
| `telegram_chat_id` | integer | Source chat identifier |
| `telegram_message_id` | integer | Source message identifier |
| `message_type` | enum | `voice` or `audio` |
| `telegram_file_id` | string | Telegram file reference used for download |
| `telegram_file_unique_id` | string | Stable provider-side file uniqueness hint |
| `received_at` | datetime | Gateway receipt time |
| `sent_at` | datetime | Telegram message timestamp |
| `language_hint` | string | Optional Telegram or operator-supplied hint |
| `actor_label` | string | Human-readable source label for manifests and records |
| `processing_status` | enum | `received`, `downloaded`, `transcribed`, `uploaded_markdown`, `landed`, `partial`, `failed`, `reconciled` |
| `retry_key` | string | Deterministic key for idempotent duplicate detection |

### TranscriptionResult

| Field | Type | Notes |
|-------|------|-------|
| `transcription_id` | string | Stable identifier for this transcription attempt |
| `intake_id` | string | Parent `TelegramIntakeEnvelope` id |
| `provider` | string | Initial value `openai` |
| `model` | string | Speech-to-text model identifier |
| `language` | string | Detected or provided language |
| `transcript_text` | string | Raw transcript text returned by the adapter |
| `completed_at` | datetime | Completion time |
| `duration_seconds` | number | Audio duration when available |
| `raw_response_ref` | string | Optional pointer to stored diagnostic data or response metadata |

### DriveUploadReference

| Field | Type | Notes |
|-------|------|-------|
| `storage_system` | enum | Initial value `google_drive` |
| `file_id` | string | Google Drive file identifier |
| `folder_id` | string | Parent folder identifier |
| `name` | string | Uploaded file name |
| `mime_type` | string | Google Drive MIME metadata |
| `web_view_url` | string | Human-facing Drive URL |
| `download_url` | string | Optional downloadable URL when available |
| `uploaded_at` | datetime | Upload completion time |
| `checksum` | string | Optional digest for duplicate or integrity checks |

### DriveLandingDocument

| Field | Type | Notes |
|-------|------|-------|
| `note_id` | string | Stable landing note identifier |
| `intake_id` | string | Parent intake identifier |
| `title` | string | Rendered note title |
| `markdown_text` | string | Generated Markdown content uploaded to Drive |
| `drive_ref` | `DriveUploadReference` | Required Markdown upload reference |
| `audio_ref` | `DriveUploadReference` or null | Optional raw-audio upload reference |
| `uploaded_at` | datetime | Time the landing document became available in Drive |

### RepoLandingRecord

| Field | Type | Notes |
|-------|------|-------|
| `record_path` | string | Repository-relative Markdown path under `knowledge/sources/telegram/` |
| `note_id` | string | Stable landing note identifier |
| `title` | string | Human-readable landing title |
| `status` | enum | `received`, `landed`, `partial`, `reconciled`, `imported`, `failed` |
| `created_at` | datetime | Creation time |
| `updated_at` | datetime | Last update time |
| `manifest_ref` | string | Repository-relative path to the machine-readable manifest |
| `drive_markdown_ref` | `DriveUploadReference` | Required Markdown landing reference |
| `drive_audio_ref` | `DriveUploadReference` or null | Optional audio landing reference |
| `telegram_source_ref` | string | Human-readable Telegram source reference |

### LandingManifest

| Field | Type | Notes |
|-------|------|-------|
| `manifest_path` | string | Repository-relative JSON path under `knowledge/manifests/telegram/` |
| `note_id` | string | Stable landing note identifier |
| `intake_id` | string | Parent intake identifier |
| `correlation_id` | string | Shared correlation identifier |
| `telegram_update_id` | integer | Telegram update identifier |
| `telegram_message_id` | integer | Telegram message identifier |
| `telegram_file_unique_id` | string | Provider uniqueness hint |
| `processing_status` | enum | `received`, `downloaded`, `transcribed`, `uploaded_markdown`, `landed`, `partial`, `failed`, `reconciled` |
| `sync_state` | enum | `pending_import`, `imported`, `skipped`, `failed`, `requires_reconciliation` |
| `drive_markdown_ref` | `DriveUploadReference` | Required Markdown landing reference |
| `drive_audio_ref` | `DriveUploadReference` or null | Optional audio reference |
| `landing_record_path` | string | Markdown landing-record path |
| `error_context` | object | Typed recovery information for partial or failed runs |
| `retry_count` | integer | Number of retry attempts |
| `last_attempted_at` | datetime | Last processing attempt timestamp |

### SyncCandidate

| Field | Type | Notes |
|-------|------|-------|
| `note_id` | string | Stable landing note identifier |
| `manifest_path` | string | Source manifest path |
| `drive_markdown_ref` | `DriveUploadReference` | Drive Markdown to import |
| `sync_state` | enum | Current import state |
| `ready_for_import` | boolean | Whether the record is importable now |
| `blocker_reason` | string | Human-readable explanation when not importable |
| `target_kms_path` | string | Planned normalized destination when known |

## Relationships

- A `TelegramIntakeEnvelope` produces zero or one `TranscriptionResult`.
- A `TelegramIntakeEnvelope` may produce one `DriveLandingDocument`.
- A `DriveLandingDocument` is represented in the repo by one
  `RepoLandingRecord` and one `LandingManifest`.
- A `LandingManifest` holds the authoritative processing and sync state for a
  `RepoLandingRecord`.
- A `LandingManifest` may later become one `SyncCandidate` for normalized KMS
  import.

## Validation Rules

- `intake_id`, `correlation_id`, and `note_id` must be stable across retries for
  the same Telegram update.
- `telegram_update_id` and `telegram_message_id` must be preserved exactly as
  received from Telegram for duplicate detection and auditability.
- `drive_markdown_ref` is required for any manifest or landing record in
  `landed`, `partial`, `reconciled`, or `imported` state.
- `drive_audio_ref` is optional and may be null when audio upload is disabled or
  skipped.
- `RepoLandingRecord` must validate against a dedicated landing-note schema, not
  `schemas/note.schema.json`.
- `LandingManifest` must validate against a dedicated manifest schema and must
  always include both `processing_status` and `sync_state`.

## State Transitions

### Processing Status

- `received -> downloaded -> transcribed -> uploaded_markdown -> landed`
- `received -> failed`
- `downloaded -> failed`
- `transcribed -> failed`
- `uploaded_markdown -> partial`
- `partial -> reconciled`
- `failed -> reconciled` when recovery fills missing durable state

### Sync State

- `pending_import -> imported`
- `pending_import -> skipped`
- `pending_import -> failed`
- `pending_import -> requires_reconciliation`
- `failed -> pending_import` after a successful retry
- `requires_reconciliation -> pending_import` after recovery
