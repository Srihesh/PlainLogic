# Five-Day Solo Delivery Plan

This timeline assumes one builder doing deep work with disciplined handoffs between Architect, Judge, and Operator hats.

## Day 1 - Lock Contracts, Stand Up Skeleton

Build targets:

1. Environment skeleton with reset, step, and state.
2. Typed action and observation contracts.
3. Deterministic seed pipeline.
4. Task registry placeholders: easy, medium, hard.

Evidence outputs:

1. docs/contracts.md
2. Local run proving endpoint health
3. Seed replay proof for a fixed action sequence

Exit gate:

- Contract freeze complete.

## Day 2 - Easy Task End-to-End

Build targets:

1. Implement easy scenario with deterministic fixtures.
2. Implement grader_easy returning score in [0.0, 1.0].
3. Add invalid-action penalties and max-step termination.
4. Add baseline script path for easy-only smoke run.

Evidence outputs:

1. tests/easy deterministic replay pass
2. Baseline log with per-step and final easy score

Exit gate:

- Easy task runs, scores, and reproduces.

## Day 3 - Medium and Hard Tasks

Build targets:

1. Implement medium multi-constraint scenario.
2. Implement hard cascading-event scenario.
3. Finalize deterministic graders for all tasks.
4. Add anti-exploit checks for repeated no-op loops.

Evidence outputs:

1. tests for all three graders
2. Score consistency report for two repeated runs

Exit gate:

- All tasks stable and deterministic.

## Day 4 - Baseline, Docker, Deploy

Build targets:

1. Baseline script runs all tasks and returns aggregate score.
2. Docker build and startup from clean checkout.
3. Deployable configuration verified.
4. README completion with task and reward design.

Evidence outputs:

1. resilienceos/outputs/baseline_report.json
2. docker_smoke.txt
3. deploy_check.txt

Exit gate:

- Full system is deployable and verifiable.

## Day 5 - Submission Hardening

Build targets:

1. Clean-machine dry run from zero.
2. Final audit against gate checklist.
3. Package final submission links and evidence.

Evidence outputs:

1. final_run_report.json
2. submission_manifest.md
3. resilienceos/docs/final_gate_check.md

Exit gate:

- Submit only after all mandatory checks pass.

## Compression Mode (If Time Shrinks)

1. Keep day boundaries but reduce polish.
2. Never drop determinism checks.
3. Never drop deployability checks.
