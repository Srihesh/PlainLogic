# Submission Notes

Use this text as a guide when filling the hackathon submission form.

## One-line summary

ResilienceOS is a deterministic city emergency operations environment with realistic multi-incident coordination tasks, explicit policy constraints, and reproducible automated grading.

## Problem framing

The environment models emergency operations where agents must triage incidents, allocate constrained resources, satisfy escalation/shelter policies, and minimize operational failure under step limits.

## Why this environment is strong

1. Real-world utility with realistic operational constraints.
2. Deterministic reproducibility via seeded fixtures.
3. Easy/medium/hard progression for capability differentiation.
4. Explicit grader with bounded scores in [0.0, 1.0].
5. Safety-focused anti-exploit and red-team checks.
6. Strong-but-not-perfect heuristic baseline on harder tasks, leaving headroom for better policies.

## Grading logic (short)

Final score combines:

1. policy alignment
2. objective progress
3. efficiency

with bounded penalties for invalid behavior.

Objective progress explicitly rewards:

1. closure completeness
2. timely closures
3. required escalations
4. required shelter activations

## Validation evidence available

1. outputs/baseline_report.json
2. outputs/deterministic_replay_report.txt
3. outputs/round1_inference_report.json
4. outputs/red_team_report.json
5. docs/final_gate_check.md
6. outputs/eval_matrix_report.json
7. docs/gemini_sanity_checks.md
8. outputs/all_outputs_dump.txt

## Current baseline posture

1. The deterministic heuristic fully solves the easy task.
2. The deterministic heuristic is intentionally non-perfect on medium and hard tasks.
3. The multi-seed evaluation matrix reports average, min, and max aggregate score across default seeds 7, 12, and 19.

## Inference mode behavior

1. Heuristic mode runs fully offline and does not require any token.
2. Model mode requires one of: OPENAI_API_KEY, HF_TOKEN, HUGGINGFACEHUB_API_TOKEN, HF_API_TOKEN.
3. Hybrid mode uses model calls when available and safely falls back to heuristic actions.

## Research grounding

Mapped references and implementation links are documented in:

1. docs/paper_to_code_mapping.md
2. docs/round1/04-research-reference-pack.md
