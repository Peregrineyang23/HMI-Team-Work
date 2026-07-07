# 张劲 Subagent

- subagent_id: subagent-zhang-jin
- feishu_open_id: `ou_31ea317afe2ea32f637de72e613a2db9`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: zhang-jin-ai-worker

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
- team_leader: [DD002, DD009, DD013, DM005]
- team_partner: [DD001, DD002, DD004, DD006, DD012, DD017, DD018, DS001, DS002, DS003, DS004, DS005, DS006, DM001, DM002, DM006]

## Organization Team Role

- source: agents/organization-teams.yml
- team: 领域驱动
- role: domain_driven_member
