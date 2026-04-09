from __future__ import annotations

from typing import Any, Callable

from fastapi import FastAPI

from apps.voice_gateway.telegram_input_flow import process_telegram_update


def create_telegram_webhook_app(
    repo_root: str,
    drive_folder_id: str,
    processor: Callable[[dict[str, Any], str, str], dict[str, Any]] | None = None,
) -> FastAPI:
    app = FastAPI()
    run_processor = processor or (
        lambda update, root, folder: process_telegram_update(
            update=update,
            repo_root=root,
            drive_folder_id=folder,
        )
    )

    @app.post("/telegram/webhook")
    def telegram_webhook(update: dict[str, Any]) -> dict[str, Any]:
        result = run_processor(update, repo_root, drive_folder_id)
        if not result.get("accepted", False):
            return {"accepted": False, "status": "ignored", "reason": result.get("reason", "unsupported_update")}
        return {"accepted": True, "status": "processed", "landing_id": result["landing_id"]}

    return app
