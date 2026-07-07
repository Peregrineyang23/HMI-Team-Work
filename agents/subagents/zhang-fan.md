# 张帆 Subagent

- subagent_id: subagent-zhang-fan
- feishu_open_id: `ou_e16bdf7c1be402a79e35c6f13e1c464d`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: zhang-fan-ai-worker

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
- team_leader: [DD015]
- team_partner: [DD001, DD005, DD010, DD012, DD014, DD016, DD018, DS005, DM006]

## Organization Team Role

- source: agents/organization-teams.yml
- team: 领域驱动
- role: domain_driven_member
