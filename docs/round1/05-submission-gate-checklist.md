# Round 1 Submission Gate Checklist

Use this as a strict pass/fail gate before submitting.

## A. Environment Validity

1. Environment models a real operational workflow, not a toy game.
2. reset, step, and state endpoints are functional.
3. Action and observation schemas are explicit and typed.
4. Task set includes easy, medium, and hard.
5. Every task has a deterministic grader.
6. Grader returns are always in [0.0, 1.0].

## B. Grading and Determinism

1. Two identical seeded runs produce identical final scores.
2. Grader scores are not constant across all attempts.
3. Partial-progress shaping exists and is documented.
4. Invalid actions trigger measurable penalties.
5. Looping behavior is bounded with max-step termination.

## C. Baseline Script Compliance

1. Baseline script reads required API key from environment variables.
2. Baseline script executes all tasks and reports per-task scores.
3. Aggregate score is computed and printed.
4. Output includes metadata: model, seed, task names, run timestamp.
5. Script fails loudly on missing configuration.

## D. Packaging and Deployment

1. Docker image builds from clean checkout.
2. Container starts and serves expected endpoints.
3. Local validation passes before deployment.
4. Deployment target is live and reachable.
5. Final submission link resolves and is usable.

## E. Originality and Safety

1. No copied public environment code path without substantial transformation.
2. No renamed clone of known benchmark tasks.
3. No obvious reward-hacking shortcut (for example, no-op farming).
4. No hidden assumptions that only work on one machine.

## F. Evidence Bundle (Create Before Submit)

1. resilienceos/outputs/baseline_report.json
2. resilienceos/outputs/deterministic_replay_report.txt
3. resilienceos/outputs/docker_build_log.txt
4. resilienceos/outputs/local_validate_log.txt
5. resilienceos/outputs/deployment_healthcheck.txt
6. resilienceos/docs/submission_manifest.md

## G. README Must Include

1. Problem framing and practical utility.
2. Action and observation schema definitions.
3. Task progression: easy, medium, hard.
4. Grader formula and score-bound guarantees.
5. Reward shaping and anti-exploit policy.
6. Local, Docker, and deployment run instructions.
7. Reproducibility instructions with fixed seed.

## H. Final Dry Run

1. Clone repo into a fresh directory.
2. Run setup commands exactly as README states.
3. Run validation.
4. Run baseline script twice with same seed.
5. Confirm equal scores across both runs.
6. Build and run Docker.
7. Confirm deployment endpoint health.
8. Submit only after every gate is green.
