# Data Model

## Core Entities

### VoiceEnvelope

| Field | Type | Notes |
|-------|------|-------|
| `envelope_id` | string | Correlation-safe unique identifier |
| `mode` | enum | `capture`, `command`, or `combined` |
| `transcript` | string | Raw or normalized transcript text |
| `language` | string | BCP-47 style language tag |
| `captured_at` | datetime | Transcript capture time |
| `source_device` | string | Mic, mobile shortcut, browser, or webhook |
| `context` | object | Optional routing hints such as topic or project |
| `parameters` | object | Parsed structured command inputs |

### KnowledgeNote

| Field | Type | Notes |
|-------|------|-------|
| `note_path` | string | Repository-relative Markdown path |
| `note_type` | enum | Inbox, daily, topic, project, decision, reference, asset index |
| `title` | string | Human-readable note title |
| `status` | enum | `raw`, `curated`, `active`, `archived` |
| `tags` | array | Taxonomy and routing support |
| `source_refs` | array | Links to transcript, Drive asset, or other sources |
| `topic_refs` | array | Topic note relationships |
| `project_refs` | array | Project note relationships |
| `summary` | string | Optional curation summary |

### CommandDefinition

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Stable identifier |
| `trigger_phrases` | array | Supported speech phrases |
| `mode_support` | array | Usually `command` or `combined` |
| `input_schema_ref` | string | Reference to JSON Schema |
| `allowed_parameters` | array | Allowlisted runtime parameters |
| `executor` | object | Type, target, timeout, and environment |
| `risk_level` | enum | `low`, `medium`, `high`, or `blocked` |
| `confirmation_policy` | string | Rule name applied before execution |
| `output_contract` | object | Normalized response shape |

### PolicyRule

| Field | Type | Notes |
|-------|------|-------|
| `rule_id` | string | Stable identifier |
| `applies_to` | string | Command id, risk level, or executor type |
| `effect` | enum | `allow`, `confirm`, or `deny` |
| `conditions` | object | Optional environment or parameter constraints |
| `audit_requirements` | object | Required audit fields and retention |

### WorkflowDefinition

| Field | Type | Notes |
|-------|------|-------|
| `workflow_id` | string | Stable identifier |
| `trigger` | object | Event source such as command, schedule, or webhook |
| `steps` | array | Ordered execution steps |
| `inputs` | object | Required and optional inputs |
| `outputs` | object | Result and artifact references |
| `backends` | array | Compatible execution backends |

### AssetRecord

| Field | Type | Notes |
|-------|------|-------|
| `asset_id` | string | Stable id across repo references |
| `storage_system` | enum | `google_drive`, `local`, or future stores |
| `storage_ref` | string | URL or opaque asset locator |
| `asset_type` | enum | PDF, audio, image, slide deck, docx, other |
| `summary` | string | Human-readable summary |
| `linked_notes` | array | Related Markdown notes |
| `captured_from` | string | Original source context |

### AuditEntry

| Field | Type | Notes |
|-------|------|-------|
| `audit_id` | string | Stable event identifier |
| `occurred_at` | datetime | Event time |
| `actor` | string | User or system actor |
| `command_id` | string | Resolved command identifier |
| `decision` | enum | `allowed`, `confirmed`, `blocked`, `failed`, `succeeded` |
| `executor` | object | Backend type and target |
| `repo_ref` | string | Commit or branch reference |
| `correlation_id` | string | Links note writes and command execution |

## Relationships

- A `VoiceEnvelope` may create or update one or more `KnowledgeNote` records.
- A `VoiceEnvelope` may resolve to one `CommandDefinition`.
- A `CommandDefinition` is constrained by one or more `PolicyRule` entries.
- A `CommandDefinition` usually points to one `WorkflowDefinition`.
- A `KnowledgeNote` may reference zero or more `AssetRecord` entries.
- Every execution decision creates an `AuditEntry`.
