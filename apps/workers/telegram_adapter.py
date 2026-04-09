from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def normalize_telegram_update(update: dict[str, Any], received_at: str | None = None) -> dict[str, Any] | None:
    message = update.get("message") or {}
    media = message.get("voice") or message.get("audio")
    if not media:
        return None

    kind = "voice" if message.get("voice") else "audio"
    chat = message.get("chat") or {}
    sender = message.get("from") or {}
    update_id = int(update["update_id"])
    message_id = int(message.get("message_id", 0))

    return {
        "envelope_id": f"tg-{update_id}-{message_id}",
        "update_id": update_id,
        "message_id": message_id,
        "message_kind": kind,
        "telegram_file_id": media["file_id"],
        "telegram_file_unique_id": media.get("file_unique_id", ""),
        "mime_type": media.get("mime_type", "application/octet-stream"),
        "duration_seconds": int(media.get("duration", 0)),
        "received_at": received_at or _utc_now_iso(),
        "source": {
            "provider": "telegram",
            "chat_id": str(chat.get("id", "")),
            "user_id": str(sender.get("id", "")),
            "username": sender.get("username", ""),
        },
    }


def build_file_download_url(bot_token: str, file_path: str) -> str:
    return f"https://api.telegram.org/file/bot{bot_token}/{file_path}"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
