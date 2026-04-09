# Repository Tree

```text
.
├── .github/
│   └── workflows/              # GitHub Actions automation samples
├── .specify/                   # Spec Kit engine and templates
├── apps/
│   ├── router/                 # Planned command routing runtime
│   ├── voice-gateway/          # Planned voice intake runtime
│   └── workers/                # Planned backend execution adapters
├── automation/
│   └── workflows/              # Repo-native workflow definitions
├── docs/
│   ├── architecture/           # Architecture and operating model docs
│   └── pseudocode/             # Runtime pseudocode and flow sketches
├── deploy/                     # Deployment targets and runtime destination metadata
├── integrations/
│   ├── n8n/                    # n8n contracts and docs
│   └── openclaw/               # OpenClaw or Clawbot contracts
├── knowledge/
│   ├── assets/                 # Asset indexes and summaries
│   ├── daily/                  # Daily notes
│   ├── decisions/              # Decision records
│   ├── entities/               # Entity notes
│   ├── inbox/                  # Raw captures awaiting curation
│   ├── projects/               # Project notes
│   ├── references/             # Curated references
│   ├── sources/                # Source pack indexes
│   ├── topics/                 # Curated topic notes
│   └── weekly/                 # Weekly rollups
├── policies/                   # Execution and safety policy definitions
├── prompts/                    # Prompt library for transformation and curation
├── registry/                   # Command registry
├── schemas/                    # JSON schemas for core contracts
├── specs/
│   └── 001-voice-kms-automation/
│       ├── checklists/
│       ├── contracts/
│       ├── data-model.md
│       ├── plan.md
│       ├── quickstart.md
│       ├── research.md
│       ├── spec.md
│       └── tasks.md
├── templates/
│   └── notes/                  # Markdown note templates
└── tests/
    ├── contract/
    ├── integration/
    └── unit/
```

This structure separates durable definitions from runtime code and keeps the
knowledge base, automation contracts, and governance assets first-class.
