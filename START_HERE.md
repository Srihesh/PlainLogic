# Round 1 Launch Pad: Solo First, Big Scope

This repository is now an execution system, not only documentation.
You can run this plan fully solo and still scale it to a team later.

Read in this order:

1. docs/round1/06-big-creative-blueprint.md
2. docs/round1/01-team-operating-model.md
3. docs/round1/02-workstreams-non-collision.md
4. docs/round1/03-five-day-delivery-plan.md
5. docs/round1/04-research-reference-pack.md
6. docs/round1/05-submission-gate-checklist.md

What this pack is optimized for:

- Real-world utility, not toy gameplay.
- Deterministic and auditable grading.
- Clear easy/medium/hard task progression.
- Reproducible baseline execution and submission readiness.

Fast execution promise:

- If you follow this pack exactly, you will have a submission-ready Round 1 system path.
- Qualification is still judged externally, but this workflow minimizes avoidable failure modes.

Round 1 non-negotiables this pack enforces:

1. Real environment.
2. Deterministic grader in [0.0, 1.0].
3. Baseline inference script with required API-key usage pattern.
4. Docker and deployability.
5. Anti-plagiarism originality.

## Implementation now available

Code scaffold location:

- resilienceos/

Run locally:

1. cd resilienceos
2. python -m pip install -e .
3. python scripts/baseline_inference.py --seed 7 --output outputs/baseline_report.json
4. python scripts/determinism_check.py
