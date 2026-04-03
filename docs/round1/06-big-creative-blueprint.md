# Big Creative Blueprint: ResilienceOS

## Vision

ResilienceOS is a digital twin of a city emergency operations center.
The agent must coordinate incident response under policy, capacity, and fairness constraints.

This is not a toy simulator.
It mirrors how real operations desks handle disruption, escalation, and cascading failures.

## Why This Can Stand Out

1. High real-world relevance across public safety, healthcare ops, and infrastructure continuity.
2. Strong deterministic grading potential through fixture-based incidents.
3. Naturally long-horizon tasks with multi-step decisions.
4. Rich partial rewards without sacrificing auditability.

## Domain Model

State tracks:

1. Incident queue
	- id, severity, deadline, location, required skill type, compliance flags.
2. Resource pool
	- teams, vehicles, shift windows, remaining capacity, capability tags.
3. Infrastructure status
	- road closures, hospital load, shelter occupancy, weather risk.
4. Policy layer
	- SLA rules, escalation policy, equity guardrails, legal constraints.
5. Episode history
	- action log, violation log, step count, unresolved incident count.

## Action Schema

Core actions:

1. classify_incident
2. request_missing_fields
3. assign_resource
4. reroute_resource
5. escalate_to_regional
6. activate_shelter
7. defer_with_justification
8. close_incident

Action payload must be strict, typed, and reject malformed fields.

## Observation Schema

Observation includes:

1. Current incident snapshot subset with priorities.
2. Available resources and constraints.
3. Policy reminders relevant to current step.
4. Remaining step budget.
5. Last action result and violations.

## Task Ladder

### Easy: Single Incident Resolution

Scenario:

- One incident with complete information and one feasible best policy path.

Success emphasis:

1. Correct classification.
2. Correct resource assignment.
3. Timely closure within step budget.

### Medium: Multi-Incident Prioritization

Scenario:

- Several incidents with overlapping resource demands and differing deadlines.

Success emphasis:

1. Priority ordering quality.
2. SLA compliance.
3. Conflict-free dispatch planning.

### Hard: Cascading Event Day

Scenario:

- New critical incidents arrive mid-trajectory; weather and infrastructure constraints shift.

Success emphasis:

1. Adaptive reallocation quality.
2. Escalation correctness under policy.
3. Low collateral harm from deferred incidents.

## Deterministic Grading Design

Each task has deterministic component scores in [0, 1].

Template:

- score = 0.40 * policy_alignment + 0.35 * objective_progress + 0.25 * efficiency

Where:

1. policy_alignment is computed from explicit rule checks.
2. objective_progress measures required milestones completed.
3. efficiency is normalized from steps used and avoidable backtracks.

Final score:

- final_score = max(0.0, min(1.0, score - exploit_penalty))

## Reward Shaping

Step reward components:

1. progress_gain for each solved milestone.
2. policy_bonus for rule-compliant decisions.
3. invalid_action_penalty for malformed or impossible moves.
4. loop_penalty for repeated ineffective actions.

Keep shaping bounded and documented to avoid hidden scorer behavior.

## Anti-Reward-Hacking Controls

1. Hard max-step cutoff.
2. Repetition detector for action loops.
3. Penalty for no-op farming.
4. Deterministic fixtures from explicit seed.
5. Grader invariant tests for boundary and adversarial trajectories.

## Baseline Inference Expectations

1. Runs easy, medium, hard in one session.
2. Uses environment variable based API key flow as required.
3. Produces per-task and aggregate score output.
4. Saves machine-readable run report.

## Stretch Extensions (Only After Round 1 Stability)

1. Counterfactual analysis mode for post-incident audit.
2. Configurable policy profiles (strict, balanced, risk-tolerant).
3. Adaptive curriculum selection for training-time difficulty shaping.
