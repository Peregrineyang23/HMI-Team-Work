# 2026H1 定量绩效模型生成说明

- generated_at: 2026-07-08
- model_version: 0.2
- workbook: `agents/performance/2026H1-performance-weight-model.xlsx`
- local_employee_forms: `/Users/frankyang/my_work/My_Team/2025 Mid-year review/xlsx`

## 生成结果

已生成一份可调权重 Excel 模型。权重位于 `01_权重设置`，员工输入位于 `04_员工输入`，模型预估分位于 `05_模型算分`，总览位于 `00_总览`。

## 当前数据状态

- 本地员工评价表数量：15
- active 分析成员：14
- 空模板评价表：15
- 排除/过渡成员：张婕

当前 `/Users/frankyang/my_work/My_Team/2025 Mid-year review/xlsx` 中的员工评价表均处于模板态，子项分为空，基础分/最终分为 0。因此模型不会把这些空表当作真实绩效 0 分，而是把本地表状态标记为 `template_blank`，并用现有项目/角色/负载规则生成临时基线分。后续本地表填写后，该基线会自动替换为人工评价分。

## 使用方式

1. 打开 `agents/performance/2026H1-performance-weight-model.xlsx`。
2. 在 `01_权重设置` 调整蓝色/黄色参数。
3. 后续接入 Jira、本地文件索引、Figma raw export、飞书会议 raw JSON 后，更新 `04_员工输入` 或扩展证据输入。
4. 查看 `05_模型算分` 和 `00_总览` 的动态结果。
5. 查看 `06_当前评分快照` 或 `agents/performance/2026H1-performance-score-snapshot.csv` 获取当前默认权重下的静态建议分。

## 主线规则

主线评分不直接等同于文件数量或会议数量，而是由主线产出、角色责任、影响力、推进闭环、证据置信度组成。详见 workbook 的 `02_主线打分规则`。

## 版本管理

- `performance-score-model-v0.1.yml`：小范围绩效评分草案与李颖样本审计。
- `performance-score-model-v0.2.yml`：当前可调权重模型配置。
- workbook `99_版本记录`：记录 Excel 模型版本变更。
