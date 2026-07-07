# 实时任务跟踪看板规格

- generated_at: 2026-07-07
- owner: 杨帆 / master-yangfan
- dashboard: `agents/realtime-tracking/realtime-task-dashboard.html`

## 使用对象

| 角色 | 关注点 |
| --- | --- |
| 杨帆 / master_agent | 任务分发、优先级仲裁、风险升级、资源调度 |
| 项目 owner | 项目状态、交付物、评审、blocker、协作缺口 |
| 子 agent | 自己负责的任务、反馈、交付和待评审事项 |
| AI提效 owner | AI worker 接入状态、数据集、自动化收益 |

## 信息架构

第一屏直接展示任务管理视图，不做介绍页。

| 区域 | 内容 |
| --- | --- |
| 顶部状态栏 | 更新时间、数据源健康、证据覆盖、需人工校正数量 |
| 项目泳道 | 每个重点项目的任务状态、owner、风险、证据趋势 |
| 人员负载 | evidence_score、estimated_effort、manual_adjustment、confidence 分离展示 |
| 风险队列 | blocker、长时间未更新、交付物缺证据、手填与证据偏差 |
| 数据源面板 | 飞书、Jira、本地 artifact、AI 生成、微信导出接入状态 |
| 证据抽屉 | 选中项目/任务后的证据列表、来源和 confidence |

## 核心指标

| 指标 | 公式或来源 | 解释 |
| --- | --- | --- |
| project_heat | 项目近 14 天 evidence_score | 反映项目活跃度，不等于工时 |
| task_wip | doing + review + blocked | 当前执行压力 |
| blocked_count | blocked 任务 + blocker 证据 | 需要杨帆介入的风险 |
| stale_tasks | 超过阈值未更新任务 | 可能漏跟进或已在线下完成 |
| hidden_contribution | 手填负载高但 evidence 低 | 可能在本地/微信/Jira 留证 |
| visible_overload | evidence 高、任务多、confidence 高 | 可能真实过载 |
| confidence_gap | evidence 高但 project/person/task confidence 低 | 需要修项目映射或人工确认 |

## 状态定义

| 状态 | 进入条件 |
| --- | --- |
| todo | 有需求或 Jira issue，但无执行证据 |
| doing | 有近 7 天文件、评论、会议动作或状态 transition |
| review | 有评审请求、导出物、Figma comment 或会议评审结论 |
| blocked | Jira blocked、会议/消息出现阻塞、交付物超过 due_at |
| done | Jira done、飞书/微信确认交付、交付目录生成 final 文件 |
| unknown | 只有弱证据或无法归因 |

## 交互

| 控件 | 行为 |
| --- | --- |
| 时间窗口 | 7 天 / 14 天 / 30 天 / 2026 YTD |
| 项目筛选 | 重点项目、活跃项目、证据缺口项目 |
| 团队筛选 | AI提效 / 超级合作 / 领域驱动 |
| 风险筛选 | blocked、stale、overload、low confidence |
| 证据类型筛选 | 飞书、Jira、本地、Figma、AI 生成、微信导出、手填 |
| 人工校正入口 | 跳转或生成待填记录，后续进入 manual_adjustment |

## 刷新策略

| 数据 | 刷新频率 | 说明 |
| --- | --- | --- |
| dashboard state | 15 分钟 | 汇总所有增量数据 |
| Jira | 15 分钟 | 有 token 后启用 |
| 飞书群消息 | 30 分钟 | 使用最小可见范围 |
| 本地 artifact | 60 分钟 | 只扫显式配置目录 |
| 飞书会议 | 6 小时 | 搜索已结束会议和妙记 |
| Sheet/Base | 手动或 6 小时 | scope 开通前不自动 |
| 微信导出 | 手动 | 用户提供文件后导入 |

## 视觉原则

- 延续现有 `workload-dashboard-2026.html` 的静态、轻量、可本地打开方式。
- 背景保持浅色，面板密度高，优先用于扫描和决策。
- 状态色分离：红色风险、黄色待确认、绿色已联通、蓝色常规证据、紫色 AI/自动化。
- 卡片只用于指标、项目泳道、风险项和数据源项，不嵌套卡片。
- 所有文字在移动端换行，不依赖超大标题。

## Dashboard State JSON 草案

```json
{
  "generated_at": "2026-07-07T00:00:00+08:00",
  "window": "2026-ytd",
  "sources": [
    {"id": "feishu_im", "status": "online", "last_sync_at": "...", "count": 209},
    {"id": "jira", "status": "pending_credentials", "last_sync_at": null, "count": 0}
  ],
  "projects": [
    {
      "project_id": "hongqi-8397",
      "name": "红旗8397",
      "owner_agent": "subagent-zhang-jin",
      "status": "doing",
      "evidence_score": 171,
      "estimated_effort": null,
      "confidence": 0.66,
      "tasks": {"todo": 0, "doing": 3, "review": 2, "blocked": 1, "done": 0},
      "risks": ["Sheet/Base 明细未授权", "本地 DCC 产出待接入"]
    }
  ],
  "people": [
    {
      "agent_id": "subagent-li-ying",
      "name": "李颖",
      "organization_team": "AI提效",
      "evidence_score": 101.5,
      "estimated_effort": null,
      "manual_adjustment": 0,
      "confidence": 0.68
    }
  ]
}
```

## 验收标准

- 看板第一屏能看到项目状态、风险、数据源健康和人员负载，不需要阅读说明。
- evidence_score、estimated_effort、confidence、manual_adjustment 独立展示。
- 本地文件扫描未配置目录时输出空索引，不读取私人目录。
- 张婕和李达不会出现在新任务 owner 或新分配建议中。
- 每个任务只能有一个 accountable subagent；多人协作通过 collaborators 表示。
