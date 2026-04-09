# Quickstart

## Goal

Run and validate the Telegram note-input path with repo-native artifacts,
contracts, schemas, and tests.

## 1. Configure Telegram + Drive Environment

Set required local environment variables before running webhook flows:

```bash
export TELEGRAM_BOT_TOKEN="<bot-token>"
export TELEGRAM_WEBHOOK_SECRET="<secret-token>"
export GOOGLE_DRIVE_FOLDER_ID="<drive-folder-id>"
export GOOGLE_OAUTH_CLIENT_SECRET_FILE="<path-to-client-secret.json>"
export GOOGLE_OAUTH_TOKEN_FILE="<path-to-user-token.json>"
```

Expected outcome: bot/webhook auth and Drive OAuth inputs are available.

## 2. Validate Repo-Native Foundations

```bash
python3 -m json.tool schemas/telegram-update.schema.json >/dev/null
python3 -m json.tool schemas/telegram-intake-envelope.schema.json >/dev/null
python3 -m json.tool schemas/landing-note.schema.json >/dev/null
python3 -m json.tool schemas/landing-manifest.schema.json >/dev/null
python3 -m pytest tests/contract/test_telegram_input_contracts.py
```

Expected outcome: Telegram intake schemas and contracts parse and validate.

## 3. Run Telegram Intake MVP Tests

```bash
python3 -m pytest \
  tests/unit/test_telegram_adapter.py \
  tests/unit/test_transcription_adapter.py \
  tests/unit/test_google_drive_adapter.py \
  tests/unit/test_landing_record_writer.py \
  tests/integration/test_telegram_note_input.py
```

Expected outcome: success-path webhook ingestion and landing artifacts pass.

## 4. Run Retry + Reconciliation Tests

```bash
python3 -m pytest \
  tests/unit/test_landing_manifest_writer.py \
  tests/integration/test_telegram_note_retries.py \
  tests/integration/test_telegram_partial_failures.py
```

Expected outcome: duplicate retries are idempotent and partial failures persist
reconciliation metadata.

## 5. Run Sync Scaffold Tests

```bash
python3 -m pytest \
  tests/unit/test_drive_sync.py \
  tests/integration/test_drive_sync_scaffold.py
```

Expected outcome: sync candidate enumeration and pending-import scanning are
operational.

## 6. Final Repository Verification

```bash
python3 -m pytest
ruff check .
```

Expected outcome: repository-wide validation passes before merge.
