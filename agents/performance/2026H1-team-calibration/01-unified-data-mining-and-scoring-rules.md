# 2026H1 统一数据挖掘与打分规则

- release_level: PUBLIC
- version: 0.7
- status: FINAL
- effective_date: 2026-07-14
- frozen_at: 2026-07-18
- clarified_at: 2026-07-24
- clarification: V07-C01 external manager aggregate rating evidence boundary
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
| Cloud collaboration | Feishu docs, meetings, minutes, group messages, drive files, reactions, comments, explicit approvals | URL/token, title, timestamp, actor, project, action |
| Online design | Figma/MasterGo/Sketch cloud version history, comments, reactions, approvals | file key, role, versions, pages/sections/artboards, modified by |
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
- Redacted path such as `<LOCAL_PROJECT_ROOT>/<PROJECT_ALIAS>/...`.
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
14. Positive recognition signals must be weighted by source authority and content clarity. Likes/reactions are weaker than written approval; written customer approval and explicit manager approval are high-confidence evidence.
15. "One-pass approval" must include a review or delivery record showing the work was accepted without material rework. A self-claimed "one-pass" statement is C-level until cross-validated.
16. Manager or master-agent replies count as high-confidence signals only when the reply clearly confirms quality, adoption, prioritization, or business value. Generic acknowledgements such as "收到", "辛苦了", or emoji-only reactions are collaboration signals, not quality proof.
17. Recognition evidence can raise confidence or unlock the upper end of a score range, but it must still map to the relevant scoring dimension. It should not create duplicate bonus if the same impact is already counted in the base score.
18. Evidence confidence is capped by the weakest required link. If a claim depends on a customer/manager message but the raw message cannot be reviewed, the claim is at most A / medium-high even when a local artifact confirms delivery.
19. Evidence grade is based on accessible verification, not the wording of the title. Labels such as "customer approved", "director recognized", or "one-pass" do not make an item S-grade by themselves.
20. Period boundaries must be applied to the underlying activity, not only the current file. A design file inspected after the period must separate in-period versions, pages, tasks, and adopted outputs from post-period additions.
21. Current node count, file size, or page count may describe current complexity. It cannot be backdated to H1 unless an H1 snapshot, version, export, or timestamped artifact proves that state existed during the period.
22. Platform assets, design systems, methods, scripts, and workflows receive extra-impact credit only when reuse, adoption, governance ownership, or measurable project use is verified. Creation alone remains base contribution evidence.
23. Coordination and leadership are outcome-scored. Group count, meeting count, message count, assignment count, and attendance are scope signals; higher scores require decisions, owner assignment, risk closure, delivery acceptance, or cross-team adoption.
24. Bonus rows must match the named bonus category and include a non-duplication explanation. A methodology claim cannot be placed under external award/praise, and the same impact cannot be counted in quality, innovation, sharing, and bonus without separating the incremental value.
25. Final totals and bands must be formula-driven or mechanically reconciled from item scores, bonus, and deductions. A narrative recommendation cannot override an inconsistent arithmetic total.
26. A written aggregate score from an onsite manager, customer-side manager, or long-term external supervisor is authoritative evidence of that evaluator's judgment, but not automatically direct evidence of each underlying performance fact. Without project, role, deliverable, acceptance, or impact details, it is medium-high confidence for bounded calibration and cannot alone unlock A band or high bonus.
27. Only subitems explicitly supported by the evaluator's wording may be adjusted. A high aggregate rating must not automatically raise unmentioned AI efficiency, research, design-system, documentation, or team-reuse subitems.
28. Before an aggregate external rating supports A band or high bonus, cross-validate at least 2-3 representative project facts with personal role, attributable action, acceptance/adoption/impact, and a reviewable source.

## 10. Recognition Evidence Weighting

Use this table when weighting Figma, Feishu, Feishu Docs, customer, and manager feedback.

| Recognition Evidence | Evidence Grade | Confidence | Suggested Score Use |
| --- | --- | --- | --- |
| Customer written approval, acceptance, sign-off, or explicit positive feedback tied to a deliverable | S | high | Can support A-level quality, adoption, bonus, or upward manager calibration. |
| Manager/master-agent explicit written confirmation of quality, adoption, key contribution, or business value | S | high | Can unlock the upper end of `manager_recommended_range`; can support bonus if impact exceeds base duty. |
| Verified "one-pass approval" with review/delivery record and no material rework | S/A | high or medium-high | Strong support for quality, execution, and responsibility dimensions. |
| Figma/MasterGo/Feishu Doc comment that requests only minor polish or confirms direction is correct | A | medium-high | Supports quality and feedback-response score, but does not alone prove final adoption. |
| Feishu/Figma/Doc likes or reactions from manager, PM, customer, or cross-functional stakeholder | A/B | medium-high or medium | Positive recognition signal; raises confidence when tied to a specific deliverable. Reaction count alone is not quality proof. |
| Likes/reactions from peers without written context | B | medium | Supports collaboration morale or visibility only; do not use for A-level quality by itself. |
| Generic acknowledgement such as "OK", "收到", "辛苦了", or emoji-only reaction | B/C | medium-low | Process/collaboration signal only unless paired with other adoption evidence. |
| Self-claimed praise or unverified verbal praise | C | medium-low | Gap note or manual review only. |

Recognition evidence should be captured in `evidence-index.csv` with `source_type` values such as `figma_comment`, `figma_reaction`, `feishu_reaction`, `feishu_doc_comment`, `customer_feedback`, `manager_reply`, or `one_pass_approval`.

## 11. Role-Calibrated Evidence

The five primary dimensions and weights remain the same for every member. Role calibration changes acceptable evidence, not the total weight.

| Contribution Pattern | Strong Evidence | Evidence That Is Only A Signal |
| --- | --- | --- |
| Project owner / delivery owner | accepted milestone, risk closure, requirement decisions, final handoff, stakeholder confirmation | project count, file count, meeting attendance |
| Specialist / design contributor | attributable adopted output, review quality, low rework, source handoff, implementation fidelity | version count, node count, artifact size |
| Coordinator / team organizer | decision record, clear assignment, dependency closure, reduced rework, delivery recovery | group count, message count, calendar count |
| Platform / method builder | reuse by another person or project, governance ownership, documented workflow, measurable project use | framework existence, code size, page count |
| AI workflow builder | adopted workflow, before/after effort, run log, repeatability, other-user reuse | tool count, prompt count, server count |

Role calibration must not lower a support or coordination role merely because it produces fewer design files. It must also not raise a platform claim without adoption evidence.

## 12. Short-Tenure Normalization

Employees with less than a full evaluation period must be evaluated against responsibilities and delivery targets prorated to their actual active period.

1. Do not multiply the whole performance score by `months_employed / 6`. Quality, acceptance, collaboration, responsibility, and role performance remain fully scoreable within the observed period.
2. Output volume, project count, task count, and meeting count must be normalized by active months before comparing with full-period employees.
3. Record `active_period`, `tenure_coverage`, and `normalization_note` in the private manager calibration sheet.
4. Half-year cumulative contribution may report tenure coverage separately, but it must not replace the performance score.
5. For less than three months of evidence, A/B+ claims require stronger attribution and acceptance because the observation window is short.
6. Short-tenure bonus requires an attributable accepted result on a manager-designated priority project. Learning activity, inherited files, or normal onboarding work is not bonus evidence.

## 13. Strategic Project Priority For Bonus Review

Manager-designated project priority for the current review. The private project-to-priority mapping is maintained outside this public rulebook.

| Priority | Project | Bonus Review Order |
| --- | --- | --- |
| P0 | Manager-designated highest-priority project | Highest |
| P1 | Manager-designated high-priority project | High |
| P2 | Manager-designated medium-high-priority project | Medium-high |
| P3 | Other projects | Standard unless separately designated |

Project priority affects the order and strength of bonus review, not the five primary dimension weights.

1. A high-priority project does not automatically grant bonus points.
2. Bonus evidence must state project priority, personal role, incremental value beyond base duty, acceptance/result, and non-duplication rationale.
3. When one outcome appears in multiple projects or bonus categories, count it once using the highest applicable project priority.
4. The bonus and deduction sections of the workbook must include an `评价依据` column. A numeric adjustment without a written basis is incomplete.
5. Zero bonus or deduction rows should state why the threshold was not triggered when the manager has reviewed that category.

## 14. Minimum Output Standard

Each agent must produce:

- Evidence index with at least 15 high/medium evidence rows if available.
- Evidence summary grouped by project and scoring dimension.
- Recommended score range.
- Claims requiring manager confirmation.
- Excluded or out-of-period evidence list.
