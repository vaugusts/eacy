---
schema_version: "1.0.0"
note_type: asset_index
title: "Asset Index"
status: curated
created_at: "2026-04-09T00:00:00Z"
updated_at: "2026-04-09T00:00:00Z"
tags:
  - assets
  - google-drive
source_refs: []
topics:
  - voice-automation
project_refs:
  - eacy
entity_refs: []
decision_refs: []
summary: "Index of non-Markdown assets stored outside the repo"
capture_mode: command
command_refs:
  - assets.sync.drive
---

## Asset Table

| Asset ID | Type | Storage | Linked Notes | Summary |
|----------|------|---------|--------------|---------|
| `drv-audio-001` | audio | `https://drive.google.com/file/d/example-audio-001` | `knowledge/inbox/` | Raw meeting capture pending transcription review |
| `drv-pdf-014` | pdf | `https://drive.google.com/file/d/example-pdf-014` | `knowledge/topics/voice-architecture.md` | Voice architecture whitepaper for topic synthesis |
| `drv-slides-009` | slides | `https://drive.google.com/file/d/example-slides-009` | `knowledge/projects/eacy-roadmap.md` | Slides for external sharing and roadmap review |

## Sync Notes

- Use `assets.sync.drive` to refresh metadata and summaries.
- Keep the repo as the source of truth for descriptions, links, and note
  relationships.
