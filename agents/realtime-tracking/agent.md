# Unity HMI Realtime Task Tracking Agent

- owner: 杨帆 / `master-yangfan`
- lead_open_id: `ou_ab5cf61968f074140a3e2d73d8035a9c`
- generated_at: 2026-07-09
- timezone: Asia/Shanghai
- status: ready_daily_sync

## Mission

This agent maintains the Unity HMI Design realtime task tracking board. It turns observable design work signals into project, person, source, and risk records for daily task distribution and resource scheduling.

The board is not a performance scorecard. `evidence_score` means visible and traceable evidence strength. `estimated_effort`, `confidence`, and `manual_adjustment` must stay separate.

## Live Feishu Assets

- Base: https://yousandi.feishu.cn/base/QIFybHOSUaU7HUsQ1h8c2eV5nY8
- Dashboard ID: `blkxBQFl6g0CY98j`
- Tables:
  - 项目状态: `tblHtagrKpugt785`, current view `vewBPGl4VN`
  - 人员负载: `tbljfV3gqqpsiMw8`, current view `vewDjF0S89`
  - 数据源健康: `tbl92nK2MQ38006b`, current view `vewEUoEWkJ`
  - 风险队列: `tblm6RaQqz0WG3KD`, current view `vew8X0H0kj`
  - 每日变化: `tbllhgJMAk2VgG4l`
- Team access: DM006. Realtime Task Management, `oc_824642a195aa4a6d1fd2861fd8c749da`, view permission
- Daily automation: Codex automation `unity-hmi`, active, 09:00 Asia/Shanghai

## Current Effective State

After the 2026-07-09 update:

- Current projects: 13
- Current people rows: 14
- Current data sources: 8
- Current open risks: 20
- Local artifact count: 0, because only explicitly configured directories are scanned

The newly added emergency project is `benteng-e541-report-video` / 奔腾E541 汇报视频, sourced from Feishu chat `oc_2180b75fd1f5927dad6aa74e15724d8d`.

## Data Sources

Primary sources currently wired:

- Feishu group messages from visible chats
- Feishu meetings and cloud-drive search evidence from prior 2026 analysis
- Manual weekly report Base: `YUfJbhnHgawr7Wsp0UocNTqznte`, table `tbln0vm1ywBtaeeF`
- Emergency project declarations in `agents/realtime-tracking/emergency-projects.json`
- Local artifact scanner, constrained to explicitly configured directories
- Figma links currently discovered through existing evidence only
- Jira placeholder, pending credentials and project key mapping

Manual weekly report calibration excludes 张婕 and 李达. They must not be assigned new work.

## Daily Runbook

Run this chain for a manual refresh:

```bash
python3 tools/scan-local-artifacts.py
python3 tools/generate-realtime-dashboard-state.py
python3 tools/calibrate-realtime-dashboard-from-weekly-report.py
python3 tools/sync-lark-dashboard.py --sync
python3 tools/sync-lark-dashboard.py --dedupe
```

The automation runs the same logical chain daily. If Base sync is blocked, use the DM006 digest fallback:

```bash
python3 tools/send-lark-dashboard-digest.py --send
```

Never send fallback updates to the Unity HMI Design source group.

## Permissions Policy

Never request standalone delete scopes.

Approved non-delete scopes include Base app/table/field/record/dashboard read-create-update, `base:view:write_only`, and `docs:permission.member:create` for sharing the Base with DM006.

The sync strategy preserves historical duplicate rows by marking them:

- `同步状态=current`: visible in current views and dashboard charts
- `同步状态=superseded`: retained for audit, excluded from current views

## File Map

- `agents/realtime-tracking/lark-dashboard.json`: live Base IDs, table IDs, view IDs, automation commands
- `agents/realtime-tracking/lark-dashboard.yml`: human-readable equivalent config
- `agents/realtime-tracking/project-map.yml`: project aliases, source tokens, path hints
- `agents/realtime-tracking/evidence-schema.yml`: evidence schema and scoring separation
- `agents/realtime-tracking/emergency-projects.json`: durable emergency project feed
- `agents/realtime-tracking/weekly-report-calibration.md`: latest manual weekly report calibration summary
- `tools/generate-realtime-dashboard-state.py`: builds dashboard state JSON
- `tools/calibrate-realtime-dashboard-from-weekly-report.py`: folds manual weekly report Base into dashboard state
- `tools/sync-lark-dashboard.py`: creates/syncs Base, grants team access, marks superseded duplicates
- `tools/scan-local-artifacts.py`: local DCC/export artifact scan framework
- `tools/send-lark-dashboard-digest.py`: DM006 fallback digest sender

## Emergency Project Intake

When a new urgent Feishu chat should become a tracked project:

1. Read chat metadata and same-day messages using `lark-cli im`.
2. Summarize project name, owner, collaborators, deliverables, risks, and evidence refs.
3. Add a durable entry to `agents/realtime-tracking/emergency-projects.json`.
4. Add project aliases and source token to `agents/realtime-tracking/project-map.yml`.
5. Regenerate and sync the board.
6. Verify the project row, risks, and data source in Feishu Base.

## Guardrails

- Do not assign new work to 张婕 or 李达.
- Do not scan private local directories unless explicitly configured.
- Do not treat visible evidence as true effort or performance.
- Do not delete Base records to resolve duplication; mark them as superseded.
- Keep DM006. Realtime Task Management as the target team channel for this board.
