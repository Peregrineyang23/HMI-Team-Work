# Requirement

- task_id: unity-hmi-realtime-feishu-freshness-20260712
- source: Unity HMI 实时任务看板
- requester: 杨帆
- created_at: 2026-07-12T17:10:00+08:00
- priority: P0
- target_area: 实时任务看板 / 飞书群数据采集
- background: 奔腾E541汇报视频群在 7 月 12 日已有大量新进展，但看板数据源同步时间仍停留在 7 月 9 日。
- expected_output: 每次生成实时看板前分页采集已配置飞书项目群，更新消息数、最后消息时间与采集时间；采集失败时中止生成，禁止静默沿用旧快照。
- deadline: 2026-07-12
- owner_subagent_id: subagent-zhang-fan
- dependencies: 飞书 user 身份、im:message:readonly、im:chat:read、目标群可见权限
- acceptance_criteria: 奔腾视频源 last_observed_at 对齐群内最新消息；采集完整分页；看板重新生成并同步 Base；权限或分页失败时命令非零退出。
- feedback_channel: master_agent / realtime dashboard automation result

## Notes

- evidence_score 仅用于证据强度，不作为绩效分。
- 仅采集 project-map / emergency-projects 中显式配置的群，不扩展到私人目录或未配置群。
