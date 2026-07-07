# Teamwork HMI Design

This repository contains the coordination setup for the Unity HMI Design team.

The current structure establishes 杨帆 as the master agent and every other member of the Feishu group `Unity HMI Design` as a subagent. The files under `agents/` are intended to support requirement distribution, feedback collection, and future integration with each member's personal AI worker.

Start with:

- `AGENTS.md` for the project-level agent contract.
- `agents/team-roster.yml` for team, Feishu, and future AI-worker routing data.
- `agents/domain-formation.yml` for DDD domain formation ownership and member role binding.
- `agents/organization-teams.yml` for the 2026 three-team organization model.
- `agents/project-assignments.yml` for project assignment and workload signals.
- `agents/workload-analysis.md` for the current project workload analysis.
- `agents/team-organization.html` for a local visual organization chart.
- `agents/analysis/workload-analysis-2026.md` for 2026 project workload and contribution analysis.
- `agents/analysis/workload-dashboard-2026.html` for the 2026 workload analysis dashboard.
- `agents/realtime-tracking/` for realtime design evidence collection, project mapping, and task dashboard specs.
- `agents/realtime-tracking/realtime-task-dashboard.html` for the first realtime task tracking dashboard prototype.
- `tools/scan-local-artifacts.py` for indexing explicitly configured local design artifact folders.
- `agents/protocol.md` for the dispatch and feedback workflow.
- `agents/subagents/` for per-person subagent profiles.
