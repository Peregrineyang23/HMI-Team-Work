#!/usr/bin/env python3
"""Generate realtime dashboard state from current evidence indexes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKLOAD_EVIDENCE = ROOT / "agents" / "analysis" / "workload-evidence-2026.json"
LOCAL_ARTIFACT_INDEX = ROOT / "tmp" / "local-artifact-index.json"
STATE_OUTPUT = ROOT / "tmp" / "realtime-tracking" / "dashboard-state.json"


PROJECT_STATUS_OVERRIDES = {
    "hongqi-8397": "blocked",
    "auto-show-demo": "review",
    "aios-ai-workflow": "doing",
    "dongfeng-8397": "doing",
    "design-system-platform": "review",
    "lixiang-game": "review",
    "jetour-light": "unknown",
}

PROJECT_OWNER_OVERRIDES = {
    "aios-ai-workflow": ("subagent-li-ying", "李颖", "AI提效"),
    "auto-show-demo": ("subagent-li-ying", "李颖", "AI提效"),
    "hongqi-8397": ("subagent-zhang-jin", "张劲", "领域驱动"),
    "dongfeng-8397": ("subagent-li-sunan", "李苏南", "超级合作"),
    "dongfeng-4sr": ("subagent-li-sunan", "李苏南", "超级合作"),
    "benteng-e541": ("subagent-li-sunan", "李苏南", "超级合作"),
    "lixiang-game": ("subagent-li-wei", "李玮", "领域驱动"),
    "benz-hmi": ("subagent-yu-zongli", "余宗历", "领域驱动"),
    "gac-audio": ("subagent-han-kangjia", "韩康佳", "领域驱动"),
    "jetour-light": ("subagent-zhang-yunhao", "张云豪", "领域驱动"),
    "design-system-platform": ("subagent-li-wei", "李玮", "领域驱动"),
    "research-figma": ("subagent-gu-yingzhi", "顾颖芝", "领域驱动"),
}

TEAM_BY_AGENT = {
    "subagent-li-ying": "AI提效",
    "subagent-li-sunan": "超级合作",
    "subagent-liu-jinfeng": "超级合作",
    "subagent-chen-ningzi": "超级合作",
    "subagent-li-haoxing": "超级合作",
    "subagent-sun-ruoyi": "超级合作",
    "subagent-du-xinke": "超级合作",
    "master-yangfan": "领域驱动",
    "subagent-yu-zongli": "领域驱动",
    "subagent-han-kangjia": "领域驱动",
    "subagent-gu-yingzhi": "领域驱动",
    "subagent-li-wei": "领域驱动",
    "subagent-zhang-yunhao": "领域驱动",
    "subagent-zhang-jin": "领域驱动",
    "subagent-zhang-fan": "领域驱动",
}


def load_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return fallback


def confidence_from_project(project: dict[str, Any], local_count: int) -> float:
    evidence = project.get("evidence", {})
    total = float(evidence.get("total", 0) or 0)
    source_kinds = sum(1 for key in ("drive_docs", "meetings", "chat_messages", "figma_links") if evidence.get(key, 0))
    confidence = 0.35 + min(total / 350.0, 0.30) + source_kinds * 0.06
    if local_count:
        confidence += 0.08
    return round(min(confidence, 0.92), 2)


def project_risks(project_id: str, evidence: dict[str, Any], local_count: int) -> list[str]:
    risks = []
    if project_id == "hongqi-8397":
        risks.append("Sheet/Base 工时与任务明细未授权")
    if evidence.get("total", 0) >= 80 and local_count == 0:
        risks.append("本地 DCC/导出物证据待接入")
    if evidence.get("figma_links", 0) == 0 and project_id in {"design-system-platform", "research-figma"}:
        risks.append("Figma workspace 证据非全量")
    if evidence.get("total", 0) == 0:
        risks.append("只有手填或弱证据，需确认项目状态")
    return risks


def infer_task_counts(status: str, evidence_total: int, risk_count: int) -> dict[str, int]:
    doing = 1 if evidence_total > 0 else 0
    if evidence_total > 100:
        doing += 2
    elif evidence_total > 40:
        doing += 1
    review = 1 if status in {"review", "blocked"} else 0
    blocked = risk_count if status == "blocked" else min(risk_count, 1)
    done = 1 if status == "done" else 0
    return {"todo": 0 if evidence_total else 1, "doing": doing, "review": review, "blocked": blocked, "done": done}


def source_rows(evidence: dict[str, Any], local_index: dict[str, Any], generated_at: str) -> list[dict[str, Any]]:
    sources = evidence.get("sources", {})
    return [
        {
            "source_id": "feishu_im",
            "name": "飞书群消息",
            "status": "online",
            "count": sources.get("im_messages", {}).get("count", 0),
            "last_sync_at": evidence.get("generated_at"),
            "limitation": "Unity HMI Design 群可见消息",
            "updated_at": generated_at,
        },
        {
            "source_id": "feishu_meetings",
            "name": "飞书会议",
            "status": "online",
            "count": sources.get("vc_meetings", {}).get("count", 0),
            "last_sync_at": evidence.get("generated_at"),
            "limitation": "当前为标题/组织者级，妙记和参会人待展开",
            "updated_at": generated_at,
        },
        {
            "source_id": "feishu_drive",
            "name": "飞书云盘",
            "status": "online",
            "count": sources.get("drive_search_results", {}).get("unique_results", 0),
            "last_sync_at": evidence.get("generated_at"),
            "limitation": "搜索结果级，Sheet/Base 明细未授权",
            "updated_at": generated_at,
        },
        {
            "source_id": "figma",
            "name": "Figma 链接",
            "status": "limited",
            "count": sources.get("figma_links", {}).get("count", 0),
            "last_sync_at": evidence.get("generated_at"),
            "limitation": "仅已发现链接，非 workspace 全量",
            "updated_at": generated_at,
        },
        {
            "source_id": "local_artifacts",
            "name": "本地设计产出物",
            "status": "ready" if local_index.get("count", 0) == 0 else "online",
            "count": local_index.get("count", 0),
            "last_sync_at": local_index.get("generated_at"),
            "limitation": "只扫描显式配置目录",
            "updated_at": generated_at,
        },
        {
            "source_id": "jira",
            "name": "Jira",
            "status": "pending_credentials",
            "count": 0,
            "last_sync_at": None,
            "limitation": "等待站点、token 和项目 key 映射",
            "updated_at": generated_at,
        },
    ]


def build_state() -> dict[str, Any]:
    evidence = load_json(WORKLOAD_EVIDENCE, {})
    local_index = load_json(LOCAL_ARTIFACT_INDEX, {"count": 0, "artifacts": []})
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    snapshot_date = generated_at[:10]

    local_by_project: dict[str, int] = {}
    for artifact in local_index.get("artifacts", []):
        project_id = artifact.get("project_id")
        if project_id:
            local_by_project[project_id] = local_by_project.get(project_id, 0) + 1

    projects = []
    risks = []
    for project in evidence.get("projects", []):
        project_id = project["project_id"]
        evidence_counts = project.get("evidence", {})
        local_count = local_by_project.get(project_id, 0)
        status = PROJECT_STATUS_OVERRIDES.get(project_id, "doing" if evidence_counts.get("total", 0) else "unknown")
        owner_agent, owner_name, team_name = PROJECT_OWNER_OVERRIDES.get(project_id, ("", "", ""))
        risk_labels = project_risks(project_id, evidence_counts, local_count)
        task_counts = infer_task_counts(status, int(evidence_counts.get("total", 0) or 0), len(risk_labels))
        confidence = confidence_from_project(project, local_count)
        project_row = {
            "project_id": project_id,
            "name": project["project_name"],
            "owner_agent": owner_agent,
            "owner_name": owner_name,
            "organization_team": team_name,
            "status": status,
            "evidence_score": evidence_counts.get("total", 0),
            "estimated_effort": None,
            "confidence": confidence,
            "manual_adjustment": 0,
            "local_artifacts": local_count,
            "tasks": task_counts,
            "risks": risk_labels,
            "updated_at": generated_at,
            "snapshot_date": snapshot_date,
        }
        projects.append(project_row)
        for index, label in enumerate(risk_labels, start=1):
            risks.append(
                {
                    "risk_id": f"{project_id}-{index}",
                    "project_id": project_id,
                    "project_name": project["project_name"],
                    "severity": "P0" if "Sheet/Base" in label else "P1",
                    "status": "open",
                    "risk": label,
                    "owner_name": owner_name or "杨帆",
                    "confidence": confidence,
                    "updated_at": generated_at,
                    "snapshot_date": snapshot_date,
                }
            )

    people = []
    for person in evidence.get("people", []):
        agent_id = person.get("agent_id")
        delta = person.get("load_delta_project_count", 0)
        people.append(
            {
                "agent_id": agent_id,
                "name": person.get("name"),
                "organization_team": TEAM_BY_AGENT.get(agent_id, "未分组"),
                "evidence_score": person.get("evidence_score", 0),
                "visible_project_count": person.get("evidence_project_count", 0),
                "manual_project_count": person.get("self_declared_project_count", 0),
                "project_delta": delta,
                "estimated_effort": None,
                "confidence": round(0.45 + min(float(person.get("evidence_score", 0)) / 220.0, 0.35), 2),
                "manual_adjustment": 0,
                "management_note": "待复核主责与支援" if abs(delta) >= 2 else "",
                "updated_at": generated_at,
                "snapshot_date": snapshot_date,
            }
        )

    sources = source_rows(evidence, local_index, generated_at)
    metrics = {
        "project_count": len(projects),
        "people_count": len(people),
        "risk_count": len(risks),
        "open_risk_count": sum(1 for item in risks if item["status"] == "open"),
        "known_evidence_count": sum(item.get("count", 0) or 0 for item in sources if item["source_id"] != "jira"),
        "local_artifact_count": local_index.get("count", 0),
        "blocked_project_count": sum(1 for item in projects if item["status"] == "blocked"),
    }

    return {
        "version": 1,
        "generated_at": generated_at,
        "snapshot_date": snapshot_date,
        "window": "2026-ytd",
        "timezone": "Asia/Shanghai",
        "metrics": metrics,
        "projects": sorted(projects, key=lambda item: item["evidence_score"], reverse=True),
        "people": sorted(people, key=lambda item: item["evidence_score"], reverse=True),
        "sources": sources,
        "risks": risks,
        "excluded_from_current_assignment": ["李达", "张婕"],
        "notes": [
            "evidence_score 衡量可见证据强度，不等于绩效分。",
            "estimated_effort 等待 Jira、Sheet/Base 工时和本地 artifact 接入后校准。",
            "本地 artifact 只来自显式配置目录。",
        ],
    }


def main() -> int:
    state = build_state()
    STATE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    STATE_OUTPUT.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "ok", "output": str(STATE_OUTPUT), "metrics": state["metrics"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
