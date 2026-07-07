# Unity HMI Design Agents

This project uses a lead-agent model for coordinating Unity HMI Design work.

## Lead Agent

- Name: 杨帆
- Role: master_agent
- Lark open_id: `ou_ab5cf61968f074140a3e2d73d8035a9c`
- Source chat: Unity HMI Design
- Source chat_id: `oc_f2f29a95d46e0fcabfaff1636bbbfada`

The lead agent owns requirement intake, assignment, priority arbitration, delivery acceptance, and cross-agent escalation.

## Subagents

Each team member is represented by a subagent profile in `agents/subagents/`.

Subagents are expected to:

- receive scoped requirements from the lead agent;
- acknowledge ownership and expected delivery time;
- return progress, blockers, and review artifacts through the feedback protocol;
- keep a placeholder for future connection to that person's AI worker.

## Operating Rules

1. New requirements should be captured with `agents/templates/requirement.md`.
2. Assignments should reference exactly one accountable subagent unless the lead agent explicitly creates a multi-owner task.
3. Feedback should follow `agents/templates/feedback.md`.
4. Human and AI-worker routing data lives in `agents/team-roster.yml`.
5. Domain formation and role ownership live in `agents/domain-formation.yml`.
6. Team organization streams live in `agents/organization-teams.yml`.
7. Do not hard-code personal routing details elsewhere; update the roster, formation, or organization file first, then let tools consume it.
