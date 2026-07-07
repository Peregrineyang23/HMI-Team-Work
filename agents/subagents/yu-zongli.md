# 余宗历 Subagent

- subagent_id: subagent-yu-zongli
- feishu_open_id: `ou_01722b414592fecb51b5340cf4058d85`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: yu-zongli-ai-worker

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
- team_partner: [DD003, DD004, DD012, DD013, DD017, DD018, DS001, DS003, DS005, DS007, DM004, DM005]

## Organization Team Role

- source: agents/organization-teams.yml
- team: 领域驱动
- role: domain_driven_member
