# Quickstart

## Goal

Validate that the repository already contains the control-plane assets required
to start implementing the runtime.

## 1. Review the Architecture

Open:

- `/docs/architecture/system-overview.md`
- `/docs/repo-tree.md`
- `/specs/001-voice-kms-automation/spec.md`

## 2. Inspect the Repo-Native Backbone

From the repo root:

```bash
find knowledge registry policies schemas automation integrations templates prompts deploy -maxdepth 2 -type f | sort
```

Expected outcome: starter notes, registry entries, policy definitions, JSON
schemas, workflow contracts, and integration contracts are visible in one place.

## 3. Inspect Spec-Driven Artifacts

```bash
find specs/001-voice-kms-automation -maxdepth 2 -type f | sort
```

Expected outcome: `spec.md`, `plan.md`, `research.md`, `data-model.md`,
`quickstart.md`, `contracts/`, `checklists/`, and `tasks.md` are present.

## 4. Validate JSON Schemas

```bash
python3 - <<'PY'
import json
from pathlib import Path

for path in sorted(Path("schemas").glob("*.json")):
    json.loads(path.read_text())
    print(f"validated {path}")
PY
```

Expected outcome: each schema file parses successfully as JSON.

## 5. Review Starter Command and Policy Definitions

Open:

- `/registry/commands.yaml`
- `/policies/execution-policy.yaml`

Confirm that each command defines trigger phrases, risk, confirmation, input
schema, executor type, and output contract.

## 6. Continue with Implementation

Use `/specs/001-voice-kms-automation/tasks.md` as the execution backlog for the
next iteration.
