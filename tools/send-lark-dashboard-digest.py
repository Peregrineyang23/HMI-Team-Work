#!/usr/bin/env python3
"""Send a daily realtime dashboard digest to the Unity HMI Design Feishu group.

This is the fallback channel when Feishu Base permissions are blocked.
Use --send to actually post; without --send the script only prints the message.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "tmp" / "realtime-tracking" / "dashboard-state.json"
DEFAULT_CHAT_ID = "oc_824642a195aa4a6d1fd2861fd8c749da"


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        raise SystemExit("缺少 dashboard-state.json。请先运行 tools/generate-realtime-dashboard-state.py。")
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def top_projects(state: dict[str, Any], limit: int = 6) -> list[dict[str, Any]]:
    return sorted(state.get("projects", []), key=lambda item: item.get("evidence_score", 0), reverse=True)[:limit]


def top_people(state: dict[str, Any], limit: int = 6) -> list[dict[str, Any]]:
    return sorted(state.get("people", []), key=lambda item: item.get("evidence_score", 0), reverse=True)[:limit]


def open_risks(state: dict[str, Any], limit: int = 5) -> list[dict[str, Any]]:
    priority = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    risks = [item for item in state.get("risks", []) if item.get("status") == "open"]
    return sorted(risks, key=lambda item: (priority.get(item.get("severity"), 9), item.get("project_name", "")))[:limit]


def build_markdown(state: dict[str, Any]) -> str:
    metrics = state.get("metrics", {})
    lines = [
        "## Unity HMI 实时任务跟踪看板",
        "",
        f"更新时间：{state.get('generated_at')}（{state.get('timezone', 'Asia/Shanghai')}）",
        "",
        "### 今日总览",
        f"- 项目：{metrics.get('project_count', 0)} 个",
        f"- 成员：{metrics.get('people_count', 0)} 人",
        f"- 开放风险：{metrics.get('open_risk_count', 0)} 条",
        f"- 已知可见证据：{metrics.get('known_evidence_count', 0)} 条",
        f"- 本地 artifact：{metrics.get('local_artifact_count', 0)} 个",
        "",
        "### 项目热度 Top",
    ]
    for item in top_projects(state):
        risks = "；".join(item.get("risks", [])[:2]) or "暂无开放风险"
        lines.append(
            f"- {item.get('name')}：证据分 {item.get('evidence_score', 0)}，状态 {item.get('status')}，负责人 {item.get('owner_name') or '待确认'}，风险：{risks}"
        )

    lines.extend(["", "### 人员可见负载 Top"])
    for item in top_people(state):
        note = f"，管理动作：{item.get('management_note')}" if item.get("management_note") else ""
        lines.append(
            f"- {item.get('name')}：证据分 {item.get('evidence_score', 0)}，可见项目 {item.get('visible_project_count', 0)}，手填项目 {item.get('manual_project_count', 0)}{note}"
        )

    lines.extend(["", "### 风险队列"])
    risks = open_risks(state)
    if risks:
        for item in risks:
            lines.append(f"- [{item.get('severity')}] {item.get('project_name')}：{item.get('risk')}（owner：{item.get('owner_name')}）")
    else:
        lines.append("- 暂无开放风险。")

    lines.extend(
        [
            "",
            "### 数据口径",
            "- evidence_score 是可见证据强度，不是绩效分。",
            "- estimated_effort 等待 Jira、Sheet/Base 工时和本地 artifact 接入后校准。",
            "- 当前 Base 仪表盘受飞书应用权限阻塞，先用群内每日摘要保证团队可见。",
        ]
    )
    return "\n".join(lines)


def send_message(markdown: str, chat_id: str, identity: str, dry_run: bool) -> None:
    command = [
        "lark-cli",
        "im",
        "+messages-send",
        "--chat-id",
        chat_id,
        "--markdown",
        markdown,
        "--as",
        identity,
        "--format",
        "json",
    ]
    if dry_run:
        command.append("--dry-run")
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout)
    print(proc.stdout.strip() or json.dumps({"status": "ok", "dry_run": dry_run}, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Send daily dashboard digest to Feishu group.")
    parser.add_argument("--chat-id", default=DEFAULT_CHAT_ID, help="Target Feishu chat id.")
    parser.add_argument("--identity", default="bot", choices=["user", "bot"], help="Sending identity.")
    parser.add_argument("--send", action="store_true", help="Actually send the message. Omit for dry-run.")
    args = parser.parse_args()

    state = load_state()
    markdown = build_markdown(state)
    if not args.send:
        print(markdown)
        print("\n--- dry-run request ---")
    send_message(markdown, args.chat_id, args.identity, dry_run=not args.send)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
