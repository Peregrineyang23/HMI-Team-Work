# Agent Dispatch Protocol

## Purpose

This protocol defines how the master agent distributes Unity HMI Design requirements to subagents and receives feedback from humans or future AI workers.

## Roles

- Master agent: 杨帆 owns intake, decomposition, priority, assignment, acceptance, and escalation.
- Subagent: one team member or that member's future AI worker.
- Shared bot: group-level automation or meeting context source.

## Requirement Flow

1. Intake: capture the source, requester, business goal, target vehicle or HMI surface, deadline, and acceptance criteria.
2. Decomposition: split the request into deliverable tasks with a clear owner, inputs, outputs, and review point.
3. Dispatch: send the task to the selected subagent through Feishu first; when an AI worker endpoint is available, route to both the human and AI worker.
4. Acknowledgement: the subagent confirms scope, deadline, and known blockers.
5. Execution: the subagent works independently, asks clarifying questions, and posts progress.
6. Feedback: the subagent returns artifacts, summary, risks, and next-step recommendation.
7. Acceptance: the master agent accepts, requests revision, or escalates.

## Dispatch Contract

Every assignment should include:

- task_id
- owner_subagent_id
- source_requirement
- expected_output
- deadline
- priority: P0, P1, P2, or P3
- dependencies
- acceptance_criteria
- feedback_channel

## Feedback Contract

Every feedback response should include:

- task_id
- status: accepted, in_progress, blocked, ready_for_review, or done
- summary
- changed_artifacts
- decisions_needed
- blockers
- next_check_in

## Future AI Worker Routing

The roster stores `ai_worker.status`, `endpoint`, and `routing_key` for each subagent. Keep the status as `planned` until a real worker is available.

When a worker is connected:

1. update the matching `ai_worker.endpoint`;
2. set `ai_worker.status` to `active`;
3. document authentication and payload shape in that subagent profile;
4. keep Feishu open_id as the human fallback route.
