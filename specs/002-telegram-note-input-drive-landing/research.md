# Research Notes

## Decision 1: Use a FastAPI Webhook Vertical Slice in `apps.voice_gateway`

- **Decision**: Implement Telegram intake as a real FastAPI webhook flow under
  `apps.voice_gateway`, with a thin endpoint handing off to a dedicated
  orchestration module.
- **Rationale**: This matches the existing runtime boundary in the repo and
  delivers a practical, testable input channel without scattering orchestration
  across scripts or external services.
- **Alternatives considered**:
  - Service-only implementation without a webhook: rejected because it does not
    produce the real intake path the feature is meant to add.
  - Telegram-specific monolith module: rejected because it would mix webhook,
    adapter, transformation, and persistence concerns.

## Decision 2: Keep External Systems Behind Typed Worker Adapters

- **Decision**: Implement Telegram retrieval, OpenAI transcription, and Google
  Drive upload behind separate worker adapters in `apps/workers/`.
- **Rationale**: Adapter boundaries keep network behavior, retries, auth, and
  provider-specific payloads out of the webhook handler and make contracts easier
  to test and swap later.
- **Alternatives considered**:
  - Direct HTTP calls from the webhook handler: rejected because it weakens
    separation of concerns and makes testing harder.
  - One generalized "integration client": rejected because Telegram, OpenAI, and
    Drive have different auth models and failure modes.

## Decision 3: Use OAuth User Tokens for Google Drive

- **Decision**: Authenticate Google Drive uploads through an OAuth user-token
  flow documented in the repo rather than a service account.
- **Rationale**: This is a personal project tied to one operator-owned Drive
  account, so OAuth user tokens are the simplest "run anywhere" solution that
  still keeps config surfaces explicit and reviewable.
- **Alternatives considered**:
  - Service account: rejected because it adds unnecessary setup friction for a
    single-user personal workflow.
  - Manual browser-only upload step: rejected because it moves logic outside the
    repo and breaks repeatability.

## Decision 4: Use a Dedicated Landing-Note Schema Plus a Separate Manifest Schema

- **Decision**: Validate repo-native Telegram landing records against a new
  `landing-note` schema and persist machine-readable state in a separate
  `landing-manifest` schema.
- **Rationale**: Ingress landing records carry Telegram metadata, Drive refs,
  processing state, and reconciliation details that do not fit the lifecycle of
  normalized KMS notes validated by `note.schema.json`.
- **Alternatives considered**:
  - Extend `note.schema.json`: rejected because it would overload long-term KMS
    note semantics with ingress-only fields and statuses.
  - Manifest-only storage: rejected because the repo also needs a human-readable
    landing record for review and traceability.

## Decision 5: Treat Drive Markdown as Ingress-Stage Only

- **Decision**: Store the first landed Markdown document in Google Drive, but
  keep the repository authoritative through landing records, manifests, sync
  state, and future import logic.
- **Rationale**: This satisfies the mobile-friendly landing-zone requirement
  while remaining consistent with the amended constitution and the repo’s
  Everything-as-Code model.
- **Alternatives considered**:
  - Repo-first Markdown only: rejected because the feature explicitly targets
    Drive as the first landing zone.
  - Drive-only storage with no repo landing artifacts: rejected because it would
    fracture the control plane and hide operational state.

## Decision 6: Make Idempotency and Reconciliation First-Class

- **Decision**: Key retry safety off stable Telegram identifiers plus a stable
  landing note identifier, and represent partial-success outcomes explicitly in
  landing manifests.
- **Rationale**: Telegram can retry webhooks and external providers can fail
  independently. The system needs deterministic duplicate handling and recoverable
  state from the first version.
- **Alternatives considered**:
  - Best-effort retries without a manifest state model: rejected because it risks
    duplicate notes and silent drift between Drive and repo state.
  - Delete-on-failure cleanup in Drive: rejected because cleanup can fail and
    would hide useful recovery information.

## Decision 7: Scaffold Future Sync from Repo Manifests, Not Hidden Runtime State

- **Decision**: Add a sync-oriented module and contract that read repo-native
  landing manifests to determine import readiness for normalized KMS locations.
- **Rationale**: Future sync work stays reviewable and deterministic when the
  repo, not ephemeral runtime memory, defines what should be imported next.
- **Alternatives considered**:
  - Deferred sync design: rejected because the landing flow would hard-code
    assumptions that later import logic would have to rediscover.
  - Drive-first sync scanning with no repo state: rejected because it weakens the
    repository as the durable control plane.
