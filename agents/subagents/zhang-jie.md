# 张婕 Subagent

- subagent_id: subagent-zhang-jie
- feishu_open_id: `ou_bdefa45bc7f6bb146473878136cd5095`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: zhang-jie-ai-worker

## Employee Information

- employment_status: departure_planned
- source: manager_supplied
- notes: 即将离职；不纳入新的项目工作担当分析或后续任务分配。

## Responsibilities

- Receive scoped Unity HMI Design tasks from the master agent.
- Acknowledge scope, deadline, and blockers.
- Return progress and review-ready artifacts through the feedback protocol.

## AI Worker Integration

- endpoint: null
- auth: TBD
- payload_contract: TBD
- human_fallback: Feishu open_id above

## Domain Formation Roles

- source: agents/domain-formation.yml
- team_leader: []
- team_partner: [DD006, DD009, DD010, DS002, DM005]

## Organization Team Role

- source: agents/organization-teams.yml
- team: 领域驱动
- role: transition_member
- assignment_policy: do_not_assign_new_work
