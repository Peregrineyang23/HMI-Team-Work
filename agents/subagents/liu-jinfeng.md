# 刘锦峰 Subagent

- subagent_id: subagent-liu-jinfeng
- feishu_open_id: `ou_d805446cab590db8d825a1baa8a447e3`
- master_agent: 杨帆
- ai_worker_status: planned
- ai_worker_routing_key: liu-jinfeng-ai-worker

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
