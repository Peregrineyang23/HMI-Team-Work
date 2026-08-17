# 2026H1 全员自评与最终打分一周行动方案

- release_level: PRIVATE
- start_date: 2026-07-09
- end_date: 2026-07-16
- timezone: Asia/Shanghai
- owner: manager
- goal: By 2026-07-16, every active member has a self-evaluation package, evidence index, calibrated score range, and manager-final score ready for review.

## Team Scope

The active member list is maintained in the manager-side roster and should not be embedded in employee-facing prompts.

Use anonymized working IDs in shared progress tracking:

- `M01` to `M14`: active evaluation cohort.
- `EX01+`: manager-private exclusions or out-of-scope records.
- `DATA_GAP`: member has incomplete evidence package but must still submit v0.

## Success Criteria

By 2026-07-16 18:00:

1. 14 active members each have an evidence index.
2. At least 10 active members have 3+ evidence source categories.
3. All `DATA_GAP` members have at least v0 packages even if raw data remains incomplete.
4. Every member has a score range and a manager-final score.
5. Every A or B+ recommendation has written evidence justification.
6. Every unresolved claim is listed in an evidence gap table.

## Daily Plan

### Day 1: 2026-07-09 Thu

Objective: Distribute unified rules and start v0 extraction.

Actions:

- Send `06-team-message-to-send.md` to all members/agents.
- Send `02-agent-self-evaluation-prompt.md` to every member agent.
- Require each agent to acknowledge:
  - accessible data sources;
  - blocked sources;
  - expected v0 delivery time.
- `DATA_GAP` members must start even with partial data.

Deliverables due:

- Acknowledgement from all active agents.
- Initial source availability list.

### Day 2: 2026-07-10 Fri

Objective: Collect v0 evidence indexes.

Actions:

- Each agent submits `evidence-index.csv` with at least available cloud/local/task evidence.
- Mark each row with S/A/B/C/D grade and confidence.
- Manager checks whether the evidence is project-mapped and desensitized.

Deliverables due:

- v0 evidence index for all members.
- Missing data source list for each member.

### Day 3: 2026-07-11 Sat

Objective: Cross-validate high-impact claims.

Actions:

- For A/B+ candidates, verify:
  - project owner role;
  - final delivery/adoption;
  - issue closure;
  - Figma or local artifact raw evidence;
  - review pass or stakeholder feedback.
- For `DATA_GAP` members, prioritize role/impact evidence first, raw local data second.

Deliverables due:

- Cross-validation notes.
- Claims requiring manager confirmation.

### Day 4: 2026-07-12 Sun

Objective: Generate first scoring range.

Actions:

- Each agent submits:
  - `self_claimed_score`;
  - `evidence_adjusted_range`;
  - `manager_recommended_range`;
  - draft xlsx evaluation table.
- Normalize obvious score inflation.

Deliverables due:

- v1 score range for all active members.
- List of likely A/B+/B/C bands.

### Day 5: 2026-07-13 Mon

Objective: Manager calibration round 1.

Actions:

- Compare all members side by side.
- Check for:
  - same evidence type producing same score effect;
  - score inflation from file counts;
  - under-counted local/Unity/DCC work;
  - unfair penalty from missing data.
- Hold targeted follow-up with members missing critical evidence.

Deliverables due:

- Manager calibration table v1.
- Targeted补证清单.

### Day 6: 2026-07-14 Tue

Objective:补证 and final adjustment.

Actions:

- Agents submit raw exports or additional metadata.
- Manager reviews A/B+ claims and all加分项.
- Any claim without raw evidence is downgraded to medium confidence or moved to gap list.

Deliverables due:

- Evidence index v2.
- Score range v2.

### Day 7: 2026-07-15 Wed

Objective: Final score draft.

Actions:

- Freeze scoring rules.
- Freeze evidence through 2026-07-15 18:00.
- Generate final manager score draft.
- Identify discussion items for final review.

Deliverables due:

- Final draft score for each active member.
- Written rationale for every A / B+ / C or below.

### Day 8: 2026-07-16 Thu

Objective: Final review and close.

Actions:

- Review score table with manager view.
- Confirm final scores.
- Archive evidence package.
- Record unresolved evidence gaps for next cycle.

Deliverables due:

- Final score table.
- Final evidence package.
- Next-cycle evidence improvement checklist.

## Risk Controls

| Risk | Control |
| --- | --- |
| Some member data not ready | Require v0 package by Day 2; use role/impact evidence first; mark gaps. |
| Agents over-score themselves | Require evidence grade, confidence, and manager range. |
| Local file count inflation | Require dedupe and adoption status. |
| Sensitive data leakage | Use redacted path, token-free URLs, no private chat raw text. |
| Inconsistent scoring | Use shared score bands and calibration checklist. |

## Final Meeting Inputs

For each active member:

- One-line role summary.
- Key projects.
- Evidence coverage count.
- Self score.
- Evidence-adjusted range.
- Manager recommended range.
- Final score.
- Open risk or note.
