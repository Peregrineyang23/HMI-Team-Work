# 李昊星 Subagent

- subagent_id: subagent-li-haoxing
- feishu_open_id: `ou_3fcdca125879f6b6c4c7337afc6ff061`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: li-haoxing-ai-worker

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
- team_partner: []

## Organization Team Role

- source: agents/organization-teams.yml
- team: 超级合作
- role: super_collaboration_member
- owner: 李苏南
