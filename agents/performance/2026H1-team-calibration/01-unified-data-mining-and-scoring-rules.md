# 2026H1 统一数据挖掘与打分规则

- release_level: PUBLIC
- version: 0.3
- effective_date: 2026-07-09
- evaluation_period: 2026-01-01 to 2026-06-30
- background_tolerance: 2026-07-01 to 2026-07-07 may be used only as project continuation context, not core H1 scoring.

## 1. Core Principles

1. **证据分不等于绩效分**  
   `evidence_score` measures traceable evidence. `performance_score` is manager-calibrated value based on impact, quality, delivery, responsibility, and role expectation.

2. **同口径优先于高分**  
   Everyone must use the same evidence template, same evidence grading, same scoring dimensions, and same desensitization rules.

3. **本地工作流必须纳入，但不能裸算文件数**  
   Blender, After Effects, Photoshop, 3ds Max, Sketch, Figma, Unity, Jira, local folders, Midjourney, Lovart, and WeChat exports may be evidence sources. File count and folder size can show complexity, but cannot alone prove personal contribution or quality.

4. **自评必须给区间，不只给单点分**  
   Required output: `self_claimed_score`, `evidence_adjusted_range`, `manager_recommended_range`, and `open_risks`.

5. **未准备好数据也要交 v0**  
   Any member with incomplete data should still submit a v0 evidence package first. Missing data should be listed as gaps, not hidden.

## 2. Evaluation Scope

The active evaluation cohort is assigned by the manager or master agent outside this public rulebook.

Employee agents should only evaluate the member explicitly assigned to them.

Do not infer other members' status, score, rank, departure state, or data readiness from this document.

If a member is not assigned to the current evaluation run, the agent should stop and ask the manager for scope confirmation.

## 3. Evidence Grades

| Grade | Name | Definition | Can Support |
| --- | --- | --- | --- |
| S | Direct evidence | Raw, timestamped, person-attributed, project-mapped evidence. | High confidence scoring and A/B+ claims. |
| A | Strong related evidence | Strongly supports participation or responsibility, but needs another source for exact attribution. | Medium-high scoring when cross-validated. |
| B | Auxiliary evidence | Shows workload, complexity, or context. | Scope/complexity explanation, not quality alone. |
| C | Self explanation | Person-provided explanation for hard-to-record work. | Gap notes, cautious wording, manual review. |
| D | Not scoreable | Unattributed, out-of-period, unverifiable, or unrelated evidence. | Background only, no scoring. |

## 4. Confidence Rules

| Confidence | Criteria | Score Use |
| --- | --- | --- |
| High | Raw export or source accessible; person and project resolved; timestamp in period; cross-source consistency. | Can support exact score or A-level claim. |
| Medium-high | Structured evidence exists, but raw source is partial or contribution ratio needs review. | Can support strong claim with cautious wording. |
| Medium | One source plus reasonable inference. | Use as score range, not single-point certainty. |
| Medium-low | Mainly self explanation or process evidence. | Manual review only. |
| Low | Unclear attribution, missing source, or out-of-period. | Do not use for score increase. |

## 5. Required Evidence Sources

Each agent should try to collect at least 3 categories:

| Category | Examples | Required Fields |
| --- | --- | --- |
| Cloud collaboration | Feishu docs, meetings, minutes, group messages, drive files | URL/token, title, timestamp, actor, project, action |
| Online design | Figma/MasterGo/Sketch cloud version history | file key, role, versions, pages/sections/artboards, modified by |
| Local artifacts | `.blend`, `.aep`, `.psd`, `.max`, `.sketch`, `.fbx`, `.mp4`, `.key`, `.pptx` | redacted path, hash, size, created/modified time, project, artifact type |
| Task systems | Jira/Base/Gantt/issues | issue ID, assignee, status transition, close time, priority |
| Git/Unity | commits, branches, tags, changed files | repo, commit hash, author, date, summary |
| AI workflow | prompts, generated assets, scripts, run logs | tool, input/output summary, human adjustment, reuse scope |
| Manual supplement | unrecorded Unity/DCC/debug/onsite work | statement, date range, project, reviewer needed |

## 6. Desensitization Rules

Never include:

- OAuth tokens, API keys, cookies, QR codes, secrets.
- Private phone numbers, private emails, personal IDs.
- Full private chat content unless explicitly approved.
- Customer confidential raw material if it can be replaced by metadata.
- Unredacted local absolute paths when sharing outside the repo.

Use instead:

- `project_id` and `artifact_id`.
- Redacted path such as `<LOCAL_PROJECT_ROOT>/红旗8397/...`.
- Hash prefix, file size, extension, and modified time.
- Message counts and sampled message categories rather than full text.
- Short paraphrase of sensitive feedback instead of raw quote.

## 7. Scoring Dimensions

Use the original evaluation table dimensions:

| Dimension | Weight | Notes |
| --- | ---: | --- |
| UI/UE设计产出与质量 | 50% | Output, quality, consistency, documentation/source handoff. |
| 项目进度与执行力 | 20% | Delivery rhythm, schedule, risk, requirement landing. |
| 设计能力与沉淀、AI工具利用 | 15% | Research, innovation, reusable methods, AI workflow. |
| 团队协作与沟通 | 10% | Cross-role communication, response, team contribution. |
| 工作规范与责任心 | 5% | Process, ownership, attitude, basic reliability. |

## 8. Score Bands

| Band | Range | Required Conditions |
| --- | --- | --- |
| A | 90-100 | Key project owner or platform-level contribution; 3+ evidence categories; strong quality/delivery; no major risk. |
| B+ | 85-89 | Strong multi-project contribution and solid evidence, but platform impact or quality metrics need more proof. |
| B | 75-84 | Stable delivery and collaboration, enough evidence for core duties. |
| C | 60-74 | Delivery exists but evidence, quality, or reliability is incomplete. |
| D | <60 | Core delivery unsupported or major negative evidence. |

## 9. Calibration Rules

1. File count, version count, message count, and meeting count are **signals**, not direct scores.
2. A-level quality claims require review pass, customer/stakeholder feedback, final adoption, low rework, or issue closure evidence.
3. AI efficiency claims require before/after time estimate, reusable workflow, run logs, or adoption by others.
4. Bonus points require evidence beyond normal job responsibility.
5. Deduction requires explicit negative evidence.
6. If raw evidence is incomplete, give a range such as `88-90`, not a false-precision single score.
7. Score and band must be mechanically consistent. A requires final score >= 90; B requires 75-89; C requires 60-74; D is <60. If manager calibration changes the band, keep both `evidence_adjusted_score` and `manager_calibrated_score`.
8. The evidence package must be internally consistent. `evidence-index.csv`, `self-evaluation-summary.md`, `evidence-gaps.md`, and the draft xlsx must not contradict each other about resolved or missing data sources.
9. Manual records and mined metrics must be separated. Worklogs, weekly reports, and self-maintained tables are manual source records; extracted hours, topic clusters, ticket counts, and monthly distributions are mined metrics. Both need confidence labels.
10. Local workflow evidence must be deduped and adoption-aware. Separate source files, autosaves, temporary renders, downloaded assets, shared libraries, final adopted outputs, and reusable tools.
11. AI workflow claims require either adoption evidence or before/after evidence. Code size, script count, or server count can show complexity, but not efficiency impact by itself.
12. Shared file contribution must be role-adjusted. Low edit ratios in large shared files should be treated as participation or context evidence unless ownership or final adoption is confirmed.
13. Bonus items must not duplicate base responsibilities. External praise, business impact, reusable methodology, or major initiative claims require written, raw, or manager-confirmed impact evidence.

## 10. Minimum Output Standard

Each agent must produce:

- Evidence index with at least 15 high/medium evidence rows if available.
- Evidence summary grouped by project and scoring dimension.
- Recommended score range.
- Claims requiring manager confirmation.
- Excluded or out-of-period evidence list.
