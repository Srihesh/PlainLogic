# Solo Task Cards (Use as Daily Focus Cards)

Pick one card per work block. Complete the card before switching context.

## Card 1: Architect Hat

Mission:

- Build deterministic environment mechanics and stable API contracts.

You own:

1. reset, step, and state behavior
2. typed action and observation models
3. seed handling and deterministic replay
4. done criteria and max-step enforcement

Done when:

1. State transitions are replayable under fixed seed.
2. Invalid actions are handled predictably.
3. Contract remains stable for graders and baseline.

## Card 2: Judge Hat

Mission:

- Build three graded tasks with interpretable and deterministic scoring.

You own:

1. easy, medium, hard task definitions
2. grader formulas bounded in [0.0, 1.0]
3. partial progress shaping
4. exploit and loop penalties

Done when:

1. Scores vary meaningfully by trajectory quality.
2. Same trajectory always yields same score.
3. Grader tests cover happy path and adversarial path.

## Card 3: Operator Hat

Mission:

- Make the project runnable, reproducible, and submittable.

You own:

1. Dockerfile and startup flow
2. baseline inference script and reports
3. validation command path
4. deployment and final manifest

Done when:

1. Fresh clone can build and run.
2. Baseline executes all tasks and outputs aggregate score.
3. Deployment endpoint health check passes.

## Optional Team Scaling Card

If collaborators join, map:

1. Architect Hat to Member A
2. Judge Hat to Member B
3. Operator Hat to Member C

No interface changes required.
