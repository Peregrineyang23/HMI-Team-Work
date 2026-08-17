#!/usr/bin/env python3
"""Calibrate realtime dashboard state with the manually maintained weekly report Base."""

from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "tmp" / "realtime-tracking" / "dashboard-state.json"
OUTPUT_JSON = ROOT / "tmp" / "realtime-tracking" / "weekly-report-calibration.json"
OUTPUT_MD = ROOT / "agents" / "realtime-tracking" / "weekly-report-calibration.md"

WEEKLY_BASE_TOKEN = "YUfJbhnHgawr7Wsp0UocNTqznte"
WEEKLY_TABLE_ID = "tbln0vm1ywBtaeeF"
IDENTITY = "user"
EXCLUDED_REPORTERS = {"张婕", "李达"}

MANUAL_PROJECT_MAP = {
    "一汽·红旗 8397 PS项目": ["hongqi-8397"],
    "一汽·红旗 POC": ["hongqi-8397"],
    "一汽·红旗 POC ": ["hongqi-8397"],
    "东风8397&4SR项目": ["dongfeng-8397", "dongfeng-4sr"],
    "东风悦享 M18_3 高阶智驾": ["dongfeng-4sr"],
    "东风M8_3 低阶智驾": ["dongfeng-4sr"],
    "东风M8_3 L2 海外": ["dongfeng-4sr"],
    "一汽·奔腾 E541": ["benteng-e541"],
    "一汽·奔腾实验室二期 POC": ["benteng-e541"],
    "奔驰项目": ["benz-hmi"],
    "广汽本田·音乐可视化 POC": ["gac-audio"],
    "车载游戏": ["lixiang-game"],
    "车载游戏商城 POC": ["lixiang-game"],
    "红旗DLP投影游戏 POC": ["lixiang-game"],
    "2026 北京车展": ["auto-show-demo"],
    "UNITE DEMO-POC": ["auto-show-demo"],
    "JETOUR - T1J&FL2": ["jetour-light"],
    "JETOUR - D02": ["jetour-light"],
    "JETOUR - D01": ["jetour-light"],
    "创新设计探索": ["research-figma"],
    "团队技能提升": ["design-system-platform"],
}

NO_RISK_VALUES = {"", "/", "无", "暂无", "无风险", "没有", "无。", "暂无。", "暂时还好"}
HIGH_RISK_KEYWORDS = ("风险", "延期", "延迟", "阻塞", "无法", "不稳定", "等待", "需要支援", "需帮助", "需求蔓延")


def run_lark(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(["lark-cli", *args], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout)
    return json.loads(proc.stdout or "{}")


def parse_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = payload.get("data", {})
    rows = data.get("data") or []
    fields = data.get("fields") or []
    record_ids = data.get("record_id_list") or []
    parsed = []
    for idx, row in enumerate(rows):
        if not isinstance(row, list):
            continue
        fields_map = {field: row[pos] if pos < len(row) else None for pos, field in enumerate(fields)}
        fields_map["_record_id"] = record_ids[idx] if idx < len(record_ids) else None
        parsed.append(fields_map)
    return parsed


def fetch_weekly_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    offset = 0
    while True:
        payload = run_lark(
            [
                "base",
                "+record-list",
                "--base-token",
                WEEKLY_BASE_TOKEN,
                "--table-id",
                WEEKLY_TABLE_ID,
                "--limit",
                "200",
                "--offset",
                str(offset),
                "--as",
                IDENTITY,
                "--format",
                "json",
            ]
        )
        records.extend(parse_records(payload))
        if not payload.get("data", {}).get("has_more"):
            break
        offset += 200
    return records


def text_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        if value and isinstance(value[0], dict):
            return "、".join(str(item.get("name", "")) for item in value if item.get("name"))
        return "、".join(str(item) for item in value)
    return str(value)


def list_names(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        names = []
        for item in value:
            if isinstance(item, dict):
                if item.get("name"):
                    names.append(str(item["name"]))
            elif item:
                names.append(str(item))
        return names
    return [str(value)]


def parse_datetime(value: Any) -> datetime | None:
    text = text_value(value)
    if not text:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text[:19], fmt)
        except ValueError:
            continue
    return None


def has_actionable_risk(value: Any) -> bool:
    text = text_value(value).strip()
    if text in NO_RISK_VALUES:
        return False
    return bool(text)


def is_high_risk(value: Any) -> bool:
    text = text_value(value)
    return any(keyword in text for keyword in HIGH_RISK_KEYWORDS)


def calibrate_state(state: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    clean_records = []
    unmapped: dict[str, int] = defaultdict(int)
    per_project: dict[str, list[dict[str, Any]]] = defaultdict(list)
    latest_date = None

    for record in records:
        reporters = list_names(record.get("汇报人"))
        if any(name in EXCLUDED_REPORTERS for name in reporters):
            continue
        date_value = parse_datetime(record.get("填报日期（自动）"))
        if date_value and (latest_date is None or date_value > latest_date):
            latest_date = date_value
        projects = list_names(record.get("所属项目"))
        mapped_project_ids = []
        for project_name in projects:
            project_ids = MANUAL_PROJECT_MAP.get(project_name.strip())
            if project_ids:
                mapped_project_ids.extend(project_ids)
            else:
                unmapped[project_name] += 1
        normalized = {
            "record_id": record.get("_record_id"),
            "title": text_value(record.get("汇报标题")),
            "projects": projects,
            "project_ids": sorted(set(mapped_project_ids)),
            "reporters": reporters,
            "date": date_value.isoformat(timespec="seconds") if date_value else None,
            "week": text_value(record.get("周会周别")),
            "progress": text_value(record.get("本周进展")),
            "next_plan": text_value(record.get("下周计划")),
            "risk": text_value(record.get("问题、风险、需帮助项")).strip(),
            "has_risk": has_actionable_risk(record.get("问题、风险、需帮助项")),
            "high_risk": is_high_risk(record.get("问题、风险、需帮助项")),
        }
        clean_records.append(normalized)
        for project_id in normalized["project_ids"]:
            per_project[project_id].append(normalized)

    recent_cutoff = (latest_date or datetime.now()) - timedelta(days=45)
    project_summaries = {}
    for project_id, items in per_project.items():
        recent = [item for item in items if item["date"] and datetime.fromisoformat(item["date"]) >= recent_cutoff]
        risk_items = [item for item in recent if item["has_risk"]]
        high_risk_items = [item for item in recent if item["high_risk"]]
        reporters = sorted({name for item in recent or items for name in item["reporters"]})
        latest_item = max(items, key=lambda item: item["date"] or "")
        project_summaries[project_id] = {
            "weekly_report_count": len(items),
            "recent_report_count": len(recent),
            "recent_risk_count": len(risk_items),
            "recent_high_risk_count": len(high_risk_items),
            "latest_report_at": latest_item["date"],
            "latest_week": latest_item["week"],
            "recent_reporters": reporters,
            "latest_risk": next((item["risk"] for item in reversed(recent) if item["has_risk"]), ""),
        }

    now = datetime.now().astimezone().isoformat(timespec="seconds")
    for project in state.get("projects", []):
        summary = project_summaries.get(project.get("project_id"))
        if not summary:
            continue
        project["manual_adjustment"] = summary["recent_report_count"]
        project["confidence"] = round(min(float(project.get("confidence", 0)) + 0.08, 0.95), 2)
        project["updated_at"] = now
        if summary["recent_high_risk_count"]:
            project["status"] = "blocked"
            project.setdefault("tasks", {})["blocked"] = max(project.get("tasks", {}).get("blocked", 0), 1)
        elif project.get("status") == "unknown" and summary["recent_report_count"]:
            project["status"] = "doing"
        risk_note = f"人工周报校准：近45天 {summary['recent_report_count']} 条，风险/需帮助 {summary['recent_risk_count']} 条"
        if risk_note not in project.get("risks", []):
            project.setdefault("risks", []).append(risk_note)

    existing_risk_ids = {risk.get("risk_id") for risk in state.get("risks", [])}
    project_name_by_id = {project.get("project_id"): project.get("name") for project in state.get("projects", [])}
    owner_by_id = {project.get("project_id"): project.get("owner_name") for project in state.get("projects", [])}
    for project_id, summary in project_summaries.items():
        if not summary["recent_risk_count"]:
            continue
        risk_id = f"{project_id}-weekly-report"
        if risk_id in existing_risk_ids:
            continue
        state.setdefault("risks", []).append(
            {
                "risk_id": risk_id,
                "project_id": project_id,
                "project_name": project_name_by_id.get(project_id, project_id),
                "severity": "P0" if summary["recent_high_risk_count"] else "P1",
                "status": "open",
                "risk": summary["latest_risk"] or "人工周报存在风险/需帮助项",
                "owner_name": owner_by_id.get(project_id) or "杨帆",
                "confidence": 0.82,
                "updated_at": now,
                "snapshot_date": now[:10],
            }
        )

    sources = state.setdefault("sources", [])
    sources = [item for item in sources if item.get("source_id") != "weekly_report_base"]
    sources.append(
        {
            "source_id": "weekly_report_base",
            "name": "人工项目周报 Base",
            "status": "online",
            "count": len(clean_records),
            "last_sync_at": now,
            "limitation": "人工填报；已排除张婕和李达；用于校准任务看板，不等于绩效",
            "updated_at": now,
        }
    )
    state["sources"] = sources
    state["metrics"]["risk_count"] = len(state.get("risks", []))
    state["metrics"]["open_risk_count"] = sum(1 for risk in state.get("risks", []) if risk.get("status") == "open")

    calibration = {
        "generated_at": now,
        "source": {
            "base_token": WEEKLY_BASE_TOKEN,
            "table_id": WEEKLY_TABLE_ID,
            "record_count": len(records),
            "included_record_count": len(clean_records),
            "latest_report_at": latest_date.isoformat(timespec="seconds") if latest_date else None,
        },
        "excluded_reporters": sorted(EXCLUDED_REPORTERS),
        "project_summaries": project_summaries,
        "unmapped_projects": dict(sorted(unmapped.items(), key=lambda item: (-item[1], item[0]))),
    }
    return {"state": state, "calibration": calibration}


def write_report(calibration: dict[str, Any]) -> None:
    project_summaries = calibration["project_summaries"]
    lines = [
        "# 人工周报校准记录",
        "",
        f"- 生成时间：{calibration['generated_at']}",
        f"- 来源 Base：{calibration['source']['base_token']} / {calibration['source']['table_id']}",
        f"- 原始记录：{calibration['source']['record_count']}；纳入校准：{calibration['source']['included_record_count']}",
        f"- 最新填报时间：{calibration['source']['latest_report_at']}",
        f"- 排除人员：{', '.join(calibration['excluded_reporters'])}",
        "",
        "## 已映射项目",
        "",
        "| project_id | 全年周报数 | 近45天 | 近45天风险 | 最近周别 | 最近填报 | 近期汇报人 |",
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for project_id, item in sorted(project_summaries.items()):
        lines.append(
            "| {project_id} | {weekly_report_count} | {recent_report_count} | {recent_risk_count} | {latest_week} | {latest_report_at} | {reporters} |".format(
                project_id=project_id,
                reporters="、".join(item.get("recent_reporters", [])),
                **item,
            )
        )
    lines.extend(["", "## 未映射项目", ""])
    for name, count in calibration["unmapped_projects"].items():
        lines.append(f"- {name}: {count}")
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if not STATE_PATH.exists():
        raise SystemExit("缺少 dashboard-state.json。请先运行 tools/generate-realtime-dashboard-state.py。")
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    records = fetch_weekly_records()
    result = calibrate_state(state, records)
    STATE_PATH.write_text(json.dumps(result["state"], ensure_ascii=False, indent=2), encoding="utf-8")
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result["calibration"], ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result["calibration"])
    print(json.dumps({"status": "ok", "output": str(OUTPUT_JSON), "report": str(OUTPUT_MD)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
