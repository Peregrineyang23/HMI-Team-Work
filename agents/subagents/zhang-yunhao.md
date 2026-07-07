# 张云豪 Subagent

- subagent_id: subagent-zhang-yunhao
- feishu_open_id: `ou_2eb1838c04f94da5b2f4e42574f49a1a`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: zhang-yunhao-ai-worker

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
- team_leader: [DD012, DS005, DS006]
- team_partner: [DD001, DD002, DD004, DD006, DD010, DD014, DD015, DD018, DM003]

## Organization Team Role

- source: agents/organization-teams.yml
- team: 领域驱动
- role: domain_driven_member
