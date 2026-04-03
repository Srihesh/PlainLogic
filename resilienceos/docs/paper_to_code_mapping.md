# Paper-to-Code Mapping

This file maps research references to concrete implementation points in ResilienceOS.

## 1) WebArena: realistic and reproducible environments

Reference:

1. Zhou et al., WebArena, arXiv:2307.13854

Applied here:

1. src/resilienceos/fixtures.py
2. src/resilienceos/environment.py

How applied:

1. Deterministic seeded fixtures.
2. Easy, medium, hard progression with realistic operational constraints.

## 2) Concrete Problems in AI Safety

Reference:

1. Amodei et al., arXiv:1606.06565

Applied here:

1. src/resilienceos/grading.py
2. src/resilienceos/environment.py
3. scripts/red_team_eval.py

How applied:

1. Invalid action penalties and exploit resistance.
2. Loop tracking and bounded scoring.
3. Red-team trajectories for adversarial behavior checks.

## 3) Planning efficiency vs discriminator quality

Reference:

1. Chen et al., arXiv:2402.10890

Applied here:

1. scripts/inference_round1.py
2. src/resilienceos/baseline.py

How applied:

1. Heuristic policy mode for fast reliable execution.
2. Hybrid fallback mode to avoid expensive fragile planning paths.

## 4) Frontier capability evaluation methodology

Reference:

1. Phuong et al., arXiv:2403.13793

Applied here:

1. scripts/red_team_eval.py
2. final_gate_check.md

How applied:

1. Structured failure-mode checks are codified and logged.
2. Evaluation is explicit, repeatable, and artifact-backed.
