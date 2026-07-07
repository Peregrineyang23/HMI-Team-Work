#!/usr/bin/env python3
"""Index explicitly configured local design artifacts for realtime tracking.

The scanner is intentionally conservative: it does not scan any directory unless
the directory is enabled in data-sources.yml or passed with --root.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES = ROOT / "agents" / "realtime-tracking" / "data-sources.yml"
DEFAULT_PROJECT_MAP = ROOT / "agents" / "realtime-tracking" / "project-map.yml"
DEFAULT_ROSTER = ROOT / "agents" / "team-roster.yml"
DEFAULT_JSON = ROOT / "tmp" / "local-artifact-index.json"
DEFAULT_CSV = ROOT / "tmp" / "local-artifact-index.csv"

EXCLUDED_NAMES = {"张婕", "李达"}
DEFAULT_EXTENSIONS = {
    ".blend",
    ".max",
    ".ma",
    ".mb",
    ".aep",
    ".psd",
    ".psb",
    ".sketch",
    ".fig",
    ".ai",
    ".fbx",
    ".obj",
    ".glb",
    ".gltf",
    ".unity",
    ".prefab",
    ".png",
    ".jpg",
    ".jpeg",
    ".mp4",
    ".mov",
    ".json",
    ".csv",
    ".xlsx",
    ".pdf",
}
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".Trash",
    "__pycache__",
    "node_modules",
    "Library",
    "Temp",
    "DerivedData",
}

BUILTIN_PROJECTS = [
    {
        "project_id": "aios-ai-workflow",
        "name": "AIOS / AI Workflow / AI Worker",
        "terms": ["AIOS", "AI Workflow", "AI Worker", "AI桌面", "fufu", "AI Agent", "智能机器人"],
    },
    {
        "project_id": "auto-show-demo",
        "name": "2026车展DEMO",
        "terms": ["2026车展DEMO", "车展DEMO", "车展", "Demo01", "HMI Demo"],
    },
    {
        "project_id": "hongqi-8397",
        "name": "红旗8397",
        "terms": ["红旗8397", "一汽红旗", "红旗", "8397内部例会", "金葵花", "HQ8397"],
    },
    {
        "project_id": "dongfeng-8397",
        "name": "东风8397",
        "terms": ["东风8397", "东风xUnity", "东风+Unity", "东风 POC", "DF8397"],
    },
    {
        "project_id": "dongfeng-4sr",
        "name": "东风4SR / 8295 4SR",
        "terms": ["东风4SR", "8295 4SR", "4SR项目", "东风8295", "DF4SR"],
    },
    {
        "project_id": "benteng-e541",
        "name": "奔腾E541 / 奔腾实验室",
        "terms": ["奔腾E541", "E541", "奔腾实验室", "奔腾", "Benteng"],
    },
    {
        "project_id": "lixiang-game",
        "name": "理想游戏上车",
        "terms": ["理想游戏", "理想游戏上车", "饥饿鲨", "车载游戏", "GameStore"],
    },
    {
        "project_id": "benz-hmi",
        "name": "奔驰HMI",
        "terms": ["奔驰HMI", "奔驰", "Benz HMI", "Mercedes HMI"],
    },
    {
        "project_id": "gac-audio",
        "name": "广汽音频可视化",
        "terms": ["广汽音频可视化", "广汽本田音乐可视化", "广汽音频", "AudioViz"],
    },
    {
        "project_id": "jetour-light",
        "name": "捷途灯语",
        "terms": ["捷途灯语", "捷途", "JetourLight"],
    },
    {
        "project_id": "design-system-platform",
        "name": "设计系统 / 动效平台化",
        "terms": ["设计系统", "动效平台化", "UI kit", "Design System", "MotionLibrary", "3DAssets"],
    },
    {
        "project_id": "research-figma",
        "name": "Figma / 创意研究画板",
        "terms": ["Figma", "FigJam", "创意研究画板", "GVDP", "Research", "创意研究"],
    },
]


@dataclass
class WatchRoot:
    root_id: str
    path: Path
    enabled: bool = True
    owner_agent: str | None = None
    owner_name: str | None = None
    file_extensions: set[str] = field(default_factory=lambda: set(DEFAULT_EXTENSIONS))
    exclude_dirs: set[str] = field(default_factory=lambda: set(DEFAULT_EXCLUDE_DIRS))


def iso_from_timestamp(value: float) -> str:
    return datetime.fromtimestamp(value, timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_short(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:20]


def normalize_ext(ext: str) -> str:
    ext = ext.strip()
    if not ext:
        return ext
    return ext.lower() if ext.startswith(".") else f".{ext.lower()}"


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "~", ""}:
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        raw_items = value[1:-1].strip()
        if not raw_items:
            return []
        return [item.strip().strip("\"'") for item in raw_items.split(",")]
    return value.strip("\"'")


def load_yaml_if_available(path: Path) -> Any | None:
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_watch_roots_fallback(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    roots: list[dict[str, Any]] = []
    in_local = False
    in_watch = False
    current: dict[str, Any] | None = None
    current_list: str | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        if indent == 2 and stripped == "local_artifacts:":
            in_local = True
            in_watch = False
            continue
        if in_local and indent == 2 and stripped.endswith(":") and stripped != "local_artifacts:":
            break
        if in_local and indent == 4 and stripped == "watch_roots:":
            in_watch = True
            continue
        if not in_watch:
            continue

        if indent == 6 and stripped.startswith("- id:"):
            if current:
                roots.append(current)
            current = {"id": parse_scalar(stripped.split(":", 1)[1]), "file_extensions": [], "exclude_dirs": []}
            current_list = None
            continue

        if current is None:
            continue

        if indent == 8 and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                current[key] = parse_scalar(value)
                current_list = None
            else:
                current.setdefault(key, [])
                current_list = key
            continue

        if current_list and indent >= 10 and stripped.startswith("- "):
            current.setdefault(current_list, []).append(parse_scalar(stripped[2:]))

    if current:
        roots.append(current)
    return roots


def load_watch_roots(sources_path: Path, cli_roots: list[str]) -> list[WatchRoot]:
    raw_roots: list[dict[str, Any]] = []
    config = load_yaml_if_available(sources_path)
    if config:
        raw_roots = (
            config.get("sources", {})
            .get("local_artifacts", {})
            .get("watch_roots", [])
        )
    else:
        raw_roots = parse_watch_roots_fallback(sources_path)

    roots: list[WatchRoot] = []
    for raw in raw_roots:
        if not raw.get("enabled"):
            continue
        root_path = raw.get("root_path")
        if not root_path:
            continue
        roots.append(
            WatchRoot(
                root_id=str(raw.get("id") or Path(str(root_path)).name),
                path=Path(str(root_path)).expanduser().resolve(),
                enabled=True,
                owner_agent=raw.get("owner_agent"),
                owner_name=raw.get("owner_name"),
                file_extensions={normalize_ext(str(ext)) for ext in raw.get("file_extensions", [])} or set(DEFAULT_EXTENSIONS),
                exclude_dirs=set(raw.get("exclude_dirs", [])) | set(DEFAULT_EXCLUDE_DIRS),
            )
        )

    for index, root in enumerate(cli_roots, start=1):
        roots.append(
            WatchRoot(
                root_id=f"cli-root-{index}",
                path=Path(root).expanduser().resolve(),
                enabled=True,
            )
        )

    return roots


def parse_project_map_fallback(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return BUILTIN_PROJECTS

    projects: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_projects = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        if indent == 0 and stripped == "projects:":
            in_projects = True
            continue
        if not in_projects:
            continue
        if indent == 2 and stripped.startswith("- project_id:"):
            if current:
                projects.append(current)
            current = {"project_id": parse_scalar(stripped.split(":", 1)[1]), "name": "", "terms": []}
            continue
        if current is None:
            continue
        if indent == 4 and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "name":
                current["name"] = parse_scalar(value)
            elif key in {"aliases", "keywords", "local_path_hints", "jira_project_keys"}:
                current["terms"].extend(parse_scalar(value) or [])
    return projects or BUILTIN_PROJECTS


def load_projects(project_map_path: Path) -> list[dict[str, Any]]:
    config = load_yaml_if_available(project_map_path)
    if config:
        projects = []
        for raw in config.get("projects", []):
            terms = []
            for key in ("aliases", "keywords", "local_path_hints", "jira_project_keys"):
                terms.extend(raw.get(key) or [])
            projects.append({"project_id": raw["project_id"], "name": raw["name"], "terms": [str(term) for term in terms]})
        return projects or BUILTIN_PROJECTS
    return parse_project_map_fallback(project_map_path)


def load_people(roster_path: Path) -> list[dict[str, str]]:
    config = load_yaml_if_available(roster_path)
    if config:
        people = []
        for raw in [config.get("lead_agent", {})] + config.get("subagents", []):
            name = raw.get("name")
            if not name or name in EXCLUDED_NAMES:
                continue
            people.append({"agent_id": raw.get("id", ""), "name": name})
        return people

    people: list[dict[str, str]] = []
    current_id = ""
    for raw in roster_path.read_text(encoding="utf-8").splitlines() if roster_path.exists() else []:
        stripped = raw.strip()
        if stripped.startswith("- id:") or stripped.startswith("id:"):
            current_id = str(parse_scalar(stripped.split(":", 1)[1]) or "")
        elif stripped.startswith("name:"):
            name = str(parse_scalar(stripped.split(":", 1)[1]) or "")
            if name and name not in EXCLUDED_NAMES:
                people.append({"agent_id": current_id, "name": name})
    return people


def infer_tool(extension: str) -> str:
    return {
        ".blend": "Blender",
        ".max": "3ds Max",
        ".ma": "Maya",
        ".mb": "Maya",
        ".aep": "After Effects",
        ".psd": "Photoshop",
        ".psb": "Photoshop",
        ".sketch": "Sketch",
        ".fig": "Figma export",
        ".ai": "Illustrator",
        ".unity": "Unity",
        ".prefab": "Unity",
        ".fbx": "DCC interchange",
        ".obj": "DCC interchange",
        ".glb": "DCC interchange",
        ".gltf": "DCC interchange",
        ".mp4": "Video export",
        ".mov": "Video export",
    }.get(extension, "unknown")


def infer_artifact_type(path: Path, extension: str) -> str:
    text = "/".join(part.lower() for part in path.parts)
    if any(marker in text for marker in ("delivery", "deliver", "final", "交付")):
        return "delivery"
    if any(marker in text for marker in ("export", "render", "review", "导出", "渲染", "评审")):
        return "render_export"
    if extension in {".blend", ".max", ".ma", ".mb", ".aep", ".psd", ".psb", ".sketch", ".ai", ".unity", ".prefab"}:
        return "source_asset"
    if extension in {".mp4", ".mov", ".png", ".jpg", ".jpeg", ".pdf"}:
        return "render_export"
    return "unknown"


def match_terms(text: str, projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lowered = text.lower()
    matches = []
    for project in projects:
        hit_terms = []
        for term in project.get("terms", []):
            term_text = str(term).strip()
            if term_text and term_text.lower() in lowered:
                hit_terms.append(term_text)
        if hit_terms:
            confidence = min(0.95, 0.45 + 0.12 * len(hit_terms))
            matches.append(
                {
                    "project_id": project["project_id"],
                    "name": project["name"],
                    "confidence": round(confidence, 2),
                    "matched_terms": hit_terms[:6],
                }
            )
    return sorted(matches, key=lambda item: item["confidence"], reverse=True)


def match_people(text: str, people: list[dict[str, str]], owner_name: str | None = None) -> list[dict[str, Any]]:
    matches = []
    lowered = text.lower()
    for person in people:
        name = person["name"]
        if owner_name and owner_name == name:
            matches.append({"agent_id": person["agent_id"], "name": name, "confidence": 0.85, "source": "configured_owner"})
        elif name and name.lower() in lowered:
            matches.append({"agent_id": person["agent_id"], "name": name, "confidence": 0.55, "source": "path_or_filename"})
    unique: dict[str, dict[str, Any]] = {}
    for match in matches:
        existing = unique.get(match["agent_id"])
        if not existing or existing["confidence"] < match["confidence"]:
            unique[match["agent_id"]] = match
    return sorted(unique.values(), key=lambda item: item["confidence"], reverse=True)


def score_artifact(artifact_type: str, project_matches: list[dict[str, Any]], person_matches: list[dict[str, Any]]) -> tuple[float, float]:
    base = {
        "source_asset": 2.5,
        "render_export": 2.0,
        "delivery": 3.0,
        "unknown": 1.0,
    }.get(artifact_type, 1.0)
    project_conf = project_matches[0]["confidence"] if project_matches else 0.25
    person_conf = person_matches[0]["confidence"] if person_matches else 0.25
    confidence = round((project_conf * 0.65) + (person_conf * 0.25) + 0.10, 2)
    return round(base * confidence, 2), min(confidence, 0.95)


def iter_artifacts(root: WatchRoot, projects: list[dict[str, Any]], people: list[dict[str, str]], max_files: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not root.path.exists() or not root.path.is_dir():
        return rows

    for current_dir, dirnames, filenames in os.walk(root.path):
        dirnames[:] = [
            name
            for name in dirnames
            if name not in root.exclude_dirs and not name.startswith(".")
        ]

        for filename in filenames:
            if len(rows) >= max_files:
                return rows
            if filename.startswith("."):
                continue
            path = Path(current_dir) / filename
            extension = normalize_ext(path.suffix)
            if extension not in root.file_extensions:
                continue
            try:
                stat = path.stat()
            except OSError:
                continue

            rel_path = path.relative_to(root.path)
            match_text = f"{rel_path} {root.path.name}"
            project_matches = match_terms(match_text, projects)
            person_matches = match_people(match_text, people, owner_name=root.owner_name)
            artifact_type = infer_artifact_type(path, extension)
            evidence_score, confidence = score_artifact(artifact_type, project_matches, person_matches)
            modified_at = iso_from_timestamp(stat.st_mtime)
            absolute_path = str(path.resolve())
            artifact_id = sha256_short(f"{absolute_path}|{stat.st_mtime_ns}|{stat.st_size}")

            rows.append(
                {
                    "artifact_id": artifact_id,
                    "source_id": root.root_id,
                    "source_system": "local",
                    "artifact_type": artifact_type,
                    "title": path.name,
                    "absolute_path": absolute_path,
                    "relative_path": str(rel_path),
                    "extension": extension,
                    "tool_hint": infer_tool(extension),
                    "size_bytes": stat.st_size,
                    "modified_at": modified_at,
                    "project_id": project_matches[0]["project_id"] if project_matches else None,
                    "project_name": project_matches[0]["name"] if project_matches else None,
                    "project_confidence": project_matches[0]["confidence"] if project_matches else 0.0,
                    "person_agent_id": person_matches[0]["agent_id"] if person_matches else root.owner_agent,
                    "person_name": person_matches[0]["name"] if person_matches else root.owner_name,
                    "person_confidence": person_matches[0]["confidence"] if person_matches else (0.85 if root.owner_agent else 0.0),
                    "evidence_score": evidence_score,
                    "confidence": confidence,
                    "project_candidates": project_matches[:3],
                    "person_candidates": person_matches[:3],
                    "dedupe_key": sha256_short(f"local|{absolute_path}"),
                }
            )
    return rows


def write_outputs(rows: list[dict[str, Any]], json_path: Path, csv_path: Path, roots: list[WatchRoot]) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "version": 1,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "scanner": "tools/scan-local-artifacts.py",
        "mode": "explicit_roots_only",
        "roots": [
            {"id": root.root_id, "path": str(root.path), "exists": root.path.exists()}
            for root in roots
        ],
        "count": len(rows),
        "artifacts": rows,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    fieldnames = [
        "artifact_id",
        "source_id",
        "artifact_type",
        "title",
        "absolute_path",
        "relative_path",
        "extension",
        "tool_hint",
        "size_bytes",
        "modified_at",
        "project_id",
        "project_name",
        "project_confidence",
        "person_agent_id",
        "person_name",
        "person_confidence",
        "evidence_score",
        "confidence",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan explicitly configured local design artifact directories.")
    parser.add_argument("--sources-config", default=str(DEFAULT_SOURCES), help="Path to realtime data-sources.yml.")
    parser.add_argument("--project-map", default=str(DEFAULT_PROJECT_MAP), help="Path to project-map.yml.")
    parser.add_argument("--roster", default=str(DEFAULT_ROSTER), help="Path to team-roster.yml.")
    parser.add_argument("--root", action="append", default=[], help="Explicit extra root to scan. Can be repeated.")
    parser.add_argument("--json-output", default=str(DEFAULT_JSON), help="JSON output path.")
    parser.add_argument("--csv-output", default=str(DEFAULT_CSV), help="CSV output path.")
    parser.add_argument("--max-files", type=int, default=20000, help="Maximum files to index per run.")
    args = parser.parse_args()

    roots = load_watch_roots(Path(args.sources_config), args.root)
    projects = load_projects(Path(args.project_map))
    people = load_people(Path(args.roster))

    rows: list[dict[str, Any]] = []
    for root in roots:
        rows.extend(iter_artifacts(root, projects, people, args.max_files - len(rows)))
        if len(rows) >= args.max_files:
            break

    rows.sort(key=lambda item: item["modified_at"], reverse=True)
    write_outputs(rows, Path(args.json_output), Path(args.csv_output), roots)

    print(
        json.dumps(
            {
                "status": "ok",
                "roots": len(roots),
                "artifacts": len(rows),
                "json_output": str(Path(args.json_output)),
                "csv_output": str(Path(args.csv_output)),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
