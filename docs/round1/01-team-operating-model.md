# Operating Model: One Builder, Three Hats

## Mission

Build and submit one original OpenEnv environment that is ambitious, real-world, deterministic, and Round 1 compliant.

Target environment in this pack:

- ResilienceOS: a city emergency operations digital twin.

## Execution Principles

1. Utility before style: solve a workflow that real operations teams face.
2. Determinism before optimization: no score randomness in final grading.
3. Compliance before novelty: pass every mandatory gate first.
4. Novelty with discipline: creative state and task design, strict interfaces.

## Solo Mode Structure

Run yourself as three rotating hats each day.

1. Architect Hat
   - Owns state machine, action contract, observation contract, and episode lifecycle.
2. Judge Hat
   - Owns tasks, deterministic graders, shaping logic, and exploit prevention.
3. Operator Hat
   - Owns Docker, baseline script, reproducibility logs, and deploy flow.

Rule: never wear two hats in the same coding block.

## Working Rhythm (Solo)

1. Morning architecture block (90 minutes).
2. Midday grading block (90 minutes).
3. Evening integration and deploy block (90 minutes).
4. End-of-day release note: what changed, what broke, what is next.

## Decision Protocol

For any technical choice, score each option on 5 dimensions from 1 to 5:

1. Real-world relevance
2. Deterministic evaluability
3. Implementation risk
4. Creativity advantage
5. Submission readiness

Choose the highest total score. Tie-break with lower implementation risk.

## Completion Definition

You are done only when all are true:

1. Environment has easy, medium, hard tasks.
2. Graders produce bounded values in [0.0, 1.0].
3. Same seed and action sequence gives same score.
4. Baseline script runs end-to-end and reports reproducible aggregate score.
5. Docker build/run and deploy checks pass from clean checkout.

## If You Convert to Team Later

Use the same three hats as three people. Keep contracts unchanged.
