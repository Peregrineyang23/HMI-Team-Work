# 2026H1 余宗历自评数据包校验与评分审计

- release_level: PRIVATE
- audit_date: 2026-07-10
- source_folder: `/Users/frankyang/my_work/My_Team/2026 Mid-year review/xlsx/余宗历/yuzongli-v0`
- source_files:
  - `2026H1半年度评价表_yuzongli_agent_draft.xlsx`
  - `self-evaluation-summary.md`
  - `evidence-index.csv`
  - `evidence-gaps.md`
- compared_rules:
  - `agents/performance/2026H1-team-calibration/01-unified-data-mining-and-scoring-rules.md`
  - `agents/performance/2026H1-team-calibration/05-manager-final-calibration-checklist.md`

## 1. Executive Conclusion

余宗历 v0 包整体质量较好，且打分思路偏克制。它没有把人天、ticket 数、本地文件线索直接等同于绩效分，而是把这些作为交付量、项目连续性和复杂度信号，这一点与团队统一规则一致。

当前证据最强的是 **MB Onsite / I2 Max Navi 的持续交付和主线投入**：916h、115 个有效工作日、29 个 APRICOT ticket 引用、月度工时稳定、项目池中明确 `For Zongli`。这足以把他从原先“本地表空白导致的低模型分”拉回到正式 B 档附近。

但 v0 还不足以支撑 A 档，也暂时不建议给 B+ 高位。核心原因是质量、采纳、返工率、Figma/MasterGo 源文件、Jira/APRICOT 关闭状态和评审反馈尚未交叉验证。当前更合理的管理校准区间是：

| 口径 | 建议 |
| --- | --- |
| Excel 当前实际分 | 74.5 |
| 严格证据分 | 74-79 |
| 管理校准建议 | 78-82 |
| 有质量/采纳补证后的上探区间 | 83-86 |
| A 档可行性 | 当前不成立 |

建议先把 74.5 的档位表达修正：按通知规则，74.5 严格属于 C；若管理者认可其主责交付稳定性，应通过“主管校准”明确上调到 78-82，而不是在 74.5 上直接标 B。

## 2. Submission Completeness Check

| Required item | Status | Notes |
| --- | --- | --- |
| Evidence index | Pass | 18 rows, fields match v0.3 template. |
| Self-evaluation summary | Pass | Contains mainline contribution, project evidence, score ranges, open questions. |
| Draft evaluation xlsx | Pass with issue | Subscores are filled, but final score 74.5 conflicts with B band label. |
| Evidence gaps | Pass | Gaps are explicit and correctly prioritized. |
| Desensitization | Mostly pass | All evidence rows marked `desensitized`; local paths are redacted. Internal project/ticket IDs should stay manager-private. |

## 3. Evidence Index Audit

### 3.1 Coverage

| Metric | Result |
| --- | ---: |
| Evidence rows | 18 |
| S grade | 2 |
| A grade | 8 |
| B grade | 7 |
| C grade | 1 |
| High confidence | 2 |
| Medium-high confidence | 3 |
| Medium confidence | 7 |
| Medium-low / low confidence | 6 |

Source distribution is heavily weighted toward worklog and local spreadsheet evidence:

| Source type | Count | Audit note |
| --- | ---: | --- |
| `local_xlsx` / `local_xlsx+feishu_sheet` | 11 | Strong for delivery rhythm and scope; not enough for quality alone. |
| `task_system_ids` / `feishu_task` | 3 | Useful as issue/task linkage, but raw status and closure are incomplete. |
| `feishu_doc_meta` | 2 | Metadata only; body unread. |
| `feishu_sheet_meta` | 1 | Good cross-source consistency for worklog. |
| `local_file_index` | 1 | Low confidence; should not score until mapped to H1 project and owner. |

### 3.2 What The Evidence Can Support

Strongly supported:

- H1 主线集中在 MB Onsite / I2 Max Navi。
- 有连续、稳定、可追溯的交付节奏。
- 多模块工作面存在，包括 Mapview、Guiding / LLN、Overlay UI、Special Day Particle、IC、CPM、bugfix。
- 有结构化人天和 ticket 引用习惯。

Partially supported:

- 多轮 finetune / bugfix 说明他参与了反馈响应，但暂时不能证明响应速度或质量闭环。
- I3 Max Concept Animation 与 Special Day Particle 可作为创新/专项信号，但缺成片、评审或采纳证明。
- OKR Review、周会分享任务可作为过程和团队参与信号，但正文和实际分享材料未验证。

Not supported yet:

- A 档设计质量。
- 客户/PM/评审通过。
- 低返工或零返工。
- AI 提效 30%-50% 以上。
- 可复用设计规范、组件库、方法论产出。
- 外部好评或业务指标提升。

## 4. Excel Score Audit

### 4.1 Current Draft Scores

| Dimension | Max | Draft Score | Ratio | Audit |
| --- | ---: | ---: | ---: | --- |
| UI/UE设计产出与质量 | 50 | 39.0 | 78.0% | Reasonable B-level score. Output evidence is strong; quality proof is incomplete. |
| 项目进度与执行力 | 20 | 15.5 | 77.5% | Slightly conservative if主管确认主责稳定交付；可上调到 16-17。 |
| 设计能力与沉淀、AI工具利用 | 15 | 10.0 | 66.7% | Reasonable. AI only has 1-day signal; no strong research/methodology evidence. |
| 团队协作与沟通 | 10 | 6.25 | 62.5% | Conservative but defensible; missing meeting/message quality samples. |
| 工作规范与责任心 | 5 | 3.75 | 75.0% | Reasonable; HR/流程审计未接入。 |
| Base total | 100 | 74.5 | 74.5% | Borderline. Formal band is C, not B. |

### 4.2 Main Inconsistency

The workbook says:

- final score: 74.5
- band: `B（证据校准区间 70-79；主管建议关注 78-86；未达 A）`

This needs correction. Per the official notice in the same workbook:

- A: 90+
- B: 75-89
- C: 60-74
- D: <60

So 74.5 cannot be labeled B unless the manager applies a documented calibration adjustment to at least 75. The clean treatment is:

1. Keep `evidence_adjusted_score = 74.5`.
2. Add `manager_calibrated_score = 78-82` if主管确认主责、采纳和稳定交付。
3. Mark current raw evidence band as `C+/B boundary`, final manager band as `B` only after adjustment.

## 5. Scoring Calibration Recommendation

### 5.1 Recommended Manager Range

I recommend using **78-82** as the current manager calibration range.

Reason:

- The evidence clearly supports sustained delivery above a C-level employee.
- The v0 package is unusually transparent about limitations, which increases trust.
- The work appears to be a stable project-owner or core delivery role, but formal ownership and quality adoption still need manager confirmation.
- There is not enough verified quality or platform impact to justify 85+ yet.

### 5.2 Conditions For Upward Adjustment

Move to **83-86** only if at least two of the following are verified:

- Figma/MasterGo version export or source file list proves key deliverables and ownership.
- APRICOT/Jira export proves the 29 ticket references were closed, accepted, or materially supported by him.
- PM/customer/design review gives a脱敏 positive confirmation for I2 Max Navi, Special Day Particle, LLN, CPM, or I3 Max Concept.
- Source files or final exported assets show reusable or high-quality design output, not only worklog presence.
- Evidence shows proactive risk closure, not only bugfix participation.

Keep below **83** if:

- only worklog and metadata remain available;
- no quality/adoption proof is added;
- contribution ratio versus peers cannot be resolved.

Do not give **90+ / A** unless there is clear proof of exceptional impact beyond stable delivery, such as platform-level design influence, major stakeholder praise, measurable quality improvement, or reusable method/system contribution.

## 6. Rule-Compliance Assessment

| Rule | Result | Note |
| --- | --- | --- |
| Evidence score != performance score | Pass | Summary explicitly separates evidence-adjusted and manager range. |
| Same scoring dimensions | Pass | Uses the 50/20/15/10/5 official table. |
| No raw sensitive leakage | Pass with caution | Local paths redacted; project/ticket IDs should remain private. |
| File/version/message counts not direct score | Pass | Worklog and ticket counts are treated as signals. |
| A claims require strong evidence | Pass | A档 and加分项 are not claimed. |
| Incomplete data still submits v0 | Pass | Gaps are clearly listed. |
| Out-of-period evidence separated | Pass | 2026-07-03 OKR is marked background only. |
| Score band consistency | Needs fix | 74.5 is not B under official band rules. |

## 7. Required Follow-Up Before Final Score

Priority 1:

- Confirm H1 role: MB Onsite / I2 Max Navi 是否为其主责或核心责任面。
- Export APRICOT/Jira H1 issue list with assignee/status/close time.
- Provide at least one PM/customer/design review confirmation for quality/adoption.

Priority 2:

- Restore Figma/MasterGo evidence or export version/file list.
- Provide source file or final asset index for Special Day Particle, LLN, CPM, I3 Max Concept.
- Resolve contribution ratio versus peers mentioned in the worklog.

Priority 3:

- Read OKR Review body if authorization becomes available.
- Add meeting/minute/message category counts only as collaboration support, not direct score.
- Keep AI score at 1-1.5 unless there is a real workflow and before/after efficiency proof.

## 8. Suggested Feedback To Yuzongli Agent

Use this feedback if asking the agent for v1:

```text
v0 结构合格，证据分级和保守打分方向正确。请在 v1 修正两个问题：

1. 当前 Excel 最终分 74.5 不能直接标 B。请拆成 evidence_adjusted_score=74.5 与 manager_calibrated_range=78-82，不要混写。
2. 请优先补三类证据：Figma/MasterGo 版本或源文件索引、APRICOT/Jira ticket 关闭状态、PM/评审/客户采纳确认。

不要新增 A 档或加分项，除非有高置信原始证据。AI 提效目前仍按 1-1.5/2 处理。
```

