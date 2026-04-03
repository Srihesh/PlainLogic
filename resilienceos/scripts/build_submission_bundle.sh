#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT_DIR="$ROOT_DIR/outputs"
OUT_DIR="$OUTPUT_DIR/submission_bundle"
ZIP_PATH="$OUTPUT_DIR/submission_bundle.zip"

mkdir -p "$OUTPUT_DIR"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR/docs" "$OUT_DIR/scripts" "$OUT_DIR/src"

copy_if_exists() {
  local src="$1"
  local dst="$2"
  if [[ -e "$src" ]]; then
    cp -R "$src" "$dst"
  else
    echo "WARN missing: $src"
  fi
}

copy_if_exists "$ROOT_DIR/README.md" "$OUT_DIR/"
copy_if_exists "$ROOT_DIR/openenv.yaml" "$OUT_DIR/"
copy_if_exists "$ROOT_DIR/pyproject.toml" "$OUT_DIR/"
copy_if_exists "$ROOT_DIR/Dockerfile" "$OUT_DIR/"

copy_if_exists "$ROOT_DIR/docs/contracts.md" "$OUT_DIR/docs/"
copy_if_exists "$ROOT_DIR/docs/paper_to_code_mapping.md" "$OUT_DIR/docs/"
copy_if_exists "$ROOT_DIR/docs/submission_notes.md" "$OUT_DIR/docs/"
copy_if_exists "$ROOT_DIR/docs/index.md" "$OUT_DIR/docs/"

copy_if_exists "$ROOT_DIR/src/resilienceos" "$OUT_DIR/src/"
copy_if_exists "$ROOT_DIR/scripts/baseline_inference.py" "$OUT_DIR/scripts/"
copy_if_exists "$ROOT_DIR/scripts/inference_round1.py" "$OUT_DIR/scripts/"
copy_if_exists "$ROOT_DIR/scripts/red_team_eval.py" "$OUT_DIR/scripts/"
copy_if_exists "$ROOT_DIR/scripts/eval_matrix.py" "$OUT_DIR/scripts/"
copy_if_exists "$ROOT_DIR/scripts/run_round1_inference.sh" "$OUT_DIR/scripts/"

copy_if_exists "$ROOT_DIR/docs/final_gate_check.md" "$OUT_DIR/"
copy_if_exists "$ROOT_DIR/docs/submission_manifest.md" "$OUT_DIR/"
copy_if_exists "$ROOT_DIR/docs/gemini_sanity_checks.md" "$OUT_DIR/"
copy_if_exists "$OUTPUT_DIR/all_outputs_dump.txt" "$OUT_DIR/"
copy_if_exists "$OUTPUT_DIR/baseline_report.json" "$OUT_DIR/"
copy_if_exists "$OUTPUT_DIR/deterministic_replay_report.txt" "$OUT_DIR/"
copy_if_exists "$OUTPUT_DIR/deployment_healthcheck.txt" "$OUT_DIR/"
copy_if_exists "$OUTPUT_DIR/round1_inference_report.json" "$OUT_DIR/"
copy_if_exists "$OUTPUT_DIR/round1_inference_report_heuristic.json" "$OUT_DIR/"
copy_if_exists "$OUTPUT_DIR/red_team_report.json" "$OUT_DIR/"
copy_if_exists "$OUTPUT_DIR/eval_matrix_report.json" "$OUT_DIR/"
copy_if_exists "$OUTPUT_DIR/test_log.txt" "$OUT_DIR/"

rm -f "$ZIP_PATH"
(
  cd "$OUTPUT_DIR"
  zip -r "$ZIP_PATH" submission_bundle >/dev/null
)

echo "Built: $OUT_DIR"
echo "Built: $ZIP_PATH"
