# 2026H1 Team Performance Calibration Pack

- release_level: PRIVATE
- version: 0.3
- created_at: 2026-07-09
- timezone: Asia/Shanghai
- owner: manager
- purpose: Provide a unified, desensitized, evidence-based self-evaluation and scoring workflow for all Unity HMI Design subagents.

## Release Classification

| File | Release Level | Audience | Notes |
| --- | --- | --- | --- |
| `01-unified-data-mining-and-scoring-rules.md` | PUBLIC | Employee agents | Share as the common scoring and evidence rulebook. |
| `02-agent-self-evaluation-prompt.md` | PUBLIC | Employee agents | Send one-to-one after replacing placeholders for that member only. |
| `03-desensitized-evidence-index-template.csv` | PUBLIC | Employee agents | Shared evidence index schema. |
| `06-team-message-to-send.md` | PUBLIC | Team chat or employee agents | Team-wide task message with no individual scoring context. |
| `04-one-week-action-plan.md` | PRIVATE | Manager / master agent | Contains execution controls and should not be sent as the primary agent prompt. |
| `05-manager-final-calibration-checklist.md` | PRIVATE | Manager / master agent | Final scoring and calibration checklist. |
| `README.md` | PRIVATE | Manager / master agent | This index explains release boundaries. |
| `performance-score-model-v0.3.yml` | PRIVATE | Manager / master agent / tooling | Machine-readable model manifest. |

## Deliverables

| File | Purpose |
| --- | --- |
| `01-unified-data-mining-and-scoring-rules.md` | Unified data mining, desensitization, evidence grading, and scoring rules. |
| `02-agent-self-evaluation-prompt.md` | Prompt to send to every member's agent today. |
| `03-desensitized-evidence-index-template.csv` | Evidence index template that every agent must fill. |
| `04-one-week-action-plan.md` | July 9 to July 16 execution plan, checkpoints, owners, and outputs. |
| `05-manager-final-calibration-checklist.md` | Final manager review checklist for score calibration. |
| `06-team-message-to-send.md` | Short team-facing message for distributing the task. |

## Current Constraints

- Some member data packages are not ready yet. They should still follow the same workflow and submit a v0 evidence index first.
- Primary calibration scope is controlled by the manager-side roster and must not be inferred by employee agents.
- Departure, exclusion, and special-case handling must stay in manager-private materials.
- Current model v0.2 is evidence-visible scoring, not final performance scoring.

## Required Output From Every Active Member Agent

1. `evidence-index.csv` using the shared template.
2. `self-evaluation-summary.md`.
3. Filled or draft `2026H1半年度评价表_<member_alias>.xlsx`.
4. `evidence-gaps.md` listing missing raw exports, inaccessible files, and claims needing manager confirmation.
5. Suggested score range, not only a single score.
