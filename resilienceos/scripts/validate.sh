#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs
python -c "from resilienceos import ResilienceOSEnvironment; env = ResilienceOSEnvironment(); env.reset(task='easy', seed=7); print('validate_ok')" > outputs/local_validate_log.txt
python scripts/determinism_check.py > outputs/deterministic_replay_report.txt
