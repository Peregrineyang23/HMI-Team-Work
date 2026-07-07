# 李颖 Subagent

- subagent_id: subagent-li-ying
- feishu_open_id: `ou_150073c653d69ae2230f5a70b06f1d90`
- master_agent: 杨帆
- ai_worker_status: testing_planned
- ai_worker_routing_key: li-ying-ai-worker

## Employee Information

- employment_type: null
- employment_status: active
- start_date: null
- source: pending_feishu_or_manager_confirmation
- last_updated: 2026-07-04

## Project Participation

- project: AI Worker 对接测试
  role: first_integration_tester
  status: planned
  source: manager_supplied

## Responsibilities

- Receive scoped Unity HMI Design tasks from the master agent.
- Acknowledge scope, deadline, and blockers.
- Return progress and review-ready artifacts through the feedback protocol.

## AI Worker Integration

- endpoint: null
- auth: TBD
- payload_contract: TBD
- feishu_ai_bot_name: fufu 001
- worker_type: feishu_ai_bot
- integration_priority: first
- source: manager_supplied
- human_fallback: Feishu open_id above

## Domain Formation Roles

- source: agents/domain-formation.yml
- team_leader: [DD006, DM004]
- team_partner: [DD003, DD005, DD009, DD010, DD012, DD013, DD015, DD016, DS003, DM005]

## Organization Team Role

- source: agents/organization-teams.yml
- team: AI提效
- role: ai_worker_organization_coordinator
- scope: all_future_ai_workers
- initial_ai_worker: fufu 001
