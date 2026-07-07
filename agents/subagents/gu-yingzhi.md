# 顾颖芝 Subagent

- subagent_id: subagent-gu-yingzhi
- feishu_open_id: `ou_2bf8fe6c956f4dc994847f6a4c9d8dcc`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: gu-yingzhi-ai-worker

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
- team_leader: [DD003, DD016, DS002, DS003]
- team_partner: [DD004, DD005, DD006, DD009, DD015, DS001, DS007, DM001]

## Organization Team Role

- source: agents/organization-teams.yml
- team: 领域驱动
- role: domain_driven_member
