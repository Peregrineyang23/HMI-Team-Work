#!/usr/bin/env python3
"""Refresh configured realtime Feishu chat sources before dashboard generation."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EMERGENCY_PROJECTS = ROOT / "agents" / "realtime-tracking" / "emergency-projects.json"
PAGE_SIZE = 50


def fetch_page(chat_id: str, start: str, page_token: str | None = None) -> dict[str, Any]:
    command = [
        "lark-cli", "im", "+chat-messages-list", "--as", "user",
        "--chat-id", chat_id, "--start", start, "--order", "asc",
        "--page-size", str(PAGE_SIZE), "--no-reactions", "--format", "json",
    ]
    if page_token:
        command.extend(["--page-token", page_token])
    env = os.environ.copy()
    env["LARKSUITE_CLI_NO_UPDATE_NOTIFIER"] = "1"
    env["LARKSUITE_CLI_NO_SKILLS_NOTIFIER"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise RuntimeError(f"Feishu chat refresh failed for {chat_id}: {detail}")
    envelope = json.loads(result.stdout)
    if envelope.get("ok") is not True:
        raise RuntimeError(f"Feishu chat refresh failed for {chat_id}: {json.dumps(envelope, ensure_ascii=False)}")
    return envelope.get("data", {})


def refresh_source(source: dict[str, Any]) -> dict[str, Any]:
    chat_id = source.get("chat_id")
    first_observed_at = source.get("first_observed_at")
    if not chat_id or not first_observed_at:
        raise RuntimeError("Realtime Feishu source requires chat_id and first_observed_at")

    messages: list[dict[str, Any]] = []
    page_token: str | None = None
    while True:
        page = fetch_page(chat_id, first_observed_at, page_token)
        messages.extend(page.get("messages", []))
        if not page.get("has_more"):
            break
        page_token = page.get("page_token")
        if not page_token:
            raise RuntimeError(f"Feishu pagination for {chat_id} reported has_more without page_token")

    visible = [message for message in messages if not message.get("deleted")]
    if not visible:
        raise RuntimeError(f"Feishu chat refresh returned no visible messages for {chat_id}")
    visible.sort(key=lambda item: (item.get("create_time", ""), item.get("message_position", "")))
    latest = visible[-1]
    source["message_count"] = len(visible)
    source["deleted_message_count"] = len(messages) - len(visible)
    source["last_observed_at"] = latest.get("create_time")
    source["last_message_id"] = latest.get("message_id")
    source["evidence_refs"] = [item["message_id"] for item in visible[-20:] if item.get("message_id")]
    source["collected_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    source["collection_identity"] = "user"
    source["collection_complete"] = True
    return source


def main() -> int:
    data = json.loads(EMERGENCY_PROJECTS.read_text(encoding="utf-8"))
    refreshed = []
    for project in data.get("projects", []):
        source = project.get("source", {})
        if source.get("source_system") != "feishu":
            continue
        refresh_source(source)
        refreshed.append({
            "project_id": project.get("project_id"),
            "chat_id": source.get("chat_id"),
            "message_count": source.get("message_count"),
            "last_observed_at": source.get("last_observed_at"),
            "collected_at": source.get("collected_at"),
        })
    data["generated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    EMERGENCY_PROJECTS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "refreshed": refreshed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
