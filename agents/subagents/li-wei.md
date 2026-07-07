# 李玮 Subagent

- subagent_id: subagent-li-wei
- feishu_open_id: `ou_5de227ce3782ed0f198131c2317d2a33`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: li-wei-ai-worker

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
- team_leader: [DD001, DD010, DD017, DD018, DS007, DM006]
- team_partner: [DD002, DD004, DD006, DD012, DD014, DD016, DS006, DM001, DM002, DM003, DM005]

## Organization Team Role

- source: agents/organization-teams.yml
- team: 领域驱动
- role: domain_driven_member
