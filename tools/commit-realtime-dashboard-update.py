#!/usr/bin/env python3
"""Commit and push durable daily dashboard artifacts to the current GitHub branch."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "tmp" / "realtime-tracking" / "dashboard-state.json"
DAILY_ARTIFACTS = [
    "agents/realtime-tracking/emergency-projects.json",
    "agents/realtime-tracking/weekly-report-calibration.md",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=check)


def main() -> int:
    branch = git("branch", "--show-current").stdout.strip()
    if not branch:
        raise SystemExit("Cannot publish dashboard update from detached HEAD")
    if git("remote", "get-url", "origin", check=False).returncode != 0:
        raise SystemExit("Cannot publish dashboard update: origin remote is missing")

    existing = [path for path in DAILY_ARTIFACTS if (ROOT / path).exists()]
    git("add", "--", *existing)
    staged = git("diff", "--cached", "--name-only").stdout.splitlines()
    unexpected = sorted(set(staged) - set(existing))
    if unexpected:
        git("reset", "--", *unexpected)
        raise SystemExit(f"Refusing to commit unexpected staged files: {unexpected}")
    if not staged:
        print(json.dumps({"status": "ok", "git": "no_daily_changes", "branch": branch}, ensure_ascii=False))
        return 0

    state = json.loads(STATE.read_text(encoding="utf-8"))
    version = state.get("dashboard_version", state.get("snapshot_date", "unknown"))
    git("commit", "-m", f"Update realtime dashboard {version}")
    git("push", "-u", "origin", branch)
    commit = git("rev-parse", "--short", "HEAD").stdout.strip()
    print(json.dumps({"status": "ok", "git": "pushed", "branch": branch, "commit": commit, "version": version}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
