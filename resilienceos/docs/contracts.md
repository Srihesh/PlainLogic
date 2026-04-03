# ResilienceOS Contract

## Action contract

Required fields:

1. action_type
2. incident_id (optional for some actions)
3. resource_id (optional)
4. payload (key-value map)

## Observation contract

Required fields:

1. task
2. step
3. remaining_steps
4. incidents
5. resources
6. policy
7. last_result

## Step result contract

1. observation
2. reward
3. done
4. score

## Score guarantees

1. final score bounded in [0.0, 1.0]
2. deterministic scoring for identical seed and action sequence
3. non-constant grading behavior across divergent trajectories

## Task registry

Supported tasks:

1. easy
2. medium
3. hard
