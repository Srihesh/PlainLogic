# Non-Collision Build Map (Solo Safe)

This map prevents self-collision when one person is rapidly shipping architecture, graders, and infra in parallel.

## Branch Strategy

Even in solo mode, use three long-lived branches.

1. core-state-contract
2. tasks-graders
3. infra-baseline-deploy

Merge order each day:

1. core-state-contract
2. tasks-graders
3. infra-baseline-deploy

## File Ownership by Hat

### Architect Hat

- src/core/state.py
- src/core/models.py
- src/core/environment.py
- src/core/seed.py

### Judge Hat

- src/tasks/easy.py
- src/tasks/medium.py
- src/tasks/hard.py
- src/graders/easy.py
- src/graders/medium.py
- src/graders/hard.py
- src/reward/shaping.py
- tests/graders/*

### Operator Hat

- scripts/baseline_inference.py
- Dockerfile
- openenv.yaml
- pyproject.toml
- scripts/run_local.sh
- scripts/validate.sh
- README.md

## Contract Freeze (Day 1 Mandatory)

Freeze these interfaces before heavy implementation:

1. Action schema
2. Observation schema
3. Step output envelope
4. Task registry signature
5. Grader signature and score bounds

Once frozen, treat them as public APIs.

## Merge Policy

Each merge must include:

1. Why the change exists
2. What contract it touches
3. Proof of deterministic behavior
4. One command for local verification

## Self-Protection Tactics

1. No mega-PRs over one subsystem in a single commit.
2. No mixed changes across state logic and infra startup in one merge.
3. Run validation before every merge.
4. Tag every stable checkpoint with date and short purpose.

## Emergency Rule

If contract breakage appears after merge, revert branch head and patch forward.
Do not hotfix directly on top of broken integration.
