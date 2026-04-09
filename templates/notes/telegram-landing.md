---
schema_version: "1.0.0"
note_type: telegram_landing
status: landed
landing_id: "{{landing_id}}"
source_provider: telegram
source_update_id: {{update_id}}
source_message_id: {{message_id}}
drive_markdown_file_id: "{{drive_markdown_file_id}}"
drive_audio_file_id: "{{drive_audio_file_id}}"
created_at: "{{timestamp}}"
updated_at: "{{timestamp}}"
tags:
  - telegram
  - landing
  - voice-capture
---

## Transcript

{{transcript}}

## Source Metadata

- Envelope: {{envelope_id}}
- Telegram file id: {{telegram_file_id}}
- Mime type: {{mime_type}}

## Landing Targets

- Drive markdown: {{drive_markdown_url}}
- Drive audio: {{drive_audio_url}}

## Sync Hints

- Import state: {{import_state}}
- Block reason: {{block_reason}}
