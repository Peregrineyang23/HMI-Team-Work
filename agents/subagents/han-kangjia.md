# 韩康佳 Subagent

- subagent_id: subagent-han-kangjia
- feishu_open_id: `ou_51ffbe7308fbb641a65eb15d3fa2021e`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: han-kangjia-ai-worker

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
- team_leader: [DD005, DD014]
- team_partner: [DD001, DD002, DD004, DD006, DD013, DD017, DS002, DM004]

## Organization Team Role

- source: agents/organization-teams.yml
- team: 领域驱动
- role: domain_driven_member
