#!/usr/bin/env python3
"""Create and sync the realtime task dashboard to Feishu Base."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "agents" / "realtime-tracking" / "lark-dashboard.json"
STATE_PATH = ROOT / "tmp" / "realtime-tracking" / "dashboard-state.json"

PROJECT_FIELDS = [
    {"name": "项目ID", "type": "text"},
    {"name": "项目名称", "type": "text"},
    {"name": "负责人", "type": "text"},
    {"name": "团队", "type": "text"},
    {"name": "状态", "type": "select", "options": [{"name": value} for value in ["todo", "doing", "review", "blocked", "done", "unknown"]]},
    {"name": "证据分", "type": "number"},
    {"name": "预计工作量", "type": "text"},
    {"name": "置信度", "type": "number"},
    {"name": "手动校正", "type": "number"},
    {"name": "本地文件数", "type": "number"},
    {"name": "WIP任务", "type": "number"},
    {"name": "阻塞数", "type": "number"},
    {"name": "风险", "type": "text"},
    {"name": "更新时间", "type": "datetime"},
    {"name": "快照日期", "type": "datetime"},
]

PEOPLE_FIELDS = [
    {"name": "成员ID", "type": "text"},
    {"name": "成员", "type": "text"},
    {"name": "团队", "type": "text"},
    {"name": "证据分", "type": "number"},
    {"name": "可见项目数", "type": "number"},
    {"name": "手填项目数", "type": "number"},
    {"name": "项目偏差", "type": "number"},
    {"name": "预计工作量", "type": "text"},
    {"name": "置信度", "type": "number"},
    {"name": "手动校正", "type": "number"},
    {"name": "管理动作", "type": "text"},
    {"name": "更新时间", "type": "datetime"},
    {"name": "快照日期", "type": "datetime"},
]

SOURCE_FIELDS = [
    {"name": "数据源ID", "type": "text"},
    {"name": "数据源", "type": "text"},
    {"name": "状态", "type": "select", "options": [{"name": value} for value in ["online", "limited", "ready", "pending_credentials", "blocked_by_scope"]]},
    {"name": "记录数", "type": "number"},
    {"name": "最近同步", "type": "text"},
    {"name": "限制", "type": "text"},
    {"name": "更新时间", "type": "datetime"},
]

RISK_FIELDS = [
    {"name": "风险ID", "type": "text"},
    {"name": "项目ID", "type": "text"},
    {"name": "项目", "type": "text"},
    {"name": "级别", "type": "select", "options": [{"name": value} for value in ["P0", "P1", "P2", "P3"]]},
    {"name": "状态", "type": "select", "options": [{"name": value} for value in ["open", "tracking", "resolved"]]},
    {"name": "风险", "type": "text"},
    {"name": "负责人", "type": "text"},
    {"name": "置信度", "type": "number"},
    {"name": "更新时间", "type": "datetime"},
    {"name": "快照日期", "type": "datetime"},
]

CHANGE_FIELDS = [
    {"name": "变化ID", "type": "text"},
    {"name": "对象类型", "type": "select", "options": [{"name": value} for value in ["project", "person", "source", "risk"]]},
    {"name": "对象ID", "type": "text"},
    {"name": "对象名称", "type": "text"},
    {"name": "变化摘要", "type": "text"},
    {"name": "证据分", "type": "number"},
    {"name": "状态", "type": "text"},
    {"name": "更新时间", "type": "datetime"},
    {"name": "快照日期", "type": "datetime"},
]

TABLE_SPECS = {
    "projects": ("项目状态", PROJECT_FIELDS),
    "people": ("人员负载", PEOPLE_FIELDS),
    "sources": ("数据源健康", SOURCE_FIELDS),
    "risks": ("风险队列", RISK_FIELDS),
    "changes": ("每日变化", CHANGE_FIELDS),
}


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_config(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def run_lark(args: list[str], dry_run: bool = False) -> dict[str, Any]:
    command = ["lark-cli", *args]
    if dry_run and "--dry-run" not in command:
        command.append("--dry-run")
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = proc.stdout.strip()
    error = proc.stderr.strip()
    try:
        payload = json.loads(output) if output else {}
    except json.JSONDecodeError:
        payload = {"raw_stdout": output}
    if proc.returncode != 0:
        try:
            err_payload = json.loads(error) if error else payload
        except json.JSONDecodeError:
            err_payload = {"raw_stderr": error, "raw_stdout": output}
        raise RuntimeError(json.dumps({"command": command, "returncode": proc.returncode, "error": err_payload}, ensure_ascii=False))
    return payload


def find_first_key(value: Any, keys: set[str]) -> Any:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in keys and item:
                return item
        for item in value.values():
            found = find_first_key(item, keys)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = find_first_key(item, keys)
            if found:
                return found
    return None


def collect_records(value: Any) -> list[dict[str, Any]]:
    records = []
    if isinstance(value, dict):
        if any(key in value for key in ("record_id", "id")) and isinstance(value.get("fields"), dict):
            records.append(value)
        for item in value.values():
            records.extend(collect_records(item))
    elif isinstance(value, list):
        for item in value:
            records.extend(collect_records(item))
    return records


def feishu_datetime(value: str | None) -> str | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
        return parsed.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return value[:19].replace("T", " ")


def snapshot_datetime(value: str | None) -> str | None:
    if not value:
        return None
    return f"{value[:10]} 00:00:00"


def create_base(config: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
    title = config["dashboard"]["title"]
    identity = config["dashboard"].get("identity", "bot")
    payload = run_lark(
        [
            "base",
            "+base-create",
            "--name",
            title,
            "--table-name",
            TABLE_SPECS["projects"][0],
            "--fields",
            json.dumps(PROJECT_FIELDS, ensure_ascii=False),
            "--time-zone",
            "Asia/Shanghai",
            "--as",
            identity,
            "--format",
            "json",
        ],
        dry_run=dry_run,
    )
    if dry_run:
        print(json.dumps({"dry_run": "base-create", "request": payload}, ensure_ascii=False))
        return config

    base_token = find_first_key(payload, {"base_token", "app_token", "token"})
    url = find_first_key(payload, {"url", "app_url"})
    if not base_token:
        raise RuntimeError(f"无法从创建结果中识别 base token: {json.dumps(payload, ensure_ascii=False)[:1000]}")
    config["dashboard"]["base_token"] = base_token
    if url:
        config["dashboard"]["url"] = url
    refresh_table_ids(config)
    return config


def refresh_table_ids(config: dict[str, Any]) -> None:
    base_token = config["dashboard"]["base_token"]
    identity = config["dashboard"].get("identity", "bot")
    payload = run_lark(["base", "+table-list", "--base-token", base_token, "--as", identity, "--format", "json"])
    table_map: dict[str, str] = {}

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            name = value.get("name") or value.get("table_name")
            table_id = value.get("table_id") or value.get("id")
            if name and table_id:
                table_map[str(name)] = str(table_id)
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(payload)
    for key, (table_name, _fields) in TABLE_SPECS.items():
        if table_name in table_map:
            config["tables"][key]["table_id"] = table_map[table_name]


def ensure_tables(config: dict[str, Any], dry_run: bool = False) -> None:
    base_token = config["dashboard"]["base_token"]
    identity = config["dashboard"].get("identity", "bot")
    refresh_table_ids(config)
    for key, (table_name, fields) in TABLE_SPECS.items():
        if config["tables"][key].get("table_id"):
            continue
        payload = run_lark(
            [
                "base",
                "+table-create",
                "--base-token",
                base_token,
                "--name",
                table_name,
                "--fields",
                json.dumps(fields, ensure_ascii=False),
                "--as",
                identity,
                "--format",
                "json",
            ],
            dry_run=dry_run,
        )
        if dry_run:
            print(json.dumps({"dry_run": "table-create", "table": table_name, "request": payload}, ensure_ascii=False))
        else:
            table_id = find_first_key(payload, {"table_id", "id"})
            if table_id:
                config["tables"][key]["table_id"] = table_id
    if not dry_run:
        refresh_table_ids(config)


def ensure_dashboard(config: dict[str, Any], dry_run: bool = False) -> None:
    base_token = config["dashboard"]["base_token"]
    identity = config["dashboard"].get("identity", "bot")
    if not config["dashboard"].get("dashboard_id"):
        payload = run_lark(
            [
                "base",
                "+dashboard-create",
                "--base-token",
                base_token,
                "--name",
                config["dashboard"]["title"],
                "--as",
                identity,
                "--format",
                "json",
            ],
            dry_run=dry_run,
        )
        if dry_run:
            print(json.dumps({"dry_run": "dashboard-create", "request": payload}, ensure_ascii=False))
            return
        dashboard_id = find_first_key(payload, {"dashboard_id", "block_id", "id"})
        if not dashboard_id:
            raise RuntimeError(f"无法从创建结果中识别 dashboard id: {json.dumps(payload, ensure_ascii=False)[:1000]}")
        config["dashboard"]["dashboard_id"] = dashboard_id

    dashboard_id = config["dashboard"]["dashboard_id"]
    blocks = [
        (
            "看板说明",
            "text",
            {
                "text": "# Unity HMI 实时任务跟踪看板\n每日自动更新。evidence_score 是可见证据强度，不等于绩效分；estimated_effort 等待 Jira、Sheet/Base 和本地 artifact 校准。"
            },
        ),
        ("项目数", "statistics", {"table_name": "项目状态", "count_all": True}),
        ("开放风险", "statistics", {"table_name": "风险队列", "count_all": True, "filter": {"conjunction": "and", "conditions": [{"field_name": "状态", "operator": "is", "value": "open"}]}}),
        ("项目证据分", "bar", {"table_name": "项目状态", "series": [{"field_name": "证据分", "rollup": "SUM"}], "group_by": [{"field_name": "项目名称", "mode": "integrated", "sort": {"type": "value", "order": "desc"}}]}),
        ("项目状态分布", "pie", {"table_name": "项目状态", "count_all": True, "group_by": [{"field_name": "状态", "mode": "integrated"}]}),
        ("人员可见负载", "bar", {"table_name": "人员负载", "series": [{"field_name": "证据分", "rollup": "SUM"}], "group_by": [{"field_name": "成员", "mode": "integrated", "sort": {"type": "value", "order": "desc"}}]}),
        ("数据源状态", "pie", {"table_name": "数据源健康", "count_all": True, "group_by": [{"field_name": "状态", "mode": "integrated"}]}),
    ]
    for name, block_type, data_config in blocks:
        payload = run_lark(
            [
                "base",
                "+dashboard-block-create",
                "--base-token",
                base_token,
                "--dashboard-id",
                dashboard_id,
                "--name",
                name,
                "--type",
                block_type,
                "--data-config",
                json.dumps(data_config, ensure_ascii=False),
                "--as",
                identity,
                "--format",
                "json",
            ],
            dry_run=dry_run,
        )
        if dry_run:
            print(json.dumps({"dry_run": "dashboard-block-create", "block": name, "request": payload}, ensure_ascii=False))


def find_record_id(base_token: str, table_id: str, key_field: str, key_value: str) -> str | None:
    config = load_config(CONFIG_PATH)
    identity = config["dashboard"].get("identity", "bot")
    payload = run_lark(
        [
            "base",
            "+record-search",
            "--base-token",
            base_token,
            "--table-id",
            table_id,
            "--keyword",
            key_value,
            "--search-field",
            key_field,
            "--field-id",
            key_field,
            "--limit",
            "10",
            "--as",
            identity,
            "--format",
            "json",
        ]
    )
    for record in collect_records(payload):
        fields = record.get("fields") or {}
        if str(fields.get(key_field, "")).strip() == key_value:
            return record.get("record_id") or record.get("id")
    return None


def upsert_record(base_token: str, table_id: str, key_field: str, row: dict[str, Any], dry_run: bool = False) -> str:
    key_value = str(row[key_field])
    record_id = None if dry_run else find_record_id(base_token, table_id, key_field, key_value)
    config = load_config(CONFIG_PATH)
    identity = config["dashboard"].get("identity", "bot")
    args = [
        "base",
        "+record-upsert",
        "--base-token",
        base_token,
        "--table-id",
        table_id,
        "--json",
        json.dumps(row, ensure_ascii=False),
        "--as",
        identity,
        "--format",
        "json",
    ]
    if record_id:
        args.extend(["--record-id", record_id])
    run_lark(args, dry_run=dry_run)
    return "updated" if record_id else "created"


def project_row(item: dict[str, Any]) -> dict[str, Any]:
    tasks = item.get("tasks", {})
    return {
        "项目ID": item["project_id"],
        "项目名称": item["name"],
        "负责人": item.get("owner_name"),
        "团队": item.get("organization_team"),
        "状态": item.get("status"),
        "证据分": item.get("evidence_score", 0),
        "预计工作量": "待校准" if item.get("estimated_effort") is None else str(item.get("estimated_effort")),
        "置信度": item.get("confidence", 0),
        "手动校正": item.get("manual_adjustment", 0),
        "本地文件数": item.get("local_artifacts", 0),
        "WIP任务": tasks.get("doing", 0) + tasks.get("review", 0) + tasks.get("blocked", 0),
        "阻塞数": tasks.get("blocked", 0),
        "风险": "；".join(item.get("risks", [])),
        "更新时间": feishu_datetime(item.get("updated_at")),
        "快照日期": snapshot_datetime(item.get("snapshot_date")),
    }


def person_row(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "成员ID": item.get("agent_id"),
        "成员": item.get("name"),
        "团队": item.get("organization_team"),
        "证据分": item.get("evidence_score", 0),
        "可见项目数": item.get("visible_project_count", 0),
        "手填项目数": item.get("manual_project_count", 0),
        "项目偏差": item.get("project_delta", 0),
        "预计工作量": "待校准" if item.get("estimated_effort") is None else str(item.get("estimated_effort")),
        "置信度": item.get("confidence", 0),
        "手动校正": item.get("manual_adjustment", 0),
        "管理动作": item.get("management_note", ""),
        "更新时间": feishu_datetime(item.get("updated_at")),
        "快照日期": snapshot_datetime(item.get("snapshot_date")),
    }


def source_row(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "数据源ID": item.get("source_id"),
        "数据源": item.get("name"),
        "状态": item.get("status"),
        "记录数": item.get("count", 0),
        "最近同步": item.get("last_sync_at") or "",
        "限制": item.get("limitation", ""),
        "更新时间": feishu_datetime(item.get("updated_at")),
    }


def risk_row(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "风险ID": item.get("risk_id"),
        "项目ID": item.get("project_id"),
        "项目": item.get("project_name"),
        "级别": item.get("severity"),
        "状态": item.get("status"),
        "风险": item.get("risk"),
        "负责人": item.get("owner_name"),
        "置信度": item.get("confidence", 0),
        "更新时间": feishu_datetime(item.get("updated_at")),
        "快照日期": snapshot_datetime(item.get("snapshot_date")),
    }


def sync_rows(config: dict[str, Any], state: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
    base_token = config["dashboard"]["base_token"]
    sync_plan = [
        ("projects", "项目ID", [project_row(item) for item in state.get("projects", [])]),
        ("people", "成员ID", [person_row(item) for item in state.get("people", []) if item.get("agent_id")]),
        ("sources", "数据源ID", [source_row(item) for item in state.get("sources", [])]),
        ("risks", "风险ID", [risk_row(item) for item in state.get("risks", [])]),
    ]
    summary: dict[str, Any] = {}
    for table_key, key_field, rows in sync_plan:
        table_id = config["tables"][table_key]["table_id"]
        created = 0
        updated = 0
        for row in rows:
            result = upsert_record(base_token, table_id, key_field, row, dry_run=dry_run)
            if result == "updated":
                updated += 1
            else:
                created += 1
        summary[table_key] = {"created": created, "updated": updated, "total": len(rows)}
    return summary


def grant_team(config: dict[str, Any], dry_run: bool = False) -> None:
    base_token = config["dashboard"]["base_token"]
    team = config["permissions"]["team_chat"]
    identity = config["dashboard"].get("identity", "bot")
    run_lark(
        [
            "drive",
            "+member-add",
            "--token",
            base_token,
            "--type",
            "bitable",
            "--member-type",
            team["member_type"],
            "--member-id",
            team["member_id"],
            "--perm",
            team.get("perm", "view"),
            "--as",
            identity,
            "--format",
            "json",
            "--yes",
        ],
        dry_run=dry_run,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create and sync the Feishu Base realtime dashboard.")
    parser.add_argument("--create", action="store_true", help="Create the Base, tables, and dashboard when missing.")
    parser.add_argument("--sync", action="store_true", help="Sync dashboard state records.")
    parser.add_argument("--grant-team", action="store_true", help="Grant the Unity HMI Design chat view access.")
    parser.add_argument("--dry-run", action="store_true", help="Print Feishu requests without executing writes.")
    args = parser.parse_args()

    config = load_config(CONFIG_PATH)
    if args.create and not config["dashboard"].get("base_token"):
        config = create_base(config, dry_run=args.dry_run)
    if args.create and config["dashboard"].get("base_token"):
        ensure_tables(config, dry_run=args.dry_run)
        ensure_dashboard(config, dry_run=args.dry_run)
        if not args.dry_run:
            save_config(CONFIG_PATH, config)

    if args.sync:
        if not config["dashboard"].get("base_token"):
            raise SystemExit("缺少 base_token。请先运行 --create，或在 agents/realtime-tracking/lark-dashboard.json 中填入现有 Base。")
        ensure_tables(config, dry_run=args.dry_run)
        if not STATE_PATH.exists():
            raise SystemExit("缺少 dashboard-state.json。请先运行 tools/generate-realtime-dashboard-state.py。")
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        summary = sync_rows(config, state, dry_run=args.dry_run)
        if not args.dry_run:
            save_config(CONFIG_PATH, config)
        print(json.dumps({"status": "ok", "sync": summary}, ensure_ascii=False))

    if args.grant_team:
        if not config["dashboard"].get("base_token"):
            raise SystemExit("缺少 base_token，无法授权团队。")
        grant_team(config, dry_run=args.dry_run)
        print(json.dumps({"status": "ok", "permission": "team_view_granted"}, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
