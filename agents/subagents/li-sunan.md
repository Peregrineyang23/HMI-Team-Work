# 李苏南 Subagent

- subagent_id: subagent-li-sunan
- feishu_open_id: `ou_18812a2ca4748dc683cd04029dd0e70d`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: li-sunan-ai-worker

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
- team_leader: [DD004, DS001, DS004, DM001, DM002, DM003]
- team_partner: [DD001, DD003, DD006, DD009, DD010, DD012, DD013, DD017, DD018, DS004, DS007, DM004, DM005, DM006]

## Organization Team Role

- source: agents/organization-teams.yml
- team: 超级合作
- role: organization_manager
- scope: human_super_collaboration
