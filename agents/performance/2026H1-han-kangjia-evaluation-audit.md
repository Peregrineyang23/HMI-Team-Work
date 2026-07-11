# 2026H1 韩康佳自评证据包校验与评分审计

- release_level: PRIVATE
- audit_date: 2026-07-10
- subject: 韩康佳
- source_folder: `/Users/frankyang/my_work/My_Team/2026 Mid-year review/xlsx/韩康佳/韩康佳_2026H1_v0`
- source_files:
  - `evidence-index.csv`
  - `evidence-gaps.md`
- target_workbook: `/Users/frankyang/my_work/My_Team/2026 Mid-year review/xlsx/韩康佳/2026H1半年度评价表_韩康佳.xlsx`
- compared_rules:
  - `agents/performance/2026H1-team-calibration/01-unified-data-mining-and-scoring-rules.md`

## 1. Executive Conclusion

韩康佳 v0 证据包的覆盖面较强，明显不是单一项目或单一工具链材料。当前 28 条证据覆盖红旗8397、广汽本田音乐可视化、东风哨兵模式、东风8397 / 4SR、北京车展、紫光展锐和 AI OS Pets 等项目，其中 S 级 10 条、A 级 15 条，能较好支撑“多项目持续交付 + 视觉/动效/音乐可视化方向较强”的判断。

当前不建议直接给 A 档。核心原因是：多数高质量判断仍缺客户确认、正式采纳、评审结论、MasterGo / Figma 作者级版本记录、开发验收或明确低返工证据。本地文件规模和 Figma 节点数量能证明复杂度和产出存在，但不能直接折算为个人质量或客户认可。

建议当前管理校准：

| 口径 | 建议 |
| --- | ---: |
| 当前管理建议分 | 85 |
| 当前档位 | B 高位 / B+ |
| 补齐关键采纳与作者证据后 | 87-88 |
| A 档可行性 | 当前不成立 |

## 2. Submission Completeness

| Required item | Status | Notes |
| --- | --- | --- |
| Evidence index | Pass | 28 rows,字段与 v0.3/v0.4 模板一致。 |
| Evidence gaps | Pass | 缺口清晰，尤其客户确认、MasterGo、钉钉和 AI 工具材料。 |
| Self-evaluation summary | Missing | 未提交；需由审计侧根据 evidence-index 汇总。 |
| Draft evaluation xlsx | Missing | 未提交 agent draft；正式表仍为空白模板。 |
| Desensitization | Pass | 28 条均标记 `desensitized`。 |

缺 summary 和 agent draft 不代表证据无效，但会降低管理判断的可解释性。因此本次正式表采用“管理校准分”，并在支撑论据中保留补证条件。

## 3. Evidence Coverage

| Metric | Count |
| --- | ---: |
| Evidence rows | 28 |
| S grade | 10 |
| A grade | 15 |
| B grade | 2 |
| C grade | 1 |
| High confidence | 10 |
| Medium-high confidence | 15 |
| Medium confidence | 2 |
| Medium-low confidence | 1 |

Source distribution:

| Source type | Count | Audit note |
| --- | ---: | --- |
| `figma` / `figma_slides` | 9 | 设计结构、节点、阶段版本强，但作者级归属仍需版本记录交叉。 |
| `lark_task` | 4 | 任务完成、评审和归档信号较强。 |
| `lark_im` | 6 | 可支撑协作、反馈和现场调试，但消息仍需结果佐证。 |
| `local_file_index` | 5 | 能证明本地源文件、视频、PPT/PDF、工程文件存在；需去重和采用状态。 |
| `lark_weekly` | 4 | 可支撑进度、风险说明和自填周报线索；需任务/交付交叉验证。 |

## 4. What The Evidence Supports

Strongly supported:

- 多项目覆盖：红旗8397、广本音乐可视化、东风哨兵模式、东风8397 / 4SR、北京车展、紫光展锐。
- 红旗8397和东风/广本音乐可视化方向有较强设计产出与迭代线索。
- 有任务、周报、消息和本地文件的多源交叉，不只是自述。
- 有现场调试、开发答疑、需求变更对接和交付归档行为。

Partially supported:

- 设计质量与最终采用：有评审版、确认版、冻结、开发版等信号，但缺客户/PM/开发正式确认。
- 个人贡献比例：任务和消息能证明参与，但 Figma/MasterGo 节点作者不可直接读取。
- 规范与流程：有反馈归档到 Wiki 和 Figma 链接动作，但不能外推全部流程零问题。

Not supported yet:

- A 档质量。
- 客户正式认可、验收或上线采纳。
- Lovart / Midjourney / LibTV / 钉钉材料。
- AI 提效或工具链复用。
- 明确带教新人或团队级方法论沉淀。

## 5. Scoring Recommendation

| Dimension | Max | Recommended | Rationale |
| --- | ---: | ---: | --- |
| UI/UE设计产出与质量 | 50 | 42.0 | 多项目、多源文件和设计版本证据强；质量/采纳仍缺最终确认。 |
| 项目进度与执行力 | 20 | 17.0 | 任务、周报和消息能证明推进、现场调试和开发配合；闭环时效仍需补。 |
| 设计能力与沉淀、AI工具利用 | 15 | 11.5 | 有策略稿、语音形象分析、音乐可视化方案；AI工具与方法论沉淀仍不足。 |
| 团队协作与沟通 | 10 | 9.0 | 客户/UI/开发/TA沟通、开发答疑、需求变更对接证据较强；质量结果仍需佐证。 |
| 工作规范与责任心 | 5 | 4.5 | 任务归档、周报、现场调试和交付动作体现责任心；流程零问题需确认。 |
| Base total | 100 | 84.0 | B 高位，接近 B+。 |
| Bonus | - | 1.0 | 可给“主导/承担多项目视觉专项”保守加分；不重复计算基础职责。 |
| Deduction | - | 0 | 未见明确负面证据。 |
| Final | - | 85.0 | B 高位 / B+。 |

## 6. Upward Conditions

如补齐以下任意两类证据，可考虑上探至 87-88：

- 红旗8397、广本音乐可视化、东风哨兵或东风4SR 的客户/PM/开发采纳确认。
- MasterGo / Figma 版本作者记录，证明关键页面或最终方案的本人贡献比例。
- 交付验收、上线采用、问题关闭、低返工记录。
- Lovart / Midjourney / LibTV 材料与项目采用关系被确认。
- 钉钉文档/消息能证明需求澄清、反馈闭环或交付确认。

当前不建议 90+。A 档需要更明确的关键项目主责、质量/采纳结果、团队级影响或可复用方法论证据。

