#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs
python scripts/baseline_inference.py --seed 7 --output outputs/baseline_report.json
python scripts/determinism_check.py > outputs/deterministic_replay_report.txt
