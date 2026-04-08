# Submission Manifest

Last updated: 2026-04-07

## Project

1. Name: resilienceos
2. Version: 0.1.0
3. Domain: city emergency operations simulation

## Entry points

1. API server: resilienceos.server:app
2. Baseline script: scripts/baseline_inference.py
3. Round1 inference script: scripts/inference_round1.py

## Core artifacts

1. docs/contracts.md
2. docs/paper_to_code_mapping.md
3. docs/submission_notes.md
4. outputs/baseline_report.json
5. outputs/deterministic_replay_report.txt
6. outputs/local_validate_log.txt
7. outputs/docker_build_log.txt
8. outputs/deployment_healthcheck.txt
9. docs/final_gate_check.md
10. outputs/round1_inference_report.json
11. outputs/round1_inference_report_heuristic.json
12. outputs/red_team_report.json
13. outputs/eval_matrix_report.json
14. outputs/submission_bundle.zip
15. docs/gemini_sanity_checks.md
16. outputs/all_outputs_dump.txt

## Deterministic setup

1. Seed: 7
2. Tasks: easy, medium, hard
3. Evaluation matrix default seeds: 7, 12, 19

## Execution status

1. Baseline run: PASS
2. Determinism replay: PASS
3. Local API healthcheck: PASS
4. Tests: PASS
5. Docker build: PASS
6. Docker run: PASS
7. Round1 inference report generation: PASS
8. Evaluation matrix generation: PASS
9. Submission bundle generation: PASS
10. Tokenless heuristic sanity checks: PASS
11. Clean direct script execution without package install step: PASS
