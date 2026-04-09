# Voice Gateway

This runtime accepts voice-adjacent ingress payloads, classifies mode, and
routes typed requests into repo-governed paths.

Combined-mode coordination is implemented in `apps.voice_gateway.combined_mode`
and writes notes before invoking the governed command path.

## Telegram Intake (Feature 002)

The Telegram intake path provides a dedicated bot channel for voice/audio note
capture into Google Drive landing artifacts and repo-native manifests.

Core runtime modules:

- `apps.voice_gateway.telegram_webhook`: FastAPI webhook endpoint for Telegram
  updates.
- `apps.voice_gateway.telegram_input_flow`: intake orchestration for
  normalize/transcribe/upload/record/manifest behavior.
- `apps.workers.telegram_adapter`: Telegram update normalization.
- `apps.workers.transcription_adapter`: OpenAI-backed transcription adapter.
- `apps.workers.google_drive_adapter`: Google Drive upload adapter with
  partial-success metadata.
- `apps.workers.landing_record_writer`: writes repo-native Telegram landing
  Markdown under `knowledge/sources/telegram/`.
- `apps.workers.landing_manifest_writer`: writes machine-readable manifests
  under `knowledge/manifests/telegram/`.

### Setup Requirements

- Telegram bot token: `TELEGRAM_BOT_TOKEN`
- Telegram webhook secret token: `TELEGRAM_WEBHOOK_SECRET`
- Drive destination folder id: `GOOGLE_DRIVE_FOLDER_ID`
- OAuth client secret path: `GOOGLE_OAUTH_CLIENT_SECRET_FILE`
- OAuth user token path: `GOOGLE_OAUTH_TOKEN_FILE`

### Webhook Endpoint

- Method: `POST`
- Path: `/telegram/webhook`
- Contract: `integrations/telegram/note-input-webhook.contract.yaml`

### Validation

Run from repo root:

```bash
python3 -m pytest tests/integration/test_telegram_note_input.py
python3 -m pytest tests/integration/test_telegram_note_retries.py
python3 -m pytest tests/integration/test_telegram_partial_failures.py
```

The authoritative implementation plan remains in
`specs/002-telegram-note-input-drive-landing/tasks.md`.
