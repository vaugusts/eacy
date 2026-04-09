# Note Curation Prompt

## Purpose

Transform raw captures into curated Markdown without losing provenance.

## Instructions

1. Preserve the original meaning of the source transcript.
2. Convert rambling phrasing into concise Markdown sections.
3. Keep explicit source references, topic links, project links, and decisions.
4. Separate factual statements from suggested actions.
5. If a command outcome exists, link it under a dedicated `## Automation` or
   `## Follow-up` section instead of merging it into the factual summary.

## Expected Output Shape

- Frontmatter that conforms to `schemas/note.schema.json`
- `## Summary`
- `## Key Points`
- `## Sources`
- `## Follow-up`
